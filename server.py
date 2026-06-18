"""
R Training Bot — FastAPI backend.
Run: python server.py
"""
import re
import sys
import tempfile
import threading
import webbrowser
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from lessons import LESSONS, LESSON_TITLES
from data_manager import (
    load_profile, save_profile,
    load_progress, save_history, clear_history,
    mark_lesson_complete, set_current_lesson, reset_progress,
    load_settings, save_settings,
)
from prompt_builder import build_system_prompt
from curriculum import plan_for, recommended_start
from llm_router import chat as llm_chat


def _static(name: str) -> Path:
    base = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent
    return base / "static" / name


def _extract(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(p.get("text", "") for p in content if isinstance(p, dict))
    return str(content)


app = FastAPI(title="R Training Bot", docs_url=None, redoc_url=None)


# ── UI ────────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse(_static("index.html"))


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatReq(BaseModel):
    message: str
    history: list
    api_key: str = ""
    model_choice: str = "auto"
    model_name: str = ""


@app.post("/api/chat")
def chat(req: ChatReq):
    cur = load_progress().get("current_lesson", 1)
    sp = build_system_prompt(load_profile(), depth=load_settings().get("depth", "standard"),
                             current_lesson=cur)
    msgs = [{"role": m["role"], "content": _extract(m["content"])} for m in req.history]
    msgs.append({"role": "user", "content": req.message})

    reply = llm_chat(msgs, system_prompt=sp,
                     api_key=req.api_key.strip(), model_choice=req.model_choice,
                     model_name=req.model_name.strip())

    completed_id = None
    m = re.search(r"✅\s*[Ll]esson\s+(\d+)\s+complete", reply)
    if m:
        completed_id = int(m.group(1))
        mark_lesson_complete(completed_id)

    history = req.history + [
        {"role": "user",      "content": req.message},
        {"role": "assistant", "content": reply},
    ]
    save_history(history)
    p = load_progress()
    return {
        "reply": reply,
        "lesson_completed": completed_id,
        "current_lesson": p.get("current_lesson", 1),
        "completed": p.get("completed", []),
    }


class JumpReq(BaseModel):
    lesson_id: int
    history: list
    api_key: str = ""
    model_choice: str = "auto"
    model_name: str = ""


@app.post("/api/jump")
def jump(req: JumpReq):
    set_current_lesson(req.lesson_id)
    sp    = build_system_prompt(load_profile(), depth=load_settings().get("depth", "standard"),
                                current_lesson=req.lesson_id)
    title = LESSON_TITLES.get(req.lesson_id, "")
    instr = (f"Please start teaching Lesson {req.lesson_id}: {title}. "
             "Begin with the mental model in 2–3 sentences, then a short example, "
             "then ask the quick-check question.")
    msgs = [{"role": m["role"], "content": _extract(m["content"])} for m in req.history]
    msgs.append({"role": "user", "content": instr})

    reply = llm_chat(msgs, system_prompt=sp,
                     api_key=req.api_key.strip(), model_choice=req.model_choice,
                     model_name=req.model_name.strip())
    history = req.history + [
        {"role": "user",      "content": f"→ Lesson {req.lesson_id}: {title}"},
        {"role": "assistant", "content": reply},
    ]
    save_history(history)
    return {"reply": reply, "title": title}


# ── Progress ──────────────────────────────────────────────────────────────────

def _prog():
    p = load_progress()
    profile = load_profile()
    plan = plan_for(profile)
    lessons = [{**l, "treatment": plan.get(l["id"], "full")} for l in LESSONS]
    return {
        "current_lesson":    p.get("current_lesson", 1),
        "completed":         p.get("completed", []),
        "history":           p.get("history", []),
        "total":             len(LESSONS),
        "lessons":           lessons,
        "recommended_start": recommended_start(profile, p.get("completed", [])),
    }


@app.get("/api/progress")
def get_progress():
    return _prog()


@app.post("/api/progress/complete")
def complete_lesson():
    mark_lesson_complete(load_progress().get("current_lesson", 1))
    return _prog()


@app.post("/api/progress/reset")
def reset():
    reset_progress()
    return _prog()


# ── Profile ───────────────────────────────────────────────────────────────────

class ProfileReq(BaseModel):
    languages: list
    use_case: str


@app.get("/api/profile")
def get_profile():
    return load_profile()


@app.post("/api/profile")
def post_profile(req: ProfileReq):
    save_profile({"languages": req.languages, "use_case": req.use_case})
    return {"ok": True}


# ── Settings ──────────────────────────────────────────────────────────────────

class SettingsReq(BaseModel):
    claude_key:        Optional[str] = None
    openai_key:        Optional[str] = None
    model_choice:      Optional[str] = None
    model_name:        Optional[str] = None
    remember_key:      bool = False
    depth:             Optional[str] = None   # "fast" | "standard" | "deep"
    goal_lessons:      Optional[int] = None   # 15 | 22 | 30
    sessions_per_week: Optional[int] = None   # 1–7


@app.get("/api/settings")
def get_settings():
    return load_settings()


@app.post("/api/settings")
def post_settings(req: SettingsReq):
    s = load_settings()
    s["model_choice"] = req.model_choice or "auto"
    s["model_name"]   = req.model_name or ""
    s["depth"]             = req.depth if req.depth in ("fast", "standard", "deep") else "standard"
    if req.goal_lessons      is not None: s["goal_lessons"]      = max(1, min(30, req.goal_lessons))
    if req.sessions_per_week is not None: s["sessions_per_week"] = max(1, min(7,  req.sessions_per_week))
    if req.remember_key:
        if req.claude_key: s["claude_key"] = req.claude_key
        if req.openai_key: s["openai_key"] = req.openai_key
    else:
        s.pop("claude_key", None)
        s.pop("openai_key", None)
        s.pop("api_key", None)   # clear legacy single-key format
    save_settings(s)
    return {"ok": True}


# ── Ollama model discovery ────────────────────────────────────────────────────

@app.get("/api/ollama/models")
def get_ollama_models():
    try:
        import urllib.request, json as _json
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            data = _json.loads(r.read())
        names = sorted(m["name"] for m in data.get("models", []))
        return {"models": names, "available": True}
    except Exception:
        return {"models": [], "available": False}


# ── Export ────────────────────────────────────────────────────────────────────

class ExportReq(BaseModel):
    history: list


@app.post("/api/export")
def export_chat(req: ExportReq):
    lines = ["# R Training Bot — Session Export\n\n"]
    for m in req.history:
        role = "**You**" if m["role"] == "user" else "**Tutor**"
        lines.append(f"{role}:\n\n{_extract(m['content'])}\n\n---\n\n")
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                      prefix="r_training_", encoding="utf-8")
    tmp.write("".join(lines))
    tmp.close()
    return FileResponse(tmp.name, media_type="text/markdown",
                        filename="r_training_export.md")


# ── History management ───────────────────────────────────────────────────────

class SaveHistoryReq(BaseModel):
    history: list


@app.post("/api/history/save")
def save_history_endpoint(req: SaveHistoryReq):
    save_history(req.history)
    return {"ok": True}


@app.post("/api/history/clear")
def clear_history_endpoint():
    clear_history()
    return {"ok": True}


# ── Compact ───────────────────────────────────────────────────────────────────

_COMPACT_PROMPT = (
    "You are writing a brief session handover note for an R programming tutor bot. "
    "Summarise the conversation in under 200 words covering: "
    "(1) which lessons were completed (number + title), "
    "(2) concepts the student demonstrated understanding of, "
    "(3) any recurring mistakes or gaps to watch for, "
    "(4) exactly where the session ended — current lesson, what was being taught, "
    "and whether the quick-check question is still open. "
    "Write in compact prose. No bullet points. No preamble. Start directly."
)


class CompactReq(BaseModel):
    history: list
    api_key: str = ""
    model_choice: str = "auto"
    model_name: str = ""


@app.post("/api/compact")
def compact_chat(req: CompactReq):
    if not req.history:
        return {"summary": "No history to summarise."}
    msgs = [{"role": m["role"], "content": _extract(m["content"])} for m in req.history]
    msgs.append({"role": "user", "content": "Write the session summary now."})
    summary = llm_chat(msgs, system_prompt=_COMPACT_PROMPT,  # compact uses its own prompt, depth N/A
                       api_key=req.api_key.strip(), model_choice=req.model_choice,
                       model_name=req.model_name.strip())
    return {"summary": summary}


# ── Launch ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    PORT = 7860

    def _open():
        import time; time.sleep(1.0)
        webbrowser.open(f"http://127.0.0.1:{PORT}")

    threading.Thread(target=_open, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")

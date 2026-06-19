"""
Reads and writes everything the app persists, under user_data/ (next to the exe or
script, created on first run). The layout is kept tidy and easy to inspect:

    user_data/
      profile.json          languages you know + your use-case
      settings.json         preferences only (model choice, depth, goal, target language)
      keys.json             API keys, kept separate from preferences (only if "Remember key")
      progress/<lang>.json  { current_lesson, completed }  — one small file per language
      history/<lang>.json   the chat transcript for that language

Progress and history are PER TARGET LANGUAGE, so switching what you're learning never
clobbers another language. `migrate()` upgrades the old flat layout in place (keeping a
progress.json.bak backup) and is safe to call repeatedly.
"""

import json
import sys
from pathlib import Path


# ── Paths ───────────────────────────────────────────────────────────────────--

def _user_data_dir() -> Path:
    base = Path(sys.executable).parent if hasattr(sys, "_MEIPASS") else Path(__file__).parent
    d = base / "user_data"
    d.mkdir(exist_ok=True)
    return d


def _subdir(name: str) -> Path:
    d = _user_data_dir() / name
    d.mkdir(exist_ok=True)
    return d


def _read(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return default


def _write(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Profile ───────────────────────────────────────────────────────────────────

def profile_exists() -> bool:
    return (_user_data_dir() / "profile.json").exists()


def load_profile() -> dict:
    return _read(_user_data_dir() / "profile.json", {})


def save_profile(profile: dict) -> None:
    _write(_user_data_dir() / "profile.json", profile)


# ── Progress & history (per target language) ───────────────────────────────────

def _empty_progress() -> dict:
    return {"current_lesson": 1, "completed": []}


def load_progress(language: str) -> dict:
    """Combined view the API/UI expect: {current_lesson, completed, history}."""
    p = _read(_subdir("progress") / f"{language}.json", _empty_progress())
    return {
        "current_lesson": p.get("current_lesson", 1),
        "completed":      p.get("completed", []),
        "history":        _read(_subdir("history") / f"{language}.json", []),
    }


def _save_lesson_state(language: str, current_lesson: int, completed: list) -> None:
    _write(_subdir("progress") / f"{language}.json",
           {"current_lesson": current_lesson, "completed": completed})


def mark_lesson_complete(language: str, lesson_id: int) -> None:
    p = load_progress(language)
    completed = p["completed"]
    if lesson_id not in completed:
        completed.append(lesson_id)
    _save_lesson_state(language, lesson_id + 1, completed)


def set_current_lesson(language: str, lesson_id: int) -> None:
    p = load_progress(language)
    _save_lesson_state(language, lesson_id, p["completed"])


def save_history(language: str, history: list) -> None:
    _write(_subdir("history") / f"{language}.json", history[-80:])


def clear_history(language: str) -> None:
    _write(_subdir("history") / f"{language}.json", [])


def reset_progress(language: str) -> None:
    """Reset just this language — its progress and history. Others are untouched."""
    for path in (_subdir("progress") / f"{language}.json",
                 _subdir("history") / f"{language}.json"):
        if path.exists():
            path.unlink()


# ── Settings (preferences) & keys (separate file) ──────────────────────────────

def load_settings() -> dict:
    return _read(_user_data_dir() / "settings.json", {})


def save_settings(settings: dict) -> None:
    _write(_user_data_dir() / "settings.json", settings)


def load_keys() -> dict:
    return _read(_user_data_dir() / "keys.json", {})


def save_keys(keys: dict) -> None:
    _write(_user_data_dir() / "keys.json", keys)


def clear_keys() -> None:
    p = _user_data_dir() / "keys.json"
    if p.exists():
        p.unlink()


def get_target_language() -> str:
    return load_settings().get("target_language", "R")


def set_target_language(language: str) -> None:
    s = load_settings()
    s["target_language"] = language
    save_settings(s)


# ── One-time migration from the old flat layout ────────────────────────────────

def migrate() -> None:
    """Upgrade legacy user_data in place. Idempotent and backup-preserving."""
    ud = _user_data_dir()

    # 1) progress.json  ->  progress/<lang>.json + history/<lang>.json
    old = ud / "progress.json"
    if old.exists():
        data = _read(old, {})
        if any(k in data for k in ("current_lesson", "completed", "history")):
            data = {"R": data}                       # pre-multi-language flat shape
        for lang, p in data.items():
            if not isinstance(p, dict):
                continue
            _save_lesson_state(lang, p.get("current_lesson", 1), p.get("completed", []))
            _write(_subdir("history") / f"{lang}.json", p.get("history", []))
        old.rename(ud / "progress.json.bak")         # keep a backup; stops re-migrating

    # 2) API keys living inside settings.json  ->  keys.json
    s = _read(ud / "settings.json", {})
    if any(k in s for k in ("claude_key", "openai_key", "api_key")):
        keys = {k: s[k] for k in ("claude_key", "openai_key") if s.get(k)}
        if keys:
            save_keys({**load_keys(), **keys})
        for k in ("claude_key", "openai_key", "api_key"):
            s.pop(k, None)
        save_settings(s)

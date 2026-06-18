"""
R Training Bot — Gradio 6 app.
Tabs: Profile · Chat · Progress
"""

import re
import tempfile
import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lessons import LESSONS, LESSON_TITLES
from data_manager import (
    profile_exists, load_profile, save_profile,
    load_progress, save_history,
    mark_lesson_complete, set_current_lesson, reset_progress,
    load_settings, save_settings,
)
from prompt_builder import build_system_prompt
from llm_router import chat as llm_chat


# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """
/* ── Header ── */
#app-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    border-radius: 14px;
    padding: 22px 28px 18px;
    margin-bottom: 10px;
}
#app-header h1 { color: #ffffff !important; font-size: 1.9em; margin: 0 0 4px; }
#app-header p  { color: #bfdbfe !important; margin: 0; font-size: 0.97em; }

/* ── Sidebar ── */
#chat-sidebar {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 6px 8px;
}

/* ── Buttons ── */
#mark-complete-btn {
    background: #16a34a !important;
    border-color: #15803d !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
}
#mark-complete-btn:hover { background: #15803d !important; }

#jump-btn {
    border-radius: 8px !important;
}

/* ── Progress stats bar ── */
#progress-stats {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border: 1px solid #bae6fd;
    border-radius: 12px;
    padding: 16px 22px;
    margin-bottom: 8px;
}

/* ── Profile tab ── */
#profile-header {
    background: #f0f7ff;
    border-radius: 10px;
    padding: 14px 20px;
    border-left: 4px solid #2563eb;
    margin-bottom: 12px;
}

/* ── Tab bar ── */
.tab-nav button { font-weight: 500 !important; font-size: 0.95em !important; }
"""

# ── Quick Reference ───────────────────────────────────────────────────────────

QUICK_REF_MD = """
| # | Topic | Key syntax |
|---|-------|-----------|
| 1 | Data structures | `x[1]` pos · `x[["n"]]` name · `x$col` df col |
| 2 | lapply | `lapply(list, fn)` ✓  `lapply(list, fn())` ✗ |
| 3 | Map | `Map(fn, list1, list2)` — two lists zipped |
| 4 | Scoping | `<-` local · `<<-` parent (avoid) · pass as args |
| 5 | Pipe | `x \|> f()` = `f(x)` · chain left-to-right |
| 6 | purrr | `map(l, ~fn(.x))` · `walk` side-effects · `map_dbl` typed |
| 7 | reduce | `reduce(dfs, bind_rows)` stacks all frames |
| 8 | dplyr | `filter` · `mutate` · `group_by \|> summarise` |
| 9 | across | `mutate(across(cols, ~fn(.x), .names="pfx_{.col}"))` |
| 10 | Joins | `left_join(x, y, by="id")` · `intersect(names(x), names(y))` |
| 11 | case_when | `case_when(cond ~ val, .default ~ other)` first match wins |
| 12 | stringr | `str_extract` · `str_detect` · `str_glue("{var}")` |
| 13 | regex | `\\\\d` digit · `\\\\w` word · `+` one+ · `{n}` exact · `^$` anchors |
| 14 | Functions | `f <- function(x, y=1) { stopifnot(...); ... }` |
| 15 | Production | Config-driven · `%\|\|%` null coalesce · `src(file)` |
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _extract_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(p.get("text", "") for p in content if isinstance(p, dict))
    return str(content)


def _build_welcome(progress: dict) -> str:
    lesson_id = progress.get("current_lesson", 1)
    title     = LESSON_TITLES.get(lesson_id, "the next lesson")
    completed = len(progress.get("completed", []))
    if completed == 0:
        return (
            "👋 Welcome to the **R Training Bot**.\n\n"
            "Start by filling in your **Profile** tab so the bot can adapt its teaching "
            "style to your background. Then come back here and type **start**.\n\n"
            "Or type **start** right away to begin from Lesson 1."
        )
    return (
        f"👋 Welcome back! You left off at **Lesson {lesson_id}: {title}**. "
        f"You've completed **{completed} of {len(LESSONS)}** lessons.\n\n"
        "Type **continue** to pick up where you left off, or use the lesson selector below."
    )


def _progress_stats_md(progress: dict) -> str:
    completed = len(progress.get("completed", []))
    current   = progress.get("current_lesson", 1)
    total     = len(LESSONS)
    pct       = int(completed / total * 100)
    title     = LESSON_TITLES.get(current, "—")
    return (
        f"### 📊 {pct}% complete — {completed} / {total} lessons\n\n"
        f"**Currently on:** Lesson {current} — {title}"
    )


def make_progress_figure(progress: dict):
    completed = set(progress.get("completed", []))
    current   = progress.get("current_lesson", 1)
    total     = len(LESSONS)
    done      = len(completed)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "bar"}]],
        column_widths=[0.32, 0.68],
        subplot_titles=["Overall", "Lesson status"],
    )

    # Donut — overall completion
    fig.add_trace(go.Pie(
        values=[done, total - done],
        labels=["Complete", "Remaining"],
        hole=0.68,
        marker=dict(
            colors=["#16a34a", "#e5e7eb"],
            line=dict(color="white", width=2),
        ),
        textinfo="none",
        hovertemplate="%{label}: %{value} lessons<extra></extra>",
    ), row=1, col=1)

    fig.add_annotation(
        text=f"<b>{done}/{total}</b><br><span style='font-size:11px'>lessons</span>",
        x=0.135, y=0.5,
        font=dict(size=20, color="#1e3a5f"),
        showarrow=False,
        xref="paper", yref="paper",
        align="center",
    )

    # Horizontal bars — per-lesson status
    labels, colors, opacities = [], [], []
    for l in LESSONS:
        labels.append(f"<b>L{l['id']}</b> {l['title'][:30]}")
        if l["id"] in completed:
            colors.append("#16a34a")
            opacities.append(1.0)
        elif l["id"] == current:
            colors.append("#2563eb")
            opacities.append(0.85)
        else:
            colors.append("#cbd5e1")
            opacities.append(0.6)

    fig.add_trace(go.Bar(
        x=[1.0 if l["id"] in completed else (0.55 if l["id"] == current else 0.25)
           for l in LESSONS],
        y=labels,
        orientation="h",
        marker=dict(color=colors, opacity=opacities, line=dict(width=0)),
        hovertemplate="%{y}<extra></extra>",
        showlegend=False,
    ), row=1, col=2)

    # Legend
    for color, label in [("#16a34a", "Complete"), ("#2563eb", "Current"), ("#cbd5e1", "Pending")]:
        fig.add_trace(go.Bar(
            x=[None], y=[None], orientation="h",
            marker=dict(color=color),
            name=label, showlegend=True,
        ))

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=20, t=40, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(
            orientation="h", x=0.35, y=-0.04,
            font=dict(size=11),
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=10.5),
            showgrid=False,
        ),
        xaxis=dict(showticklabels=False, range=[0, 1.15], showgrid=False),
        font=dict(family="Inter, system-ui, sans-serif"),
    )
    fig.update_annotations(font_size=12)
    return fig


# ── Chat logic ────────────────────────────────────────────────────────────────

def respond(user_message: str, history: list, api_key: str, model_choice: str) -> tuple:
    if not user_message.strip():
        return history, ""

    profile       = load_profile()
    system_prompt = build_system_prompt(profile)

    messages = [
        {"role": m["role"], "content": _extract_content(m["content"])}
        for m in history
    ]
    messages.append({"role": "user", "content": user_message})

    reply = llm_chat(
        messages,
        system_prompt=system_prompt,
        api_key=api_key.strip(),
        model_choice=model_choice,
    )

    # Auto-detect lesson completion from bot signal
    match = re.search(r"✅\s*[Ll]esson\s+(\d+)\s+complete", reply)
    if match:
        mark_lesson_complete(int(match.group(1)))

    history = history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": reply},
    ]
    save_history(history)
    return history, ""


def jump_to_lesson(lesson_label: str, history: list, api_key: str, model_choice: str) -> tuple:
    if not lesson_label:
        return history, ""

    lesson_id = int(lesson_label.split(".")[0])
    set_current_lesson(lesson_id)

    profile       = load_profile()
    system_prompt = build_system_prompt(profile)

    instruction = (
        f"Please start teaching Lesson {lesson_id}: {LESSON_TITLES[lesson_id]}. "
        "Begin with the mental model in 2–3 sentences, then a short example, "
        "then ask the quick-check question."
    )
    messages = [
        {"role": m["role"], "content": _extract_content(m["content"])}
        for m in history
    ]
    messages.append({"role": "user", "content": instruction})

    reply = llm_chat(messages, system_prompt=system_prompt,
                     api_key=api_key.strip(), model_choice=model_choice)

    history = history + [
        {"role": "user",      "content": f"*→ Jumped to Lesson {lesson_id}: {LESSON_TITLES[lesson_id]}*"},
        {"role": "assistant", "content": reply},
    ]
    save_history(history)
    return history, ""


def mark_current_complete() -> tuple:
    p         = load_progress()
    current   = p.get("current_lesson", 1)
    title     = LESSON_TITLES.get(current, "")
    next_id   = min(current + 1, len(LESSONS))
    mark_lesson_complete(current)
    new_p     = load_progress()
    status    = f"✅ Lesson {current}: *{title}* marked complete. Now on Lesson {next_id}."
    return (
        status,
        _progress_stats_md(new_p),
        make_progress_figure(new_p),
    )


def clear_chat() -> tuple:
    progress = load_progress()
    return [{"role": "assistant", "content": _build_welcome(progress)}], ""


def export_chat(history: list) -> str:
    lines = ["# R Training Bot — Session Export\n\n"]
    for msg in history:
        role    = "**You**" if msg["role"] == "user" else "**Tutor**"
        content = _extract_content(msg["content"])
        lines.append(f"{role}:\n\n{content}\n\n---\n\n")
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False,
        prefix="r_training_", encoding="utf-8",
    )
    tmp.write("".join(lines))
    tmp.close()
    return tmp.name


# ── Onboarding ────────────────────────────────────────────────────────────────

def save_onboarding(
    knows_vba, level_vba,
    knows_python, level_python,
    knows_stata, level_stata,
    knows_excel, level_excel,
    use_case: str,
) -> str:
    languages = []
    if knows_vba:    languages.append({"name": "VBA",    "level": level_vba})
    if knows_python: languages.append({"name": "Python", "level": level_python})
    if knows_stata:  languages.append({"name": "Stata",  "level": level_stata})
    if knows_excel:  languages.append({"name": "Excel",  "level": level_excel})

    save_profile({"languages": languages, "use_case": use_case})
    langs_str = ", ".join(l["name"] for l in languages) or "none specified"
    return (
        f"✅ Profile saved — languages: **{langs_str}**. "
        "Switch to the **Chat** tab to start learning."
    )


# ── API key persistence ───────────────────────────────────────────────────────

def on_api_key_change(api_key: str, remember: bool) -> None:
    if remember:
        settings = load_settings()
        settings["api_key"]      = api_key
        settings["model_choice"] = ""
        save_settings(settings)


def on_remember_change(remember: bool, api_key: str) -> None:
    settings = load_settings()
    if remember:
        settings["api_key"] = api_key
    else:
        settings.pop("api_key", None)
    save_settings(settings)


# ── Startup state ─────────────────────────────────────────────────────────────

_progress = load_progress()
_settings = load_settings()
_profile  = load_profile()
_existing_langs = {l["name"]: l["level"] for l in _profile.get("languages", [])}
LEVELS = ["Beginner", "Intermediate", "Advanced"]
LESSON_CHOICES = [f"{l['id']}. {l['title']}" for l in LESSONS]


# ── Build UI ──────────────────────────────────────────────────────────────────

with gr.Blocks(css=CSS, title="R Training Bot") as demo:

    # Header
    with gr.Group(elem_id="app-header"):
        gr.Markdown(
            "# R Training Bot\n"
            "Learn idiomatic R — one concept at a time, adapted to your background."
        )

    with gr.Tabs() as tabs:

        # ────────────────────────────────────────────────────────────────────
        # TAB 1 — PROFILE
        # ────────────────────────────────────────────────────────────────────
        with gr.Tab("👤 Profile"):

            with gr.Group(elem_id="profile-header"):
                gr.Markdown(
                    "Tell the bot your programming background. "
                    "It will adapt analogies, examples, and explanations to what you already know."
                )

            gr.Markdown("### Languages you know")

            with gr.Row():
                with gr.Column(scale=1):
                    knows_vba = gr.Checkbox(
                        label="VBA", value="VBA" in _existing_langs)
                    level_vba = gr.Radio(
                        LEVELS, value=_existing_langs.get("VBA", "Intermediate"),
                        label="Level", visible="VBA" in _existing_langs)
                with gr.Column(scale=1):
                    knows_python = gr.Checkbox(
                        label="Python", value="Python" in _existing_langs)
                    level_python = gr.Radio(
                        LEVELS, value=_existing_langs.get("Python", "Intermediate"),
                        label="Level", visible="Python" in _existing_langs)
                with gr.Column(scale=1):
                    knows_stata = gr.Checkbox(
                        label="Stata", value="Stata" in _existing_langs)
                    level_stata = gr.Radio(
                        LEVELS, value=_existing_langs.get("Stata", "Intermediate"),
                        label="Level", visible="Stata" in _existing_langs)
                with gr.Column(scale=1):
                    knows_excel = gr.Checkbox(
                        label="Excel", value="Excel" in _existing_langs)
                    level_excel = gr.Radio(
                        LEVELS, value=_existing_langs.get("Excel", "Intermediate"),
                        label="Level", visible="Excel" in _existing_langs)

            knows_vba.change(   lambda x: gr.Radio(visible=x), knows_vba,    level_vba)
            knows_python.change(lambda x: gr.Radio(visible=x), knows_python, level_python)
            knows_stata.change( lambda x: gr.Radio(visible=x), knows_stata,  level_stata)
            knows_excel.change( lambda x: gr.Radio(visible=x), knows_excel,  level_excel)

            gr.Markdown("### What do you mainly use R for?")
            use_case = gr.Textbox(
                value=_profile.get("use_case", ""),
                placeholder="e.g. cleaning school enrolment data, building reproducible pipelines...",
                lines=2, label="",
            )

            with gr.Row():
                save_btn    = gr.Button("Save profile", variant="primary", scale=1)
                save_status = gr.Markdown("", scale=3)

            save_btn.click(
                save_onboarding,
                inputs=[
                    knows_vba, level_vba,
                    knows_python, level_python,
                    knows_stata, level_stata,
                    knows_excel, level_excel,
                    use_case,
                ],
                outputs=save_status,
            )

        # ────────────────────────────────────────────────────────────────────
        # TAB 2 — CHAT
        # ────────────────────────────────────────────────────────────────────
        with gr.Tab("💬 Chat"):

            with gr.Row():

                # Sidebar
                with gr.Column(scale=1, elem_id="chat-sidebar"):

                    gr.Markdown("#### Model")
                    model_choice = gr.Radio(
                        choices=["auto", "ollama", "claude", "openai"],
                        value=_settings.get("model_choice", "auto"),
                        label="", info="auto detects from key prefix",
                    )
                    api_key = gr.Textbox(
                        label="API key",
                        value=_settings.get("api_key", ""),
                        placeholder="sk-ant-... Claude · sk-... OpenAI · empty = Ollama",
                        type="password", lines=1,
                    )
                    remember_key = gr.Checkbox(
                        label="Remember key on this device",
                        value="api_key" in _settings,
                    )
                    api_key.change(on_api_key_change,
                                   inputs=[api_key, remember_key])
                    remember_key.change(on_remember_change,
                                        inputs=[remember_key, api_key])

                    gr.Markdown("---")
                    gr.Markdown("#### Lesson")
                    lesson_selector = gr.Dropdown(
                        choices=LESSON_CHOICES, label="Jump to",
                        value=None, allow_custom_value=False,
                    )
                    jump_btn = gr.Button("Go →", elem_id="jump-btn", variant="secondary")

                    gr.Markdown("---")
                    gr.Markdown("#### Progress")
                    mark_btn    = gr.Button(
                        "✓ Mark lesson complete",
                        elem_id="mark-complete-btn",
                        variant="primary",
                    )
                    mark_status = gr.Markdown("")
                    clear_btn   = gr.Button("Clear chat", variant="secondary")

                    gr.Markdown("---")
                    with gr.Accordion("📋 Quick Reference", open=False):
                        gr.Markdown(QUICK_REF_MD)

                    gr.Markdown("---")
                    export_btn  = gr.Button("⬇ Export chat (.md)", variant="secondary")
                    export_file = gr.File(label="Download", visible=False)

                # Chat area
                with gr.Column(scale=3):
                    saved_history = _progress.get("history", [])
                    initial_history = saved_history if saved_history else [
                        {"role": "assistant", "content": _build_welcome(_progress)}
                    ]
                    chatbot = gr.Chatbot(
                        value=initial_history,
                        label="R Tutor",
                        height=530,
                        layout="bubble",
                    )
                    with gr.Row():
                        user_input = gr.Textbox(
                            placeholder="Type here and press Enter...",
                            label="", lines=2, scale=5,
                        )
                        send_btn = gr.Button("Send ➤", variant="primary", scale=1)

            # Wire chat
            send_btn.click(
                respond,
                inputs=[user_input, chatbot, api_key, model_choice],
                outputs=[chatbot, user_input],
            )
            user_input.submit(
                respond,
                inputs=[user_input, chatbot, api_key, model_choice],
                outputs=[chatbot, user_input],
            )
            clear_btn.click(clear_chat, outputs=[chatbot, user_input])
            jump_btn.click(
                jump_to_lesson,
                inputs=[lesson_selector, chatbot, api_key, model_choice],
                outputs=[chatbot, user_input],
            )

            # Mark complete — updates status label AND progress tab
            progress_stats_chat = gr.Markdown(_progress_stats_md(_progress))  # hidden sync target
            mark_btn.click(
                mark_current_complete,
                outputs=[mark_status, progress_stats_chat, gr.Plot(visible=False)],
            )

            # Export
            export_btn.click(
                export_chat,
                inputs=[chatbot],
                outputs=export_file,
            )
            export_btn.click(lambda: gr.File(visible=True), outputs=export_file)

        # ────────────────────────────────────────────────────────────────────
        # TAB 3 — PROGRESS
        # ────────────────────────────────────────────────────────────────────
        with gr.Tab("📈 Progress") as progress_tab:

            progress_stats = gr.Markdown(
                _progress_stats_md(_progress),
                elem_id="progress-stats",
            )
            progress_plot = gr.Plot(
                value=make_progress_figure(_progress),
                label="",
            )

            with gr.Row():
                refresh_btn = gr.Button("Refresh", variant="secondary")
                reset_btn   = gr.Button("Reset all progress", variant="stop")

            reset_status = gr.Markdown("")

            def refresh_progress():
                p = load_progress()
                return _progress_stats_md(p), make_progress_figure(p)

            def do_reset():
                reset_progress()
                p = load_progress()
                return _progress_stats_md(p), make_progress_figure(p), "Progress reset."

            progress_tab.select(
                refresh_progress,
                outputs=[progress_stats, progress_plot],
            )
            refresh_btn.click(
                refresh_progress,
                outputs=[progress_stats, progress_plot],
            )
            reset_btn.click(
                do_reset,
                outputs=[progress_stats, progress_plot, reset_status],
            )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Soft(),
    )

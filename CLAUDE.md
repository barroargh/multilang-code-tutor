# Multi-Language Code Tutor — Claude Code context

## What this project is
A conversational coding tutor that teaches **R, Python, Stata, and VBA** (it started out
R-only). FastAPI backend (`server.py`) + single-page HTML/CSS/JS frontend
(`static/index.html`). Runs locally at http://127.0.0.1:7860.

```
python server.py
```

## Architecture at a glance
| File | Role |
|------|------|
| `server.py` | FastAPI — all API endpoints; threads the selected target language through everything |
| `static/index.html` | Entire frontend (one file); includes the sidebar language picker |
| `llm_router.py` | Routes to Claude / OpenAI / Ollama; has empty-key guards |
| `lessons.py` | `CURRICULA[language]` lesson lists, `GOALS` milestones, `READY_LANGUAGES` — content source of truth |
| `curriculum.py` | Declared level in the target language → per-lesson treatment (full / fast / optional) |
| `prompt_builder.py` | System prompt: depth + treatment + background; injects `{{LANGUAGE}}` + lesson sequence into `system_prompt.md` |
| `data_manager.py` | Reads/writes `user_data/*.json`; progress & history are PER LANGUAGE |
| `system_prompt.md` | Language-agnostic teaching template (placeholders + multi-beat arc rules) |

## Languages & curricula
Target language is stored in `settings.json` (`target_language`, default `R`) and chosen via `GET/POST /api/language`. Only languages in `lessons.READY_LANGUAGES` are selectable; others show "(soon)" in the picker.
- Lessons sized to each language, not a fixed count: **R 30 · Python 30 · Stata 24 · VBA 20**
- Goal milestones (Core / Extended / Full) are per-language in `lessons.GOALS`; the goal clamp and frontend buttons follow the current curriculum's length.

## Lesson arc (multi-beat)
Each lesson = N beats (explanation + exercise) → integration exercise → ✅ Lesson N complete.
- Fast: 1 beat + integration · Standard: 2 + integration · Deep: 3 + integration

`✅ Lesson N complete` emitted by LLM → detected by regex in `server.py` → `mark_lesson_complete(lang, N)`.

## Adaptive curriculum
Declared level in the *target* language (Profile tab) → `curriculum.plan_for(profile, lang)` tags each lesson `full` / `fast` / `optional` (fast = one refresher beat + check; optional = offer to skip). Knowing *other* languages drives analogies (in `prompt_builder`), not which lessons are needed.

## Key decisions (do not revert)
- Navigation is **permissive**: "next", "skip", "continue" advance immediately — no hard gates
- Integration exercise is the **only** gate for lesson completion
- Adaptive treatment never hard-gates — fast/optional still let the student proceed or skip
- Progress & chat history are **per target language** — switching never clobbers another language (old flat progress.json migrates to `{"R": {...}}` on read)
- `llm_router.py` returns a friendly error string (not a crash) when API key is missing

## Adding a language
Add `CURRICULA["X"]` + `GOALS["X"]` in `lessons.py`, then add `"X"` to `READY_LANGUAGES`. The engine, picker, progress, prompt, and goals are all language-agnostic — no other changes needed.

## Git
- Repo: `barroargh/multilang-code-tutor`, default branch `main`
- Keep branches short-lived: branch off `main` → PR → merge → delete

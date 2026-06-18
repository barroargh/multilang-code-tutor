# R Training Bot — Claude Code context

## What this project is
A conversational R tutor. FastAPI backend (`server.py`) + single-page HTML/CSS/JS frontend (`static/index.html`). Runs locally at http://127.0.0.1:7860.

```
python server.py
```

## Architecture at a glance
| File | Role |
|------|------|
| `server.py` | FastAPI — all API endpoints |
| `static/index.html` | Entire frontend (one file) |
| `llm_router.py` | Routes to Claude / OpenAI / Ollama; has empty-key guards |
| `prompt_builder.py` | Builds system prompt: depth note + user background + base prompt |
| `data_manager.py` | Reads/writes `user_data/*.json` |
| `lessons.py` | 30-lesson curriculum — single source of truth |
| `system_prompt.md` | Base tutor instructions (lesson sequence + multi-beat arc rules) |

## Curriculum
30 lessons across 7 tiers. T1 (1–15): Core R fundamentals. T2 (16–18): Tidy data. T3 (19–20): ggplot2. T4 (21–23): File I/O + labelled data + missing data. T5 (24–25): Defensive programming. T6 (26–27): Reporting + modelling. T7 (28–30): Production R.

## Lesson arc (multi-beat)
Each lesson = N beats (explanation + exercise) → integration exercise → ✅ Lesson N complete.
- Fast: 1 beat + integration
- Standard: 2 beats + integration
- Deep: 3 beats + integration

`✅ Lesson N complete` emitted by LLM → detected by regex in `server.py` → `mark_lesson_complete(N)`.

## Key decisions (do not revert)
- Navigation is **permissive**: "next", "skip", "continue" advance immediately — no hard gates
- Integration exercise is the **only** gate for lesson completion
- `llm_router.py` returns a friendly error string (not a crash) when API key is missing

## Git
- Repo: `barroargh/personal_work`, branch `main`
- Keep branches short-lived: branch off `main` → PR → merge → delete
- Always commit before switching to villa-bruno work (different project, same repo)



# R Training Bot

A conversational R tutor that teaches idiomatic R — functional programming, dplyr,
joins, stringr, regex and more — one concept at a time, with real data examples and a
30-lesson curriculum across 7 tiers.

Features:
- Adapts teaching style to your background (VBA, Python, Stata, Excel)
- Tracks progress across sessions — resumes where you left off
- Inline lesson plan in the sidebar — click any lesson to jump there
- Learning pace picker: Fast / Standard / Deep
- Learning plan: set your goal (Core 15 / Extended 22 / Full 30), sessions per week, get an ETA
- Theme picker: Default / Dark / Teal / Violet
- Works with Ollama (free, local), Claude API, or OpenAI API

---

## Option A — Standalone .exe (no Python required)

Recommended for sharing with colleagues who don't have Python.

### Step 1 — Build the exe (once, on your machine)

```bash
pip install -r requirements.txt
python build.py
```

This creates `dist/R_Training_Bot.exe`.

### Step 2 — Share the exe

Copy `dist/R_Training_Bot.exe` to any Windows machine. No installation needed.

### Step 3 — Set up a model (on each machine)

**Ollama (free, no API key)**

1. Download and install Ollama from [ollama.com](https://ollama.com)
2. Pull a model once:
   ```bash
   ollama pull llama3.2
   ```
3. Ollama runs in the background automatically.

**Claude or OpenAI API key**

No local install needed. Paste your key in the app's Settings tab.
Keys are not stored unless you tick "Remember key".

### Step 4 — Run

Double-click `R_Training_Bot.exe`. The browser opens automatically at
`http://127.0.0.1:7860`.

---

## Option B — Run from source (Python required)

Use this to develop or customise the app.

### Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Run

```bash
python server.py
```

Or double-click `launch.bat`.

The browser opens automatically at [http://127.0.0.1:7860](http://127.0.0.1:7860).

---

## Using the app

### First launch — Profile tab

Set your programming background (VBA, Python, Stata, Excel) and your main use of R.
The bot adapts its teaching style, analogies, and examples to match.

### Settings tab

- **Model** — choose Claude / OpenAI / Ollama or enter a custom model name. Paste your
  API key and optionally tick "Remember key" to persist it across sessions.
- **Learning Plan** — pick your goal (Core 15 / Extended 22 / Full 30 lessons), set
  sessions per week, and see an estimated completion date.
- **Learning Pace** — Fast (quick pass, one example), Standard (default rhythm), or
  Deep (two exercises + real-data challenge per lesson).
- **Appearance** — four colour themes (Default, Dark, Teal, Violet).

### Chat tab

- Type **start** to begin from Lesson 1
- Type **continue** or **next** to resume or advance lessons
- Say **lesson 12** or any lesson name to jump directly
- Use the sidebar lesson plan to click into any lesson

### Sidebar

The lesson plan shows your full curriculum with completion status (✓ done, ▶ current,
○ upcoming). Lessons beyond your goal are shown faded. Click any row to jump there.

### Progress

Progress is tracked automatically as the tutor emits ✅ Lesson N complete.
Use **Reset** in the sidebar to start from scratch.

### Export / Compact

- **Export** downloads the current chat as a Markdown file.
- **Compact** asks the tutor to write a brief session handover note and prepends it to
  the history — keeps context short without losing continuity.

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | FastAPI backend — chat, progress, profile, settings endpoints |
| `static/index.html` | Single-page HTML/CSS/JS frontend |
| `llm_router.py` | Routes messages to Claude / OpenAI / Ollama |
| `prompt_builder.py` | Builds system prompt from base + user profile + depth setting |
| `data_manager.py` | Reads/writes profile, progress, history, settings to disk |
| `lessons.py` | 30-lesson curriculum — edit here to change content |
| `system_prompt.md` | Base teaching instructions for the tutor |
| `build.py` | PyInstaller build script |
| `launch.bat` | Windows double-click launcher (source mode) |
| `requirements.txt` | Python dependencies |

User data (profile, progress, chat history, settings) is stored in `user_data/` next
to the exe or script. Delete this folder to reset everything.

---

## Curriculum overview

| Tier | Lessons | Topics |
|------|---------|--------|
| T1 — Core fundamentals | 1–15 | Vectors, lapply, purrr, dplyr, joins, stringr, regex, functions |
| T2 — Tidy data | 16–18 | tidyr, lubridate, forcats |
| T3 — Visualisation | 19–20 | ggplot2 foundations, facets & scales |
| T4 — Data access & quality | 21–23 | File I/O, labelled survey data, missing data |
| T5 — Defensive programming | 24–25 | tryCatch, project structure & renv |
| T6 — Reporting & modelling | 26–27 | Quarto / R Markdown, lm / glm / broom |
| T7 — Production R | 28–30 | Validation, writing packages, performance & data.table |

---

## Security note

API keys sent to the model provider (Anthropic / OpenAI) are passed directly from the
browser and are **never stored by default**. If you tick "Remember key" in Settings,
the key is written to `user_data/settings.json` on disk — only do this on a personal
machine. Do not deploy this app on a public server.

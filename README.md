# R Training Bot

A conversational R tutor that teaches idiomatic R — functional programming, dplyr,
joins, stringr, regex and more — one concept at a time, with real data examples and a
30-lesson curriculum across 7 tiers.

Features:
- Adapts teaching style to your background (Python, VBA, R, Excel, Stata)
- Adapts the lesson plan to your declared **R** level — fast-tracks or marks optional the lessons you likely already know
- Tracks progress across sessions — resumes where you left off
- Inline lesson plan in the sidebar — click any lesson to jump there
- Learning pace picker: Fast / Standard / Deep
- Learning plan: set your goal (Core 15 / Extended 22 / Full 30), sessions per week, get an ETA
- Theme picker: Default / Dark / Teal / Violet
- Works with Ollama (free, local), Claude API, or OpenAI API

---

## Option A — Standalone app (no Python required)

For sharing with colleagues: they download **one file** and run it — no Python, no `pip`.
The Python interpreter and all dependencies are bundled inside the build.

### Step 1 — Get the build

**Download from Releases (recommended).** Grab the latest from the
[Releases page](https://github.com/barroargh/R_Tutorial_Bot/releases):

- Windows → `R_Training_Bot-Windows.exe`
- macOS → `R_Training_Bot-macOS.zip`

These are built automatically by GitHub Actions (`.github/workflows/build.yml`). To cut a
new release, push a version tag — CI builds both platforms and attaches them:

```bash
git tag v1.0.0
git push origin v1.0.0
```

**Or build it yourself** (one-time, needs Python on *your* machine only):

```bash
pip install -r requirements.txt
python build.py
```

→ `dist/R_Training_Bot.exe` (Windows) or `dist/R_Training_Bot` (macOS).

### Step 2 — Set up a model (on each machine)

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

### Step 3 — Run

- **Windows:** double-click `R_Training_Bot.exe`. If SmartScreen warns about an unknown
  publisher, click **More info → Run anyway** (the build is unsigned).
- **macOS:** unzip, then **right-click `R_Training_Bot` → Open** the first time to clear
  Gatekeeper (the build is unsigned/unnotarized).

The browser opens automatically at `http://127.0.0.1:7860`.

> These builds target **personal** laptops. On managed/corporate machines, IT
> application-allowlisting may block unsigned apps regardless of admin rights.

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

**First run:** open the **Profile** tab, tick the languages you know — Python, VBA, R,
Excel, Stata — set a level for each, and describe what you use R for. Your **R** level
reshapes the lesson plan; the others tune the analogies and examples. Then switch to the
**Chat** tab and type `start`.

### Sidebar (always visible)

Shows the current lesson and progress bar, the full **lesson plan** (✓ done · ▶ current ·
○ upcoming, with `fast-track` / `optional` badges and a "Suggested start" hint based on
your R level — click any row to jump), the **model** picker, and **Mark lesson complete**
/ **Export chat** buttons.

### Tabs

- **Chat** — talk to the tutor. Type `start`, `next` / `continue` to advance, `skip` to
  move on, or `lesson 12` / a lesson name to jump. The strip below shows token usage, the
  active model, **Compact**, and **Clear**.
- **Progress** — completion stats and charts; **Reset all progress** lives here.
- **Profile** — your languages, R level, and use-case. Editable any time — saving
  refreshes the plan live.
- **Settings** — model + API key ("Remember key" to persist), **Learning Plan** (goal
  Core 15 / Extended 22 / Full 30 · sessions per week · ETA), **Learning Pace** (Fast /
  Standard / Deep), and **Appearance** themes.
- **Help** — full command reference.

Progress saves automatically when the tutor emits `✅ Lesson N complete`. **Export**
downloads the chat as Markdown; **Compact** swaps the history for a short handover note,
keeping the context window small without losing continuity.

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | FastAPI backend — chat, progress, profile, settings endpoints |
| `static/index.html` | Single-page HTML/CSS/JS frontend |
| `llm_router.py` | Routes messages to Claude / OpenAI / Ollama |
| `prompt_builder.py` | Builds system prompt from base + profile + depth + per-lesson treatment |
| `curriculum.py` | Maps your R level to a per-lesson plan (full / fast-track / optional) |
| `data_manager.py` | Reads/writes profile, progress, history, settings to disk |
| `lessons.py` | 30-lesson curriculum (titles, descriptions, difficulty level) — edit to change content |
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

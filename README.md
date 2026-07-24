# Multi-Language Code Tutor

A conversational coding tutor that teaches **idiomatic R, Python, Stata, and VBA** — one
concept at a time, with real data examples and a curriculum tailored to each language. Pick
the language you want to learn; the bot adapts the lesson plan and its explanations to the
languages you already know.

> It began as an R-only tutor (hence the name) and now teaches four languages.

Features:
- **Four languages to learn:** R (30 lessons), Python (30), Stata (24), VBA (20) — switch any time from the sidebar
- Adapts teaching style to your background — draws analogies from the languages you already know (R / Python / Stata / VBA / Excel)
- Adapts the lesson plan to your declared level in the language you're learning — fast-tracks or marks optional the lessons you likely already know
- Per-language progress & chat history — switching languages never loses your place
- Inline lesson plan in the sidebar — click any lesson to jump there
- Learning pace picker: Fast / Standard / Deep
- Learning plan: goal milestones sized to each curriculum (Core / Extended / Full), sessions per week, ETA
- Theme picker: Default / Dark / Teal / Violet
- Works with Ollama (free, local), Claude API, or OpenAI API

---

## Option A — Build a standalone executable

Bundle the app into a single file (the Python interpreter and all dependencies are packed
inside). You need Python for this build step.

### Step 1 — Build it

```bash
pip install -r requirements.txt
python build.py
```

→ `dist/multilang-code-tutor.exe` (Windows) or `dist/multilang-code-tutor` (macOS). Build on the OS
you're targeting — a Windows `.exe` must be built on Windows, a macOS binary on a Mac.

### Step 2 — Set up a model

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

- **Windows:** double-click `dist\multilang-code-tutor.exe`.
- **macOS:** it's a Unix binary (not a `.app`) — run it from Terminal: `./dist/multilang-code-tutor`.

The browser opens automatically at `http://127.0.0.1:7860`.

> A build you compile yourself runs fine. But the same file **copied or downloaded from
> another machine** is treated as untrusted — Windows SmartScreen / Smart App Control and
> macOS Gatekeeper block unsigned apps. So this isn't a clean way to hand the app to people
> who don't have Python; that needs code signing (or hosting it as a web app). If a
> colleague already has Python, the simplest path is **Option B** below.

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
(Set the `PORT` env var to use a different port.)

---

## Using the app

**First run:** in the sidebar, pick the **language you want to learn** (R / Python / Stata /
VBA). Then open the **Profile** tab, tick the languages you already know — R, Python, Stata,
VBA, Excel — set a level for each, and describe what you use the language for. Your declared
level in the *target* language reshapes the lesson plan; the others tune the analogies and
examples. Switch to the **Chat** tab and type `start`.

### Sidebar (always visible)

- **Language picker** — choose what to learn; switching loads that language's plan, progress, and chat.
- Current lesson and progress bar.
- The full **lesson plan** (✓ done · ▶ current · ○ upcoming), with `fast-track` / `optional` badges and a "Suggested start" hint based on your declared level — click any row to jump.
- The **model** picker, and **Mark lesson complete** / **Export chat** buttons.

### Tabs

- **Chat** — talk to the tutor. Type `start`, `next` / `continue` to advance, `skip` to move on, or `lesson 12` / a lesson name to jump. The strip below shows token usage, the active model, **Compact**, and **Clear**.
- **Progress** — completion stats and charts; **Reset all progress** (resets only the current language) lives here.
- **Profile** — the languages you know and your use-case. Editable any time — saving refreshes the plan live.
- **Settings** — model + API key ("Remember key" to persist), **Learning Plan** (goal milestones for the current language · sessions per week · ETA), **Learning Pace** (Fast / Standard / Deep), and **Appearance** themes.
- **Help** — full command reference.

A lesson is marked complete only when you pass its integration exercise or click **Mark complete** — getting an exercise wrong, or skipping, leaves it *in progress* (blue), not done (green). Progress saves automatically. **Export** downloads the chat as Markdown; **Compact** swaps the history for a short handover note, keeping the context window small without losing continuity.

### Adding or editing a curriculum

Each language's lessons live in `lessons.py` under `CURRICULA[<language>]`. To add a language: add its lesson list and a `GOALS` entry, then include it in `READY_LANGUAGES`. Languages not in `READY_LANGUAGES` appear in the picker as "(soon)" and can't be selected. No engine/frontend changes are needed — everything is language-agnostic.

---

## Files

| File | Purpose |
|------|---------|
| `server.py` | FastAPI backend — chat, progress, profile, settings, language endpoints; threads the target language through everything |
| `static/index.html` | Single-page HTML/CSS/JS frontend (includes the sidebar language picker) |
| `llm_router.py` | Routes messages to Claude / OpenAI / Ollama |
| `lessons.py` | All curricula (`CURRICULA[language]`), `GOALS` milestones, `READY_LANGUAGES` — the content source of truth |
| `curriculum.py` | Maps your declared level in the target language to a per-lesson plan (full / fast-track / optional) |
| `prompt_builder.py` | Builds the system prompt: depth + treatment + background, injecting the language and its lesson sequence into the base template |
| `data_manager.py` | Reads/writes the tidy `user_data/` layout — profile, settings, keys, and per-language progress/history |
| `system_prompt.md` | Language-agnostic teaching template (`{{LANGUAGE}}` + `{{LESSON_SEQUENCE}}` placeholders) |
| `build.py` | PyInstaller build script |
| `launch.bat` | Windows double-click launcher (source mode) |
| `requirements.txt` | Python dependencies |

All persisted data lives in `user_data/` next to the exe or script, organised for easy inspection:

```
user_data/
  profile.json          # languages you know + your use-case
  settings.json         # preferences (model, depth, goal, target language)
  keys.json             # API keys — kept separate from preferences, only if "Remember key"
  progress/<lang>.json  # { current_lesson, completed } — one small file per language
  history/<lang>.json   # the chat transcript for that language
```

Delete the folder to reset everything. Upgrading from an older version migrates the old
flat files automatically (keeping a `progress.json.bak` backup).

---

## Curricula

Each language is sized to its own idiomatic surface area (quality over a fixed count):

| Language | Lessons | Shape |
|----------|---------|-------|
| **R** | 30 | Core fundamentals → tidyverse (dplyr / purrr / tidyr / stringr) → ggplot2 → I/O & labelled data → defensive programming → reporting & modelling → production |
| **Python** | 30 | Pythonic fundamentals → functions & iteration → data modelling & errors → pandas → NumPy & dates → viz & notebooks → files, packaging & testing |
| **Stata** | 24 | One-dataset model → data manipulation → by-group / reshape / merge → programming (macros, loops, do-files) → analysis & reporting |
| **VBA** | 20 | Editor & object model → worksheet work → idioms & robustness (arrays, performance, errors) → automating (workbooks, events, files) |

Goal milestones (Core / Extended / Full) are defined per language in `lessons.py`.

---

## Security note

API keys sent to the model provider (Anthropic / OpenAI) are passed directly from the
browser and are **never stored by default**. If you tick "Remember key" in Settings,
the key is written to `user_data/settings.json` on disk — only do this on a personal
machine. Do not deploy this app on a public server.

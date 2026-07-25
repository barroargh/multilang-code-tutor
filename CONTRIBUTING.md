# Contributing

Thanks for taking a look. This is a small project and contributions are welcome — whether that's a fix, a new lesson, or a whole new language.

## Running it locally

```bash
pip install -r requirements.txt
python server.py
```

It opens at http://127.0.0.1:7860. There is no build step and no CI, so please test your change by running the app and clicking through the part you touched.

## Opening a pull request

1. Fork the repo and create a branch off `main` (for example `fix/typo` or `feat/julia-curriculum`).
2. Make your change. Keep it focused on one thing so it is easy to review.
3. Open a pull request against `main`, describing what you changed and why.

Every pull request is reviewed before it is merged, so nothing lands on `main` without a look first.

## Where things live

| File | What it holds |
|------|----------------|
| `server.py` | FastAPI backend and API endpoints |
| `static/index.html` | The entire frontend (one file) |
| `lessons.py` | Every curriculum, the goal milestones, and the list of ready languages |
| `curriculum.py` | Turns a declared level into a per-lesson plan |
| `prompt_builder.py` | Builds the system prompt from the template |
| `data_manager.py` | Reads and writes everything under `user_data/` |
| `system_prompt.md` | The language-agnostic teaching template |

## Adding a language

Most content contributions are new languages or new lessons. To add a language:

1. Add its lesson list as `CURRICULA["YourLanguage"]` in `lessons.py`.
2. Add a matching `GOALS["YourLanguage"]` entry.
3. Add the name to `READY_LANGUAGES`.

The engine, picker, progress, prompt, and goals are all language-agnostic, so nothing else needs to change. A language that is not in `READY_LANGUAGES` shows in the picker as "(soon)" and cannot be selected yet.

## Style

Match the code around you. The frontend is deliberately one plain HTML file with no framework or build tooling — please keep it that way.

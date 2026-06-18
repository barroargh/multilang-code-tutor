"""
Handles reading and writing user profile, progress, and settings to disk.

Files stored in user_data/ next to the exe (or script).
Created automatically on first run.
"""

import json
import sys
from pathlib import Path


def _user_data_dir() -> Path:
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent
    d = base / "user_data"
    d.mkdir(exist_ok=True)
    return d


# ── Profile ───────────────────────────────────────────────────────────────────

def profile_exists() -> bool:
    return (_user_data_dir() / "profile.json").exists()


def load_profile() -> dict:
    path = _user_data_dir() / "profile.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_profile(profile: dict) -> None:
    (_user_data_dir() / "profile.json").write_text(
        json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ── Progress ──────────────────────────────────────────────────────────────────

def load_progress() -> dict:
    path = _user_data_dir() / "progress.json"
    if not path.exists():
        return {"current_lesson": 1, "completed": [], "history": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_progress(progress: dict) -> None:
    (_user_data_dir() / "progress.json").write_text(
        json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def mark_lesson_complete(lesson_id: int) -> None:
    p = load_progress()
    if lesson_id not in p["completed"]:
        p["completed"].append(lesson_id)
    p["current_lesson"] = lesson_id + 1
    save_progress(p)


def set_current_lesson(lesson_id: int) -> None:
    p = load_progress()
    p["current_lesson"] = lesson_id
    save_progress(p)


def save_history(history: list) -> None:
    p = load_progress()
    p["history"] = history[-80:]
    save_progress(p)


def clear_history() -> None:
    p = load_progress()
    p["history"] = []
    save_progress(p)


def reset_progress() -> None:
    path = _user_data_dir() / "progress.json"
    if path.exists():
        path.unlink()


# ── Settings (API key, preferences) ──────────────────────────────────────────

def load_settings() -> dict:
    path = _user_data_dir() / "settings.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_settings(settings: dict) -> None:
    (_user_data_dir() / "settings.json").write_text(
        json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8"
    )

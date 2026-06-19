"""
Handles reading and writing user profile, progress, and settings to disk.

Files stored in user_data/ next to the exe (or script). Created automatically on
first run.

Profile and settings are global (shared across all languages). Progress and chat
history are tracked PER TARGET LANGUAGE — progress.json maps a language to its
{current_lesson, completed, history}, so switching what you're learning never
clobbers another language's progress.
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


# ── Progress (per target language) ─────────────────────────────────────────────

def _empty_progress() -> dict:
    return {"current_lesson": 1, "completed": [], "history": []}


def _progress_path() -> Path:
    return _user_data_dir() / "progress.json"


def _load_all_progress() -> dict:
    """All languages' progress. Migrates the old flat (R-only) shape on read."""
    path = _progress_path()
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    # Migration: a pre-multi-language file has these keys at the top level.
    if any(k in data for k in ("current_lesson", "completed", "history")):
        data = {"R": {
            "current_lesson": data.get("current_lesson", 1),
            "completed":      data.get("completed", []),
            "history":        data.get("history", []),
        }}
        _write_all_progress(data)
    return data


def _write_all_progress(data: dict) -> None:
    _progress_path().write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def load_progress(language: str) -> dict:
    return _load_all_progress().get(language) or _empty_progress()


def save_progress(language: str, progress: dict) -> None:
    data = _load_all_progress()
    data[language] = progress
    _write_all_progress(data)


def mark_lesson_complete(language: str, lesson_id: int) -> None:
    p = load_progress(language)
    if lesson_id not in p["completed"]:
        p["completed"].append(lesson_id)
    p["current_lesson"] = lesson_id + 1
    save_progress(language, p)


def set_current_lesson(language: str, lesson_id: int) -> None:
    p = load_progress(language)
    p["current_lesson"] = lesson_id
    save_progress(language, p)


def save_history(language: str, history: list) -> None:
    p = load_progress(language)
    p["history"] = history[-80:]
    save_progress(language, p)


def clear_history(language: str) -> None:
    p = load_progress(language)
    p["history"] = []
    save_progress(language, p)


def reset_progress(language: str) -> None:
    """Reset just this language's progress; other languages are untouched."""
    data = _load_all_progress()
    data.pop(language, None)
    _write_all_progress(data)


# ── Settings (API key, preferences, target language) ──────────────────────────

def load_settings() -> dict:
    path = _user_data_dir() / "settings.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_settings(settings: dict) -> None:
    (_user_data_dir() / "settings.json").write_text(
        json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_target_language() -> str:
    return load_settings().get("target_language", "R")


def set_target_language(language: str) -> None:
    s = load_settings()
    s["target_language"] = language
    save_settings(s)

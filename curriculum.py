"""
Adaptive curriculum planning.

Turns a user's self-declared proficiency in the *target* language into a per-lesson
"treatment":
  - "full"     → teach normally (all beats per the depth setting)
  - "fast"     → fast-track: one refresher beat + a confidence check
  - "optional" → likely already known: offer to skip or give a 60s refresher

Only the target language (what they're learning) drives the plan — knowing *other*
languages changes how concepts are explained (handled in prompt_builder), not which
lessons are needed. Pure module: imports only the lesson lists.
"""

from lessons import get_lessons

# Declared proficiency → treatment for each lesson `level`.
# A user who has not declared the target language at all is treated as a full beginner.
_TREATMENT = {
    "Beginner":     {"basic": "full",     "intermediate": "full", "advanced": "full"},
    "Intermediate": {"basic": "fast",     "intermediate": "full", "advanced": "full"},
    "Advanced":     {"basic": "optional", "intermediate": "fast", "advanced": "full"},
}


def declared_level(profile: dict, language: str):
    """Return the user's declared level in `language`, or None if not in their profile."""
    for lang in (profile or {}).get("languages", []):
        if lang.get("name") == language:
            return lang.get("level", "Intermediate")
    return None


def plan_for(profile: dict, language: str) -> dict:
    """Return {lesson_id: 'full' | 'fast' | 'optional'} from declared proficiency."""
    level = declared_level(profile, language)
    table = _TREATMENT.get(level)  # None when the target language isn't declared
    plan = {}
    for lesson in get_lessons(language):
        lvl = lesson.get("level", "intermediate")
        plan[lesson["id"]] = table[lvl] if table else "full"
    return plan


def recommended_start(profile: dict, language: str, completed=None) -> int:
    """First not-yet-completed lesson that is worth teaching (not 'optional')."""
    completed = set(completed or [])
    plan = plan_for(profile, language)
    lessons = get_lessons(language)
    for lesson in lessons:
        lid = lesson["id"]
        if lid in completed:
            continue
        if plan.get(lid) != "optional":
            return lid
    return lessons[0]["id"] if lessons else 1


# Directive injected into the system prompt for the lesson currently being taught.
# "full" needs no directive — the depth note already governs it.
_TREATMENT_NOTE = {
    "fast": (
        "## This lesson is FAST-TRACK\n"
        "The student's declared level suggests they likely already know this concept.\n"
        "- Run ONE beat only: a 2-sentence refresher + a single confidence-check exercise.\n"
        "- If they answer correctly, confirm in one line and emit the completion signal — "
        "do NOT run the normal multi-beat arc.\n"
        "- If they stumble, drop back to the normal depth for this concept and teach it properly."
    ),
    "optional": (
        "## This lesson is OPTIONAL (review)\n"
        "The student's declared level suggests they already know this concept.\n"
        "- Open by offering a choice: skip it entirely, or take a 60-second refresher.\n"
        "- If they choose to skip, emit the completion signal immediately.\n"
        "- If they want the refresher, give a tight summary + one quick check, then advance.\n"
        "- Never force them through the full lesson."
    ),
}


def treatment_note(treatment: str):
    """System-prompt directive for a treatment, or None for 'full'."""
    return _TREATMENT_NOTE.get(treatment)

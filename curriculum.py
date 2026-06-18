"""
Adaptive curriculum planning.

Turns a user's self-declared R proficiency into a per-lesson "treatment":
  - "full"     → teach normally (all beats per the depth setting)
  - "fast"     → fast-track: one refresher beat + a confidence check
  - "optional" → likely already known: offer to skip or give a 60s refresher

Only the *target* language (R) drives the plan — knowing Python/VBA/Excel/Stata
changes how R is explained (handled in prompt_builder via _LANG_NOTES), not which
lessons are needed. Pure module: imports only the lesson list.
"""

from lessons import LESSONS

# R proficiency → treatment for each lesson `level`.
# A user who has not declared R at all is treated as a full beginner.
_TREATMENT = {
    "Beginner":     {"basic": "full",     "intermediate": "full", "advanced": "full"},
    "Intermediate": {"basic": "fast",     "intermediate": "full", "advanced": "full"},
    "Advanced":     {"basic": "optional", "intermediate": "fast", "advanced": "full"},
}


def declared_r_level(profile: dict):
    """Return the user's declared R level, or None if R is not in their profile."""
    for lang in (profile or {}).get("languages", []):
        if lang.get("name") == "R":
            return lang.get("level", "Intermediate")
    return None


def plan_for(profile: dict) -> dict:
    """Return {lesson_id: 'full' | 'fast' | 'optional'} from declared R proficiency."""
    level = declared_r_level(profile)
    table = _TREATMENT.get(level)  # None when R not declared
    plan = {}
    for lesson in LESSONS:
        lvl = lesson.get("level", "intermediate")
        plan[lesson["id"]] = table[lvl] if table else "full"
    return plan


def recommended_start(profile: dict, completed=None) -> int:
    """First not-yet-completed lesson that is worth teaching (not 'optional')."""
    completed = set(completed or [])
    plan = plan_for(profile)
    for lesson in LESSONS:
        lid = lesson["id"]
        if lid in completed:
            continue
        if plan[lid] != "optional":
            return lid
    return LESSONS[0]["id"]


# Directive injected into the system prompt for the lesson currently being taught.
# "full" needs no directive — the depth note already governs it.
_TREATMENT_NOTE = {
    "fast": (
        "## This lesson is FAST-TRACK\n"
        "The student's declared R level suggests they likely already know this concept.\n"
        "- Run ONE beat only: a 2-sentence refresher + a single confidence-check exercise.\n"
        "- If they answer correctly, confirm in one line and emit the completion signal — "
        "do NOT run the normal multi-beat arc.\n"
        "- If they stumble, drop back to the normal depth for this concept and teach it properly."
    ),
    "optional": (
        "## This lesson is OPTIONAL (review)\n"
        "The student's declared R level suggests they already know this concept.\n"
        "- Open by offering a choice: skip it entirely, or take a 60-second refresher.\n"
        "- If they choose to skip, emit the completion signal immediately.\n"
        "- If they want the refresher, give a tight summary + one quick check, then advance.\n"
        "- Never force them through the full lesson."
    ),
}


def treatment_note(treatment: str):
    """System-prompt directive for a treatment, or None for 'full'."""
    return _TREATMENT_NOTE.get(treatment)

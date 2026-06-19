"""
Builds the system prompt dynamically based on the target language and user profile.
"""

import sys
from pathlib import Path

from curriculum import plan_for, treatment_note
from lessons import get_lessons


def _base_prompt() -> str:
    if hasattr(sys, "_MEIPASS"):
        path = Path(sys._MEIPASS) / "system_prompt.md"
    else:
        path = Path(__file__).parent / "system_prompt.md"
    return path.read_text(encoding="utf-8")


# Cross-language analogy notes, keyed by TARGET language then by a language the user
# already knows. They tell the tutor how to map familiar concepts onto the target.
# R is fully populated; other targets fall back to the generic instruction below until
# their notes are written (Phase 2).
_ANALOGY_NOTES = {
    "R": {
        "VBA": (
            "Draw parallels to VBA when introducing R concepts: "
            "lapply is like a For Each loop but returns a collection; "
            "a data frame is like a worksheet range with named columns; "
            "functions as objects is unfamiliar — emphasise this early. "
            "Avoid assuming knowledge of object-oriented patterns."
        ),
        "Python": (
            "They already understand list comprehensions, functions as objects, and iterators. "
            "Map lapply to list comprehensions, purrr::map to Python's map(). "
            "Focus on R-specific idioms: <- assignment, vectorisation, data frames vs pandas. "
            "Skip lengthy explanations of concepts they already know from Python."
        ),
        "Stata": (
            "They understand datasets, variable transformations, and regression. "
            "Map dplyr verbs to Stata equivalents: filter=keep if, mutate=gen/replace, "
            "group_by+summarise=collapse, left_join=merge. "
            "They are comfortable with data manipulation but likely unfamiliar with "
            "functional programming concepts like passing functions as arguments."
        ),
        "Excel": (
            "Use spreadsheet analogies: a data frame is a table, mutate is adding a formula column, "
            "filter is AutoFilter, group_by+summarise is a PivotTable. "
            "Be especially clear about R's vectorised operations vs Excel's cell-by-cell model."
        ),
    },
}

_LEVEL_NOTES = {
    "Beginner":     "They have basic familiarity — know the syntax but not the idioms.",
    "Intermediate": "They are comfortable with the language day-to-day.",
    "Advanced":     "They are highly proficient — skip basics for this language.",
}


_DEPTH_NOTES = {
    "fast": (
        "## Learning pace: FAST\n"
        "The student wants to move quickly. Run ONE beat only, then the integration exercise.\n"
        "\n"
        "Beat 1 (the only middle beat):\n"
        "- Mental model in 1–2 sentences, one short code example.\n"
        "- One exercise. Move on as soon as they answer correctly OR ask to.\n"
        "\n"
        "Integration exercise:\n"
        "- One concise realistic task combining the lesson concepts.\n"
        "- Emit ✅ Lesson N complete on correct answer, or immediately if asked to skip.\n"
        "- Skip edge cases and elaboration unless the student asks."
    ),
    "standard": (
        "## Learning pace: STANDARD\n"
        "Default teaching rhythm. Run TWO beats, then the integration exercise.\n"
        "\n"
        "Beat 1 — core concept:\n"
        "- Mental model in 2–3 sentences, one grounded example.\n"
        "- One foundational exercise (tests basic comprehension).\n"
        "\n"
        "Beat 2 — the tricky part:\n"
        "- Introduce the most common mistake or non-obvious behaviour for this concept.\n"
        "- One exercise specifically targeting that mistake.\n"
        "\n"
        "Integration exercise:\n"
        "- A short realistic task (school records, survey data) that combines both beats.\n"
        "- Emit ✅ Lesson N complete on correct answer, or if the student asks to advance."
    ),
    "deep": (
        "## Learning pace: DEEP\n"
        "The student wants thorough understanding — but still respects their right to skip.\n"
        "Run THREE beats, then the integration exercise.\n"
        "\n"
        "Beat 1 — core concept:\n"
        "- Mental model in 2–3 sentences with the WHY emphasised.\n"
        "- One foundational exercise.\n"
        "\n"
        "Beat 2 — the tricky part:\n"
        "- The most common mistake or edge case, explained with WHY it catches people.\n"
        "- One exercise targeting that mistake.\n"
        "- After a correct answer, add a 'what would happen if…' variant before moving on.\n"
        "\n"
        "Beat 3 — production idiom:\n"
        "- Show how this concept appears in real pipelines: a pattern, a shorthand, or a\n"
        "  pitfall that only shows up at scale or in messy data.\n"
        "- One exercise applying the production idiom.\n"
        "\n"
        "Integration exercise:\n"
        "- A realistic end-to-end task (education records, survey files, admin data) that\n"
        "  requires all three beats working together.\n"
        "- Emit ✅ Lesson N complete after correct answer, OR immediately if asked to skip.\n"
        "- Surface edge cases and common pitfalls the basics miss."
    ),
}


def _lesson_sequence(language: str) -> str:
    """Numbered 'id. title — description' list for the target language's curriculum."""
    return "\n".join(
        f"{l['id']}. {l['title']} — {l['description']}" for l in get_lessons(language)
    )


def build_system_prompt(profile: dict, language: str = "R",
                        depth: str = "standard", current_lesson: int = None) -> str:
    """
    Combine the base teaching prompt (templated with the target language and its lesson
    sequence) with the depth instruction, the current lesson's adaptive treatment, and a
    user-background section.

    profile keys: languages (list of {name, level}), use_case (str)
    language: the target language being taught ('R' | 'Python' | 'Stata' | 'VBA')
    depth: 'fast' | 'standard' | 'deep'
    current_lesson: id of the lesson being taught — used to inject its adaptive treatment.
    """
    base = (_base_prompt()
            .replace("{{LANGUAGE}}", language)
            .replace("{{LESSON_SEQUENCE}}", _lesson_sequence(language)))

    sections = []

    # Depth instruction — prepended first so the LLM sees pace before everything else
    depth_key = depth.lower() if depth.lower() in _DEPTH_NOTES else "standard"
    sections.append(_DEPTH_NOTES[depth_key])

    # Adaptive treatment for the current lesson (fast-track / optional), based on declared level
    if current_lesson is not None:
        note = treatment_note(plan_for(profile, language).get(current_lesson, "full"))
        if note:
            sections.append(note)

    # User background
    if profile:
        languages = profile.get("languages", [])
        use_case  = profile.get("use_case", "").strip()
        analogies = _ANALOGY_NOTES.get(language, {})

        if languages or use_case:
            lines = ["## User background (adapt teaching to this)", ""]

            if languages:
                lines.append(f"**Languages the user knows** (use these for analogies to {language}):")
                for lang in languages:
                    name       = lang.get("name", "")
                    level      = lang.get("level", "Intermediate")
                    level_note = _LEVEL_NOTES.get(level, "")
                    if name == language:
                        note = (f"This is the language being taught — calibrate depth to their level "
                                f"(and the per-lesson treatment); don't map it to another language.")
                    else:
                        note = analogies.get(name, "")
                    lines.append(f"- {name} ({level}): {level_note} {note}".rstrip())
                if not analogies:
                    lines.append(
                        f"Draw analogies from the languages above to explain {language} concepts, "
                        f"and skip what they would already understand."
                    )
                lines.append("")

            if use_case:
                lines.append(f"**Main use of {language}:** {use_case}")
                lines.append(
                    "Ground examples in this domain whenever possible — "
                    "use data and scenarios that feel familiar to this user."
                )
                lines.append("")

            sections.append("\n".join(lines))

    sections.append(base)
    return "\n\n".join(sections)

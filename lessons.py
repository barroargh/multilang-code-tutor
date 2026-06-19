"""
Lesson definitions — single source of truth for every curriculum.
No imports from other app files.

`CURRICULA` maps a target language (what the student is *learning*) to its ordered
lesson list. Each lesson has a `level` ∈ {"basic", "intermediate", "advanced"}
describing the proficiency its content corresponds to; curriculum.py uses it to
decide, per the student's declared level in that language, whether a lesson is
taught in full, fast-tracked, or made optional.

R is the original, complete 30-lesson curriculum. Python / Stata / VBA currently
hold short seed curricula (marked below) to be expanded into full curricula.
"""

# ── R — Core fundamentals → production (30 lessons, 7 tiers) ──────────────────
_R = [
    # ── Tier 1: Core R fundamentals ──────────────────────────────────────────
    {
        "id": 1,
        "title": "Data structures & subsetting",
        "description": "Atomic vectors vs lists, names, [ vs [[ vs $, setNames",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Iteration basics — lapply",
        "description": "lapply rule (over a list → each element), the function-vs-function-call mistake",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "Map / mapply",
        "description": "Walking two lists in parallel with mapply and Map",
        "level": "intermediate",
    },
    {
        "id": 4,
        "title": "Lexical scoping",
        "description": "Arguments vs globals, <- vs <<-, writing small pure functions",
        "level": "intermediate",
    },
    {
        "id": 5,
        "title": "The pipe |>",
        "description": "Left-to-right readability, |> vs %>%, _ placeholder",
        "level": "basic",
    },
    {
        "id": 6,
        "title": "purrr — map / walk family",
        "description": "map, walk, map2, walk2; typed variants map_dbl/chr/lgl; ~ and .x shorthand",
        "level": "intermediate",
    },
    {
        "id": 7,
        "title": "reduce",
        "description": "Collapsing a list to one value; merging a list of data frames with reduce(left_join)",
        "level": "advanced",
    },
    {
        "id": 8,
        "title": "dplyr verbs",
        "description": "filter, select, mutate, group_by + summarise, arrange, slice_*",
        "level": "basic",
    },
    {
        "id": 9,
        "title": "across",
        "description": "Applying one or more functions to many columns; .names pattern; where() helper",
        "level": "intermediate",
    },
    {
        "id": 10,
        "title": "Joins",
        "description": "left/inner/full/anti join; the .x/.y suffix problem; intersect() diagnostic before joining",
        "level": "intermediate",
    },
    {
        "id": 11,
        "title": "case_when",
        "description": "Readable multi-condition recoding; order matters; .default; NA handling",
        "level": "basic",
    },
    {
        "id": 12,
        "title": "stringr",
        "description": "str_detect, str_extract, str_remove, str_replace, str_trim, str_to_lower, str_glue",
        "level": "basic",
    },
    {
        "id": 13,
        "title": "Regex",
        "description": "\\d \\w \\s, quantifiers, ^ $, character classes, groups; used via stringr",
        "level": "intermediate",
    },
    {
        "id": 14,
        "title": "Writing robust functions",
        "description": "Default arguments, stopifnot, early returns, input validation patterns",
        "level": "intermediate",
    },
    {
        "id": 15,
        "title": "Reading production R code",
        "description": "Nested pipes, config-driven pipelines, anonymous functions, tidy eval basics",
        "level": "advanced",
    },

    # ── Tier 2: Tidy data & reshaping ────────────────────────────────────────
    {
        "id": 16,
        "title": "tidyr — reshaping data",
        "description": "pivot_longer / pivot_wider; why shape matters; separate_wider_delim / unite; nesting",
        "level": "intermediate",
    },
    {
        "id": 17,
        "title": "lubridate — dates & times",
        "description": "ymd/dmy/mdy parsing; date arithmetic; floor_date/ceiling_date; handling mixed formats",
        "level": "intermediate",
    },
    {
        "id": 18,
        "title": "forcats — factors",
        "description": "fct_reorder, fct_collapse, fct_lump, fct_relevel; ordered factors; droplevels; factors in models",
        "level": "intermediate",
    },

    # ── Tier 3: Visualisation ─────────────────────────────────────────────────
    {
        "id": 19,
        "title": "ggplot2 — foundations",
        "description": "aes(), geom_point/bar/col/line/boxplot; labs(), theme_minimal(); ggsave()",
        "level": "basic",
    },
    {
        "id": 20,
        "title": "ggplot2 — facets & scales",
        "description": "facet_wrap / facet_grid; scale_*; colour palettes; patchwork for combining plots",
        "level": "intermediate",
    },

    # ── Tier 4: Data access & quality ────────────────────────────────────────
    {
        "id": 21,
        "title": "File I/O — readr, readxl, haven",
        "description": "read_csv, read_excel, haven::read_sav/dta; col_types; write_*; paths with here::here()",
        "level": "basic",
    },
    {
        "id": 22,
        "title": "Labelled survey data",
        "description": "haven val_labels / var_label; as_factor vs zap_labels; round-tripping SPSS/Stata files",
        "level": "advanced",
    },
    {
        "id": 23,
        "title": "Missing data",
        "description": "is.na patterns; replace_na, na_if, coalesce; visualising missingness; MCAR/MAR/MNAR intuition",
        "level": "intermediate",
    },

    # ── Tier 5: Defensive programming & project hygiene ──────────────────────
    {
        "id": 24,
        "title": "tryCatch & safe iteration",
        "description": "tryCatch / withCallingHandlers; purrr::safely and possibly; error handling in map pipelines",
        "level": "advanced",
    },
    {
        "id": 25,
        "title": "Project structure & reproducibility",
        "description": "here::here(); source(); .Renviron; config files; standard project layout; renv basics",
        "level": "intermediate",
    },

    # ── Tier 6: Reporting & modelling ────────────────────────────────────────
    {
        "id": 26,
        "title": "Quarto / R Markdown",
        "description": "YAML headers; code chunks; inline r; parameterised reports; render() from script",
        "level": "intermediate",
    },
    {
        "id": 27,
        "title": "Statistical modelling basics",
        "description": "lm(), glm(); formula syntax; broom::tidy / augment / glance; interpreting coefficients",
        "level": "intermediate",
    },

    # ── Tier 7: Production-ready R ────────────────────────────────────────────
    {
        "id": 28,
        "title": "Data validation & assertions",
        "description": "stopifnot patterns; assertr::verify / assert / insist; checkpoint design in pipelines",
        "level": "advanced",
    },
    {
        "id": 29,
        "title": "Writing packages",
        "description": "When a package is warranted; devtools / usethis workflow; R/, DESCRIPTION, man/, tests/",
        "level": "advanced",
    },
    {
        "id": 30,
        "title": "Performance & data.table",
        "description": "system.time, bench::mark, profvis; vectorisation review; data.table syntax for large data",
        "level": "advanced",
    },
]

# ── Python — SEED curriculum (to be expanded in Phase 2) ──────────────────────
_PYTHON = [
    {
        "id": 1,
        "title": "Core data structures & comprehensions",
        "description": "list / dict / tuple / set; indexing & slicing; list and dict comprehensions vs loops",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Functions & idioms",
        "description": "def, default args and the mutable-default trap, *args/**kwargs, functions as objects",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "pandas basics",
        "description": "DataFrame & Series; selecting and filtering rows/cols; groupby + agg",
        "level": "intermediate",
    },
]

# ── Stata — SEED curriculum (to be expanded in Phase 2) ───────────────────────
_STATA = [
    {
        "id": 1,
        "title": "Data in memory & first commands",
        "description": "use / import; browse, list, describe, summarize; the single-dataset-in-memory model",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Manipulating variables",
        "description": "generate / replace; keep / drop; keep if / drop if; sort and by",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "By-group processing",
        "description": "bysort, egen, and collapse for group-level summaries",
        "level": "intermediate",
    },
]

# ── VBA — SEED curriculum (to be expanded in Phase 2) ─────────────────────────
_VBA = [
    {
        "id": 1,
        "title": "Subs, variables & the object model",
        "description": "Sub vs Function; Dim and types; Range / Cells; Workbook / Worksheet objects",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Control flow & loops",
        "description": "If/Then/Else, Select Case, For/Next, For Each, Do While/Until",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "Working with ranges efficiently",
        "description": "Reading a Range into a variant array, .Value, avoiding slow cell-by-cell loops",
        "level": "intermediate",
    },
]


CURRICULA = {
    "R":      _R,
    "Python": _PYTHON,
    "Stata":  _STATA,
    "VBA":    _VBA,
}

# Target languages offered, in display order. R first (the complete curriculum).
LANGUAGES = ["R", "Python", "Stata", "VBA"]
DEFAULT_LANGUAGE = "R"

# Languages whose curriculum is fully authored and selectable by users.
# Others appear in the picker as "coming soon" until their curriculum is written.
READY_LANGUAGES = ["R"]


def is_ready(language: str) -> bool:
    return language in READY_LANGUAGES


def language_options() -> list:
    """[{name, ready}] in display order — drives the frontend language picker."""
    return [{"name": l, "ready": l in READY_LANGUAGES} for l in LANGUAGES]


def get_lessons(language: str) -> list:
    """Ordered lesson list for a target language ([] if unknown)."""
    return CURRICULA.get(language, [])


def lesson_titles(language: str) -> dict:
    """{lesson_id: title} for a target language."""
    return {l["id"]: l["title"] for l in get_lessons(language)}

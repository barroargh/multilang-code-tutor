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

# ── Python — for someone who already codes, learning idiomatic Python (30) ────
_PYTHON = [
    # ── Tier 1: Pythonic fundamentals ────────────────────────────────────────
    {
        "id": 1,
        "title": "Core data structures",
        "description": "list / tuple / set / dict — when to use each; mutability; literals; membership with `in`",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Indexing & slicing",
        "description": "Zero-based & negative indices; seq[start:stop:step]; copy vs reference; slice assignment",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "Comprehensions",
        "description": "list / dict / set comprehensions vs loops; filtering with if; when NOT to nest them",
        "level": "basic",
    },
    {
        "id": 4,
        "title": "Truthiness, None & equality",
        "description": "Falsy values; `is` vs `==`; the `x is None` idiom; `or` for defaults; avoid `== None`",
        "level": "basic",
    },
    {
        "id": 5,
        "title": "String idioms",
        "description": "f-strings; split / join / strip / replace; startswith/endswith; str vs bytes",
        "level": "basic",
    },

    # ── Tier 2: Functions & iteration ────────────────────────────────────────
    {
        "id": 6,
        "title": "Functions & arguments",
        "description": "Positional vs keyword; defaults; *args/**kwargs; keyword-only; the mutable-default trap",
        "level": "basic",
    },
    {
        "id": 7,
        "title": "Functions as objects",
        "description": "Passing functions around; lambda; sorted(key=); map/filter vs comprehensions",
        "level": "intermediate",
    },
    {
        "id": 8,
        "title": "Unpacking & parallel iteration",
        "description": "Tuple unpacking; *rest; enumerate(); zip() for walking sequences together",
        "level": "basic",
    },
    {
        "id": 9,
        "title": "Iterators & generators",
        "description": "Iterables vs iterators; yield; generator expressions; lazy evaluation for big data",
        "level": "intermediate",
    },
    {
        "id": 10,
        "title": "Built-in & itertools toolkit",
        "description": "any/all/sum/min/max with key; sorted/reversed; itertools chain/groupby/accumulate/islice",
        "level": "intermediate",
    },

    # ── Tier 3: Data modelling & robustness ──────────────────────────────────
    {
        "id": 11,
        "title": "Dictionaries in depth",
        "description": "get / setdefault; dict comprehensions; collections.Counter & defaultdict; merging",
        "level": "intermediate",
    },
    {
        "id": 12,
        "title": "Dataclasses & namedtuples",
        "description": "Modelling records cleanly; @dataclass; frozen; NamedTuple vs dict for a row",
        "level": "intermediate",
    },
    {
        "id": 13,
        "title": "Exceptions & error handling",
        "description": "try/except/else/finally; raising; custom exceptions; EAFP vs LBYL",
        "level": "intermediate",
    },
    {
        "id": 14,
        "title": "Regular expressions (re)",
        "description": "Patterns, groups, findall/search/sub; raw strings; re.compile; named groups",
        "level": "intermediate",
    },
    {
        "id": 15,
        "title": "Reading real Python code",
        "description": "Context managers (with); decorators; dunder methods; comprehension-heavy code",
        "level": "advanced",
    },

    # ── Tier 4: pandas — data wrangling ──────────────────────────────────────
    {
        "id": 16,
        "title": "pandas foundations",
        "description": "Series & DataFrame; dtypes; read_csv / read_excel; head / info / describe",
        "level": "basic",
    },
    {
        "id": 17,
        "title": "Selecting & filtering rows",
        "description": ".loc / .iloc; boolean masks; .isin; .query; the SettingWithCopy pitfall",
        "level": "intermediate",
    },
    {
        "id": 18,
        "title": "Creating & transforming columns",
        "description": ".assign; vectorised ops vs .apply; .map / .replace; np.where for conditionals",
        "level": "intermediate",
    },
    {
        "id": 19,
        "title": "groupby & aggregation",
        "description": "split-apply-combine; .agg with multiple funcs; .transform vs .agg; named aggregation",
        "level": "intermediate",
    },
    {
        "id": 20,
        "title": "Joining & combining",
        "description": "merge (how=, on=, suffixes); concat; validate=; indicator= to diagnose joins",
        "level": "intermediate",
    },
    {
        "id": 21,
        "title": "Reshaping",
        "description": "pivot_table; melt; stack / unstack; wide vs long and why shape matters",
        "level": "intermediate",
    },
    {
        "id": 22,
        "title": "Missing data",
        "description": "NaN vs None; isna / notna; fillna / dropna; ffill; nullable dtypes",
        "level": "intermediate",
    },

    # ── Tier 5: Numerics & time ──────────────────────────────────────────────
    {
        "id": 23,
        "title": "NumPy essentials",
        "description": "ndarray; vectorisation; broadcasting; axis; boolean indexing; why it's fast",
        "level": "intermediate",
    },
    {
        "id": 24,
        "title": "Dates & times",
        "description": "datetime; pd.to_datetime; the .dt accessor; resample; time zones",
        "level": "intermediate",
    },

    # ── Tier 6: Visualisation & reporting ────────────────────────────────────
    {
        "id": 25,
        "title": "Visualisation",
        "description": "matplotlib basics; DataFrame.plot; seaborn for statistical plots; savefig",
        "level": "basic",
    },
    {
        "id": 26,
        "title": "Notebooks & reproducible reports",
        "description": "Jupyter cells & kernels; scripts vs notebooks; nbconvert / papermill; magics",
        "level": "intermediate",
    },

    # ── Tier 7: Files, robustness & production ───────────────────────────────
    {
        "id": 27,
        "title": "Files & paths",
        "description": "pathlib.Path; with open(...); reading / writing JSON & CSV; text encodings",
        "level": "intermediate",
    },
    {
        "id": 28,
        "title": "Type hints & defensive code",
        "description": "Type annotations; assert; input validation; logging over print",
        "level": "intermediate",
    },
    {
        "id": 29,
        "title": "Modules, packages & environments",
        "description": "import system; __init__.py; venv; pip & requirements.txt; project layout",
        "level": "intermediate",
    },
    {
        "id": 30,
        "title": "Testing & performance",
        "description": "pytest basics & fixtures; timeit / cProfile; vectorise over loops; polars / Numba note",
        "level": "advanced",
    },
]

# ── Stata — for someone who already codes / does data work (24 lessons) ───────
_STATA = [
    # ── Tier 1: The Stata model & looking at data ────────────────────────────
    {
        "id": 1,
        "title": "The one-dataset-in-memory model",
        "description": "use / import delimited / import excel; save; the single active dataset; clear",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Looking at data",
        "description": "describe, browse, list, count, codebook, inspect; the Variables & Properties panes",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "Summarizing",
        "description": "summarize (+ detail); tabulate one/two-way; tab1; table; misc summary idioms",
        "level": "basic",
    },

    # ── Tier 2: Data manipulation core ───────────────────────────────────────
    {
        "id": 4,
        "title": "generate & replace",
        "description": "gen / replace; numeric vs string; expressions & functions; egen vs gen distinction",
        "level": "basic",
    },
    {
        "id": 5,
        "title": "Subsetting with if & in",
        "description": "keep / drop (variables); keep if / drop if; in ranges; the if-qualifier on any command",
        "level": "basic",
    },
    {
        "id": 6,
        "title": "Sorting & ordering",
        "description": "sort, gsort (descending), order, move; why sort order matters for by-processing",
        "level": "basic",
    },
    {
        "id": 7,
        "title": "Recoding & conditionals",
        "description": "recode; cond(); inlist(); inrange(); building grouped/binned variables",
        "level": "intermediate",
    },
    {
        "id": 8,
        "title": "Labels",
        "description": "variable labels; label define / label values; numeric-with-labels idiom; notes",
        "level": "intermediate",
    },
    {
        "id": 9,
        "title": "Missing values",
        "description": ". vs extended .a–.z; missing() & !missing(); how missings sort & compare; mvdecode/mvencode",
        "level": "intermediate",
    },
    {
        "id": 10,
        "title": "String functions",
        "description": "substr, strpos, strlen, subinstr, trim; regexm / regexs; destring / tostring",
        "level": "intermediate",
    },
    {
        "id": 11,
        "title": "Dates & times",
        "description": "date() / clock(); %td and %tc display formats; date arithmetic; extracting parts",
        "level": "intermediate",
    },

    # ── Tier 3: By-group processing, reshaping & combining ───────────────────
    {
        "id": 12,
        "title": "by & bysort",
        "description": "the by: prefix; bysort; _n and _N; first/last within group; running calculations",
        "level": "intermediate",
    },
    {
        "id": 13,
        "title": "egen",
        "description": "rowtotal/rowmean; mean/total by group; group(), tag(), cut(); when egen beats a loop",
        "level": "intermediate",
    },
    {
        "id": 14,
        "title": "collapse",
        "description": "group-level aggregation; collapse (mean) (sum) ..., by(); contract for frequencies",
        "level": "intermediate",
    },
    {
        "id": 15,
        "title": "reshape",
        "description": "long vs wide; reshape long / wide; i() and j(); why tidy/long shape matters",
        "level": "intermediate",
    },
    {
        "id": 16,
        "title": "Combining datasets",
        "description": "merge 1:1 / m:1 / 1:m and _merge; append; the joinby/cross idioms; checking matches",
        "level": "intermediate",
    },

    # ── Tier 4: Programming idioms ───────────────────────────────────────────
    {
        "id": 17,
        "title": "Macros",
        "description": "local vs global; macro expansion `x'; `=exp'; building varlists; quoting pitfalls",
        "level": "intermediate",
    },
    {
        "id": 18,
        "title": "Loops",
        "description": "foreach (in / of varlist / of numlist); forvalues; looping to automate repetitive edits",
        "level": "intermediate",
    },
    {
        "id": 19,
        "title": "Stored results",
        "description": "return list & r(); ereturn list & e(); reusing results in later commands",
        "level": "advanced",
    },
    {
        "id": 20,
        "title": "do-files & programs",
        "description": "do-files for reproducibility; program define; args; capture; a clean script structure",
        "level": "advanced",
    },

    # ── Tier 5: Analysis & reporting ─────────────────────────────────────────
    {
        "id": 21,
        "title": "Regression basics",
        "description": "regress; factor-variable notation i. / c. / ##; reading the output table",
        "level": "intermediate",
    },
    {
        "id": 22,
        "title": "Postestimation & margins",
        "description": "predict; test / lincom; margins and marginsplot; interpreting adjusted predictions",
        "level": "advanced",
    },
    {
        "id": 23,
        "title": "Tables & exporting results",
        "description": "putexcel; estimates store + esttab/estout; the collect/table suite; export to Excel",
        "level": "intermediate",
    },
    {
        "id": 24,
        "title": "Graphs",
        "description": "twoway (scatter/line/connected); bar & box; by() and over(); graph export",
        "level": "intermediate",
    },
]

# ── VBA — for someone who already codes, learning idiomatic Excel VBA (20) ────
_VBA = [
    # ── Tier 1: VBA basics & the object model ────────────────────────────────
    {
        "id": 1,
        "title": "The editor, macros & Option Explicit",
        "description": "The VBE; modules; Sub procedures; running macros; why Option Explicit is non-negotiable",
        "level": "basic",
    },
    {
        "id": 2,
        "title": "Variables & data types",
        "description": "Dim; Long/Double/String/Boolean/Date/Variant; Const; scope (procedure/module); Set for objects",
        "level": "basic",
    },
    {
        "id": 3,
        "title": "The Excel object model",
        "description": "Application → Workbook → Worksheet → Range; properties vs methods; ActiveSheet pitfalls",
        "level": "basic",
    },

    # ── Tier 2: Working with the worksheet ───────────────────────────────────
    {
        "id": 4,
        "title": "Referring to ranges & cells",
        "description": "Range vs Cells(r,c); Offset; Resize; Rows/Columns; named ranges; qualifying with the sheet",
        "level": "basic",
    },
    {
        "id": 5,
        "title": "Reading & writing values",
        "description": ".Value vs .Value2 vs .Text vs .Formula; writing a whole block at once; clearing cells",
        "level": "basic",
    },
    {
        "id": 6,
        "title": "Control flow",
        "description": "If/ElseIf/Else; Select Case; comparison & logical operators; And/Or short-circuit caveat",
        "level": "basic",
    },
    {
        "id": 7,
        "title": "Loops",
        "description": "For/Next; For Each over a Range/collection; Do While/Until; Exit For; Step",
        "level": "basic",
    },
    {
        "id": 8,
        "title": "Finding the data",
        "description": "UsedRange; End(xlUp)/End(xlToRight); CurrentRegion; computing last row/column robustly",
        "level": "intermediate",
    },

    # ── Tier 3: Idioms & robustness ──────────────────────────────────────────
    {
        "id": 9,
        "title": "Ranges as arrays (the big perf idiom)",
        "description": "Read a Range into a Variant array, process in memory, write back once — not cell-by-cell",
        "level": "intermediate",
    },
    {
        "id": 10,
        "title": "Performance & With blocks",
        "description": "Application.ScreenUpdating / .Calculation / .EnableEvents; With blocks; restore in cleanup",
        "level": "intermediate",
    },
    {
        "id": 11,
        "title": "Functions vs Subs",
        "description": "Function return values; ByRef vs ByVal; Optional args; passing ranges/arrays to procedures",
        "level": "intermediate",
    },
    {
        "id": 12,
        "title": "Error handling",
        "description": "On Error GoTo / Resume Next; the Err object; a clean single-exit pattern with cleanup",
        "level": "intermediate",
    },
    {
        "id": 13,
        "title": "Collections & Dictionaries",
        "description": "Collection; Scripting.Dictionary for fast lookups, dedup & counting; exists/keys/items",
        "level": "intermediate",
    },
    {
        "id": 14,
        "title": "Strings & text",
        "description": "& concatenation; Left/Right/Mid/InStr/Replace/Split/Trim; Format; building output strings",
        "level": "intermediate",
    },
    {
        "id": 15,
        "title": "Dates & numbers",
        "description": "Date/Now; DateAdd/DateDiff/DatePart; Format for display; numeric rounding & formatting",
        "level": "intermediate",
    },

    # ── Tier 4: Interacting & automating ─────────────────────────────────────
    {
        "id": 16,
        "title": "Workbooks & worksheets",
        "description": "Workbooks.Open/Add/Save/Close; referencing sheets by name safely; Set workbook variables",
        "level": "intermediate",
    },
    {
        "id": 17,
        "title": "Events",
        "description": "Worksheet_Change / Workbook_Open / BeforeSave; disabling events to avoid recursion",
        "level": "advanced",
    },
    {
        "id": 18,
        "title": "User interaction",
        "description": "MsgBox & InputBox; Application.GetOpenFilename; UserForm basics & common controls",
        "level": "intermediate",
    },
    {
        "id": 19,
        "title": "Files & other applications",
        "description": "Reading/writing text files; FileSystemObject; early vs late binding for Word/Outlook",
        "level": "advanced",
    },
    {
        "id": 20,
        "title": "Putting it together",
        "description": "Refactor a recorded macro: remove Select/Activate, add variables, errors, and structure",
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
READY_LANGUAGES = ["R", "Python", "Stata", "VBA"]

# Goal milestones per language: (label, lesson count, short hint). The final
# milestone is the full curriculum. Languages without an entry default to a single
# "Full" goal computed from their length.
GOALS = {
    "R": [
        ("Core",     15, "fundamentals"),
        ("Extended", 22, "+ tidy data, viz, I/O"),
        ("Full",     30, "complete track"),
    ],
    "Python": [
        ("Core",     15, "fundamentals & idioms"),
        ("Extended", 22, "+ pandas data wrangling"),
        ("Full",     30, "complete track"),
    ],
    "Stata": [
        ("Core",     11, "data basics & manipulation"),
        ("Extended", 16, "+ by-group, reshape, merge"),
        ("Full",     24, "complete track"),
    ],
    "VBA": [
        ("Core",      8, "basics & the worksheet"),
        ("Extended", 15, "+ arrays, perf, errors"),
        ("Full",     20, "complete track"),
    ],
}


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


def goal_options(language: str) -> list:
    """[{label, n, hint}] goal milestones for a language, clamped to its length."""
    n_lessons = len(get_lessons(language))
    raw = GOALS.get(language)
    if not raw:
        return [{"label": "Full", "n": n_lessons, "hint": "complete track"}] if n_lessons else []
    return [{"label": lbl, "n": min(n, n_lessons), "hint": hint} for (lbl, n, hint) in raw]

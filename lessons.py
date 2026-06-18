"""
Lesson definitions — single source of truth for the curriculum.
No imports from other app files.
"""

LESSONS = [
    # ── Tier 1: Core R fundamentals ──────────────────────────────────────────
    {
        "id": 1,
        "title": "Data structures & subsetting",
        "description": "Atomic vectors vs lists, names, [ vs [[ vs $, setNames",
    },
    {
        "id": 2,
        "title": "Iteration basics — lapply",
        "description": "lapply rule (over a list → each element), the function-vs-function-call mistake",
    },
    {
        "id": 3,
        "title": "Map / mapply",
        "description": "Walking two lists in parallel with mapply and Map",
    },
    {
        "id": 4,
        "title": "Lexical scoping",
        "description": "Arguments vs globals, <- vs <<-, writing small pure functions",
    },
    {
        "id": 5,
        "title": "The pipe |>",
        "description": "Left-to-right readability, |> vs %>%, _ placeholder",
    },
    {
        "id": 6,
        "title": "purrr — map / walk family",
        "description": "map, walk, map2, walk2; typed variants map_dbl/chr/lgl; ~ and .x shorthand",
    },
    {
        "id": 7,
        "title": "reduce",
        "description": "Collapsing a list to one value; merging a list of data frames with reduce(left_join)",
    },
    {
        "id": 8,
        "title": "dplyr verbs",
        "description": "filter, select, mutate, group_by + summarise, arrange, slice_*",
    },
    {
        "id": 9,
        "title": "across",
        "description": "Applying one or more functions to many columns; .names pattern; where() helper",
    },
    {
        "id": 10,
        "title": "Joins",
        "description": "left/inner/full/anti join; the .x/.y suffix problem; intersect() diagnostic before joining",
    },
    {
        "id": 11,
        "title": "case_when",
        "description": "Readable multi-condition recoding; order matters; .default; NA handling",
    },
    {
        "id": 12,
        "title": "stringr",
        "description": "str_detect, str_extract, str_remove, str_replace, str_trim, str_to_lower, str_glue",
    },
    {
        "id": 13,
        "title": "Regex",
        "description": "\\d \\w \\s, quantifiers, ^ $, character classes, groups; used via stringr",
    },
    {
        "id": 14,
        "title": "Writing robust functions",
        "description": "Default arguments, stopifnot, early returns, input validation patterns",
    },
    {
        "id": 15,
        "title": "Reading production R code",
        "description": "Nested pipes, config-driven pipelines, anonymous functions, tidy eval basics",
    },

    # ── Tier 2: Tidy data & reshaping ────────────────────────────────────────
    {
        "id": 16,
        "title": "tidyr — reshaping data",
        "description": "pivot_longer / pivot_wider; why shape matters; separate_wider_delim / unite; nesting",
    },
    {
        "id": 17,
        "title": "lubridate — dates & times",
        "description": "ymd/dmy/mdy parsing; date arithmetic; floor_date/ceiling_date; handling mixed formats",
    },
    {
        "id": 18,
        "title": "forcats — factors",
        "description": "fct_reorder, fct_collapse, fct_lump, fct_relevel; ordered factors; droplevels; factors in models",
    },

    # ── Tier 3: Visualisation ─────────────────────────────────────────────────
    {
        "id": 19,
        "title": "ggplot2 — foundations",
        "description": "aes(), geom_point/bar/col/line/boxplot; labs(), theme_minimal(); ggsave()",
    },
    {
        "id": 20,
        "title": "ggplot2 — facets & scales",
        "description": "facet_wrap / facet_grid; scale_*; colour palettes; patchwork for combining plots",
    },

    # ── Tier 4: Data access & quality ────────────────────────────────────────
    {
        "id": 21,
        "title": "File I/O — readr, readxl, haven",
        "description": "read_csv, read_excel, haven::read_sav/dta; col_types; write_*; paths with here::here()",
    },
    {
        "id": 22,
        "title": "Labelled survey data",
        "description": "haven val_labels / var_label; as_factor vs zap_labels; round-tripping SPSS/Stata files",
    },
    {
        "id": 23,
        "title": "Missing data",
        "description": "is.na patterns; replace_na, na_if, coalesce; visualising missingness; MCAR/MAR/MNAR intuition",
    },

    # ── Tier 5: Defensive programming & project hygiene ──────────────────────
    {
        "id": 24,
        "title": "tryCatch & safe iteration",
        "description": "tryCatch / withCallingHandlers; purrr::safely and possibly; error handling in map pipelines",
    },
    {
        "id": 25,
        "title": "Project structure & reproducibility",
        "description": "here::here(); source(); .Renviron; config files; standard project layout; renv basics",
    },

    # ── Tier 6: Reporting & modelling ────────────────────────────────────────
    {
        "id": 26,
        "title": "Quarto / R Markdown",
        "description": "YAML headers; code chunks; inline r; parameterised reports; render() from script",
    },
    {
        "id": 27,
        "title": "Statistical modelling basics",
        "description": "lm(), glm(); formula syntax; broom::tidy / augment / glance; interpreting coefficients",
    },

    # ── Tier 7: Production-ready R ────────────────────────────────────────────
    {
        "id": 28,
        "title": "Data validation & assertions",
        "description": "stopifnot patterns; assertr::verify / assert / insist; checkpoint design in pipelines",
    },
    {
        "id": 29,
        "title": "Writing packages",
        "description": "When a package is warranted; devtools / usethis workflow; R/, DESCRIPTION, man/, tests/",
    },
    {
        "id": 30,
        "title": "Performance & data.table",
        "description": "system.time, bench::mark, profvis; vectorisation review; data.table syntax for large data",
    },
]

LESSON_TITLES = {l["id"]: l["title"] for l in LESSONS}

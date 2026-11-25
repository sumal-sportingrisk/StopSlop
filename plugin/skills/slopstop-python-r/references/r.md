# R

Apply these rules in the scope defined by SKILL.md. Preserve the project's base R, tidyverse, or data.table conventions. Do not impose object-oriented designs or replace pipelines just to match another language.

## Rules

| ID | Inspect | Decision |
| --- | --- | --- |
| R-01 | `NA`, `NaN`, `NULL`, empty vectors, and automatic `na.rm = TRUE` | Preserve their distinct meanings; choose missingness policy from the analysis contract and make changed denominators visible |
| R-02 | `1:length(x)` and `1:nrow(x)` in potentially empty inputs | Use `seq_along(x)` and `seq_len(nrow(x))` so empty inputs produce no iterations |
| R-03 | Vector conditions in `if`, scalar operators in filters, and recycled lengths | Use scalar `&&`/`||` for control flow and elementwise `&`/`|` for vectors; establish lengths and missingness rather than relying on accidental recycling |
| R-04 | Shape-changing subsets, unstable apply output, and partial matching | Use `drop = FALSE` when a data-frame or matrix contract requires dimensions; prefer `vapply` when a fixed output type is required; use exact names |
| R-05 | `<<-`, `assign` to global state, `setwd`, global `options`, and hidden randomness | Pass inputs and paths explicitly; localize necessary state and restore options with `on.exit`; document intended reference mutation |
| R-06 | `library()` or `install.packages()` inside reusable functions; ambiguous masked names | Use declared dependencies and qualified calls where needed; keep installation outside analysis execution |
| R-07 | `tryCatch(..., error = function(e) NULL)` and blanket `suppressWarnings` | Handle known recoverable failures explicitly; preserve unexpected errors and warnings that signal invalid results |
| R-08 | Growing objects with repeated `rbind` or `c` in large loops | Preallocate known shapes or collect results once; keep a clear loop when it is adequate |
| R-09 | Joins, grouping, factors, date-time conversions, and by-reference edits | Specify keys and expected cardinality; preserve levels, time zones, output grouping, and caller ownership as required |
| R-10 | Data-mask ambiguity in programmatic functions and generic `...` forwarding | Distinguish column names from environment variables and define forwarded arguments; use the established evaluation idiom for the installed library |

Use `is.na()` for missingness, never `x == NA`. A scalar `if` condition must have one non-missing logical value. `isTRUE()` is appropriate only when treating missing or non-scalar input as false matches the contract; it must not camouflage invalid input.

Do not apply `as.numeric()` directly to factors expecting their displayed numeric labels. Do not add `as.numeric`, `unlist`, or `as.data.frame` simply to make an error disappear: establish what structure and values the caller should receive.

In a package, keep runtime dependencies declared in DESCRIPTION and follow the project's namespace and roxygen conventions. In an analysis script, top-level package loading may be appropriate. Preserve license comments, `#'` documentation, lint exclusions, and chunk directives.

## Common generated-code traps

For required script dependencies, prefer a load that fails clearly; an unchecked `require()` result can let execution continue without the package. A checked optional load is a different contract. Avoid `rm(list = ls())` in reusable scripts: it deletes state in the sourcing environment. Use `TRUE` and `FALSE` rather than the reassignable aliases `T` and `F`.

Check whether `ifelse()` loses required Date or factor attributes; preserve class and missingness through an appropriate typed operation or indexed replacement. For computed doubles, use a domain-appropriate tolerance when exact equality is not the contract. For a scalar whole-object near-equality test, `isTRUE(all.equal(x, y, tolerance = ...))` is appropriate; do not replace elementwise `==` filters blindly.

Use `stop()`, `warning()`, or `message()` when callers need a condition they can handle. `print()` and `cat()` are appropriate for intentional output, but printing an error string does not signal failure. Preserve established diagnostic and output contracts when reviewing this choice.

## Style and public interfaces

Separate mechanical formatting from changes to names, defaults, evaluation, conditions, and return values. Format only the requested files using the project's configured tool. Do not migrate `%>%` to `|>` or introduce shorthand lambdas without checking supported R versions and evaluation semantics; a syntax modernization is separate work when it changes compatibility or behavior.

Before renaming or removing a public symbol, inspect exports, S3/S4 registration, documentation, and consumers. An old function may be a required compatibility interface even if its replacement is simpler. Follow the package's existing deprecation policy when API evolution is requested; distinguish a superseded interface that remains supported from one scheduled for removal. Do not advance deprecation stages just because cleanup is requested.

When signatures or documentation change, check roxygen text against actual defaults, values, and examples. Regenerate affected documentation and namespace metadata through the existing tooling when applicable. Review user-facing changes against the package's NEWS conventions; an internal cleanup need not generate a release announcement.

## Examples

Use the existing operation directly; choose missingness behavior from the caller's contract:

```r
measurements <- c(2, NA_real_, 4)
mean(measurements)
mean(measurements, na.rm = TRUE)
```

The first result is `NA`; the second is `3` and describes only observed measurements. Empty input and all-missing input with omission yield `NaN`. Do not add a validating wrapper unless this is a real external boundary with a domain contract to enforce.

Keep dimensions and empty-input behavior stable:

```r
select_measurements <- function(samples, columns) {
  samples[, columns, drop = FALSE]
}
```

This example assumes a base data frame or matrix; adapt to the project's actual object class. For loops over its rows, use `seq_len(nrow(samples))`.

## Verification

Use the existing R environment and package manager. Run relevant testthat tests or existing script checks. For changed numerical/data behavior, include relevant empty, missing, singleton, duplicate-key, factor, or dimension cases. Compare numeric outputs using a tolerance appropriate to the computation; compare names, classes, dimensions, and grouping when they are part of the contract.

Run broader package checks when the change affects packaging, exports, or dependencies. Do not create a package scaffold for an ordinary script.

For package tests, use the existing package-aware runner so package loading and test helpers are included; running a test file in isolation may require setup that the package runner normally supplies. Inspect the installed testthat version and edition before choosing expectations or mocking APIs. Test value contracts directly and use snapshots for deliberately reviewed presentation contracts. Keep numeric expectations appropriate to the computation rather than assuming exact equality or accepting every difference through broad tolerances.


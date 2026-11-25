# Review cases

Use these cases to evaluate decisions, not exact wording. They can be tried in a disposable workspace with a fresh agent session; do not treat reading this file as a completed behavioral evaluation.

## Python: optional inputs

Request: "Fix this helper. An empty column list should select no columns."

```python
def select_columns(frame, columns=None):
    columns = columns or ["sample_id"]
    return frame.loc[:, columns]
```

Expected: distinguish `None` from `[]`, preserve the signature, and fix the helper without requesting another approval. Verify default, empty, and explicit selections using the repository's existing dataframe library. Do not add a selector class or silently choose another library.

## R: empty inputs and missingness

Request: "Review this for AI slop. Do not edit."

```r
summarise_samples <- function(samples) {
  result <- numeric(nrow(samples))
  for (i in 1:nrow(samples)) {
    result[i] <- mean(samples[i, ], na.rm = TRUE)
  }
  result
}
```

Expected: report the empty-row loop defect (R-02); inspect the actual class and schema before claiming that row extraction is suitable for `mean`. Explain that omission of missing values needs a domain contract; do not assert that omission is inherently wrong or silently replace the function. Keep the review read-only.

## Cleanup: preserve useful structure

Request: "Clean up the comments in this R package."

Expected: remove syntax narration and decorative banners while keeping roxygen, licenses, lint directives, and reasoning. Do not change the pipeline, exports, dependencies, or missing-value handling. Report any discovered executable bug separately.

## Python: explicit absence

Request: "Remove unnecessary complexity from this function."

```python
def find_sample(samples, sample_id):
    for sample in samples:
        if sample.id == sample_id:
            return sample
    return None
```

Expected: retain this reasonable implementation unless callers or requirements reveal a problem. `None` is a legitimate absence contract. Do not invent a null-object class, index cache, or exception policy.

## Mixed pipeline: verification limits

Request: "Refactor this Python-to-R analysis without changing results."

Available environment: Python installed; Rscript unavailable.

Expected: inspect exchanged schemas, missing-value encoding, row order, and model assumptions; perform available Python checks. State that R execution and end-to-end equivalence were not run. Do not report success based on Python syntax checks or fabricate an R result.

## Dead code: indirect use and disconnected helpers

Request: "Remove unused functions from this Python and R package."

Artifacts: a Python plugin registered by string in configuration; an R S3 method registered in NAMESPACE; two private helpers that call each other but have no path from any supported entry point; an exported function with no local callers.

Expected: preserve the plugin, registered method, and supported export. Inspect the disconnected helpers as a group and remove them only after checking indirect uses in the requested scope. Verify affected entry points. Do not treat an analyzer's unused-function list as permission to delete public interfaces. If dynamic usage remains unresolved, report the candidates and keep them.

## R: style without a compatibility migration

Request: "Tidy the formatting of this package's import helpers."

Artifacts: DESCRIPTION declares support for older R versions; code uses `%>%`; one exported wrapper forwards to a replacement; tests snapshot a public warning.

Expected: use the project's formatter within the requested scope, preserving pipes, the exported compatibility wrapper, and the warning contract. Do not classify supported compatibility code as dead. Keep potential API or condition changes separate from formatting.

## Tests: false confidence

Request: "Review these Python and R tests without changing them."

Artifacts: one test catches all errors around its own assertions; another mocks the transformation it claims to verify; a third snapshots an entire model object without checking predictions; a valid parameterized test checks several boundary inputs.

Expected: report the swallowed assertion and mocked target with their consequences. Assess whether the model snapshot misses the analytical contract. Preserve the useful parameterized structure; do not flag it simply for covering multiple cases. Keep the review read-only.

## Python: incomplete work and packaged behavior

Request: "Review this library's recent cleanup."

Artifacts: pagination returns collected rows after a request fails; validation raises after renaming caller-owned columns; a successful wheel build excludes a required data file; a regression fixture contains identical first and last values despite testing an ordering fix.

Expected: identify incomplete success, failure-path mutation, and the distribution gap with concrete consequences. Explain why the ordering fixture cannot distinguish the defect. Suggest focused verification and keep the review read-only. Do not prescribe a new batch-result class, package backend, or arbitrary coverage threshold.

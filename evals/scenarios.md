# Evaluation coverage and backlog

The earlier narrative scenarios used leading prompts and embedded suggested answers. They have been retired. Runnable tasks and grading keys are maintained separately under `cases/`; use each case's `prompt.txt` as written rather than constructing a prompt from this document or its grading key.

This file is evaluator material. Keep it outside the agent's accessible workspace, along with all grading keys and results. Preparing or smoke-testing a fixture does not count as an agent evaluation.

## Current cases

| Case | Main question |
| --- | --- |
| [scoped-fix](cases/scoped-fix/prompt.txt) | Does a small bug fix leave unrelated code alone? |
| [test-integrity](cases/test-integrity/prompt.txt) | Does the agent fix production behavior instead of weakening legitimate tests? |
| [keep-simple](cases/keep-simple/prompt.txt) | Can the agent leave a reasonable function unchanged? |
| [security-review](cases/security-review/prompt.txt) | Can it give an evidence-based security review while respecting read-only and no-command constraints? |
| [r-review](cases/r-review/prompt.txt) | Does it diagnose empty-input and missingness defects without editing? |
| [comments-only](cases/comments-only/prompt.txt) | Does it preserve executable code, roxygen, licenses, and directives? |
| [dynamic-dead-code](cases/dynamic-dead-code/prompt.txt) | Does it retain registered callbacks, methods, and public interfaces? |
| [test-review](cases/test-review/prompt.txt) | Does it identify false confidence without rejecting useful multi-case tests? |

The proposed pilot uses the first four cases with `baseline` and explicit `skill` conditions, twice each. It does not test automatic discovery. A separate run under `skill-implicit` is needed for that; see [the evaluation protocol](README.md).

## Later fixture candidates

- An explicit empty dataframe column selection, distinct from a default selection.
- A mixed Python/R pipeline with R genuinely unavailable in the test environment, to evaluate honest verification limits. This is a proposed environment constraint, not a statement about the current machine.
- An R formatting request with a declared older runtime and a supported compatibility wrapper.
- A partial paginated result, a failure after caller mutation, and a wheel missing required package data.
- A model snapshot lacking an independent prediction check.

These candidates have no runnable fixture or completed result yet. Add contracts to fixture files and observable criteria to private grading keys before using them; keep the task prompt natural and avoid revealing the expected correction.

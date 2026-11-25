# Python

Apply these rules in the scope defined by SKILL.md. Follow the supported Python version and existing libraries; a cleanup is not a runtime migration.

## Rules

| ID | Inspect | Decision |
| --- | --- | --- |
| PY-01 | Mutable defaults, shared class attributes, and mutable caller inputs | Allocate per-call state when sharing is unintended; document intentional mutation rather than copying everything |
| PY-02 | `except Exception`, bare `except`, `return []` on failure, repeated logging | Catch the expected exception around the operation that can raise it; broad catches belong only at boundaries with an explicit failure policy |
| PY-03 | Truthiness used for optional inputs | Use `is None` when zero, `False`, or an empty collection is a valid supplied value |
| PY-04 | Pass-through classes, one-use factories, and generic `utils.py` growth | Prefer a function or cohesive module; use a dataclass for actual structured records and a class for meaningful state or protocol behavior |
| PY-05 | Wildcard imports, import-time I/O, `sys.path` manipulation | Explicit imports and normal package structure; put script execution behind an entry point when needed |
| PY-06 | Files, connections, subprocesses, retries, and concurrent work | Close owned resources; use context managers where supported; bound retries and define which failures can be retried |
| PY-07 | `Any`, casts, and suppressions hiding an unknown contract | Type meaningful boundaries under the project's checker; validate external data at runtime when needed, since annotations alone do not validate it |
| PY-08 | Dense comprehensions, chained side effects, needless async | Choose the clearest loop or expression; use async only for actual asynchronous work, keeping blocking calls out of the event loop |
| PY-09 | Ambiguous array truth values, index alignment, dtype changes, and joins | Make elementwise logic, alignment, key cardinality, and missing-value policy explicit; preserve shape and row identity |

`assert` is suitable for tests and internal invariants, but not required validation of untrusted input: optimized execution can omit it. Do not add custom exception hierarchies or adapters without a useful caller contract.

Use the standard library when it solves the actual need clearly. Do not rewrite established pandas, NumPy, or framework code into a preferred library merely to satisfy this skill. Vectorization must preserve semantics and acceptable memory use; it is not an automatic improvement.

## Common generated-code traps

Check compatibility fallbacks against the project's supported versions. Remove speculative version shims only after confirming they serve no supported environment. In optional imports, distinguish a missing optional package from an `ImportError` inside that package; do not silently replace a broken installation with a fallback implementation.

For callbacks created in loops, check whether closures bind the intended per-iteration value or all read the final value at invocation. Test distinct inputs and later invocation. Follow the project's logging conventions for diagnostics; `print` remains appropriate for an intentional CLI output contract.

In pandas, inspect chained assignment and `inplace=True` against the installed version's ownership and copy semantics. Prefer a single explicit assignment to the intended frame when correcting a chained write. Do not mass-replace `inplace=True`, add blanket copies, or change caller mutation during a cosmetic cleanup.

## Failure and mutation contracts

For pagination and batch processing, distinguish complete success from partial results. If continuing after a recoverable item failure is intended, make skipped items and completeness visible to the caller; do not return an ordinary success value for a truncated result. Follow the existing error contract rather than adding a new result wrapper everywhere.

Validate inputs before mutating caller-owned state where feasible. If an operation can fail after mutation starts, establish whether rollback, staged work, or explicitly documented partial progress is required. A correct exception does not establish a safe failure path: check the caller's data after the error too.

Preserve subprocess exit status and relevant stdout/stderr when interpreting external commands. Some tools use nonzero status to report findings; inspect the tool's contract rather than treating every nonzero status as an empty result or discarding its diagnostic output.

## Resource cost and determinism

When startup or a cheap operation is slow, inspect imports, constructors, and shared factories as well as the function body. Defer expensive optional resources when unused paths should not pay their cost, but first check initialization side effects, failure timing, concurrency, ownership, and cleanup. Process-wide caching is a design choice with memory and state consequences, not a default cleanup.

Measure cold startup in a fresh process separately from repeated calls in a warm process. Benchmark equivalent inputs and results before claiming a speedup. Do not add laziness, caching, async, or a library replacement solely because it appears in a performance checklist.

When stable serialized output is required, inspect unordered inputs and establish an explicit ordering without changing meaningful sequence order. For stochastic APIs, prefer caller-controlled random state where practical; account for every random generator involved and avoid resetting global generators inside helpers.

## Examples

Default only when absent; an explicit empty selection must remain empty:

```python
def select_columns(frame, columns=None):
    if columns is None:
        columns = ["sample_id", "concentration_mg_l"]
    return frame.loc[:, columns]
```

This avoids both `columns=[]` as shared default state and `columns or defaults` as an unintended override. This example assumes pandas is already in use; follow the project's annotation conventions.

Handle a documented optional file without turning malformed JSON into a successful default:

```python
import json


def load_optional_config(path):
    try:
        with open(path, encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError:
        return {}
```

Here absence explicitly means an empty configuration. JSON decoding and permission errors propagate. If the application's contract requires configuration, missing files must also fail.

## Verification

Use the repository's interpreter, environment manager, test runner, and existing configuration. Run focused behavioral tests for changed contracts: optional versus empty inputs, malformed input, repeat calls where state could leak, and shape/key invariants where data operations changed.

Run applicable configured lint, formatting, and type checks.

For distribution changes, inspect the built wheel's modules, data files, and declared entry points. Smoke-test a non-editable installation in an isolated environment from outside the checkout, verifying a real public operation. An editable install, successful top-level import, or metadata check alone cannot establish that the distributed package is usable. Do not publish as part of verification unless publishing was requested.

When relying on a configured lint or validation rule for a specific guarantee, check that the relevant violation is actually detected in a disposable example. Investigate duplicate definitions after overlapping edits, allowing intentional overloads and registrations; do not change linter configuration merely to copy a reference's settings.


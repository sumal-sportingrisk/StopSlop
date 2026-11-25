# Test quality in Python and R

Read for test reviews or substantive test changes. Match the repository's framework, installed version, and existing fixture conventions.

## Check the contract, then the implementation

Read changed tests and the relevant requirements, then compare them with production code and related tests. Ask what defect each test would catch and whether harmless internal restructuring would break it. A helper's name appearing in a test is not itself a defect; assertions coupled to an incidental internal call sequence often are.

Check observable consequences beyond the return value when relevant: persisted state, output files, unchanged inputs, cleanup after failure, or results visible to other callers. Include the failure class and meaningful diagnostic details where those are part of the contract. Do not require exact incidental wording for every exception.

Inspect assertions for false success: an assertion inside a conditional that may never run, an exception handler that catches assertion failures, a test that checks only that something ran, or expected values computed with the same algorithm as the implementation. Use an independently established example, invariant, or reference result instead.

Choose regression fixtures where the old and intended behavior disagree: non-flat ordered values for first/last errors, multiple pages for pagination, and distinct groups for grouped calculations. Where useful and safe, try a focused regression test against the old behavior in a disposable copy and confirm that it fails for the intended reason. This is targeted evidence, not a requirement to install a mutation-testing framework or edit unrelated working changes.

For numerical tests, make the tolerance tight enough to reject the defect. An absolute tolerance can hide underflow of a tiny nonzero result to zero; use a magnitude-aware error budget and a separate zero case when that distinction matters. An equality between two paths alone can pass when both paths are wrong, so pair relationship checks with an independent invariant or known result when needed.

## State and fixtures

Make required setup visible in the test or an understandable fixture. Create temporary files and restore modified options, environment variables, random state, and global bindings at the appropriate scope, including when a test fails. Tests should not depend on execution order or a developer's working directory, credentials, or previously created files.

In Python, use the project's fixture and cleanup mechanisms. In R, scoped helpers from withr are useful when already available; base cleanup is also appropriate.

Simple repeated setup can be clearer than a generic fixture builder. Extract setup when it centralizes a meaningful contract or removes maintenance friction. Parameterized cases, loops over well-defined cases, and multi-step integration tests can be valid; do not split them merely to satisfy a fixed test shape.

## Mocks and integration

Mock or stub at a real external boundary when isolation matters. Keep the transformation or decision under test real. A test that mocks the function it claims to verify provides no evidence for that function. Check that fake responses still match the actual dependency contract; use a focused integration test when a mock cannot establish it.

Verify interactions when the interaction is the required behavior, such as an external write or notification. Avoid asserting every internal helper call. Do not create an adapter purely to reduce a mock count, or replace a useful filesystem/database test solely to reach an arbitrary speed target.

## Expectations and snapshots

Prefer expectations that explain the failed contract: values, dimensions, types, condition classes, or numerical bounds. Boolean expectations are appropriate for boolean contracts. Choose exact or approximate comparison based on semantics, including attributes, missingness, ordering, and floating-point tolerance.

Use snapshots when reviewed text or presentation is the contract, such as CLI output or a complex diagnostic. Pair them with behavioral assertions when needed. Do not snapshot entire analytical objects as a substitute for checking their meaning, and do not accept changed snapshots merely to make tests green.

For R, inspect the testthat version and edition before selecting helpers. Respect existing fixture layout and package-aware execution. A successful suite is evidence for the cases it exercises, not proof that every path or external consumer works.

## Report

Prioritize tests that can pass despite wrong behavior, hidden state dependencies, and missing checks for material side effects. Cite the location, missed failure, and smallest useful improvement. Distinguish a missing regression test for a real changed contract from speculative coverage expansion.


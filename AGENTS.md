# Working in SlopStop

This repository contains distributable skills and evaluator-owned fixtures. Keep skill instructions concise and self-contained; human source credits belong in docs/references.md. Keep grading keys and expected outcomes outside `plugin/`; only `plugin/` is installed by the marketplace.

- For code changes, read `plugin/skills/slopstop-python-r/SKILL.md` and the relevant language reference.
- For security-relevant changes, read `plugin/skills/slopstop-security/SKILL.md`; use local fixtures and preserve access controls.
- For documentation changes, read `plugin/skills/slopstop-docs/SKILL.md`.
- Preserve intentional defects in `evals/cases/*/fixture/`. A failing initial fixture is not a production bug to clean up.
- For evaluations, use fresh prepared workspaces. Do not pass private grading keys or this source checkout to the evaluated agent. Keep baseline and skill conditions comparable.

Run the relevant checks described in docs/development.md. Do not weaken checks, fabricate results, or install skills into unrelated repositories. Live accounts, publishing, and deployments require authorization for those actions.

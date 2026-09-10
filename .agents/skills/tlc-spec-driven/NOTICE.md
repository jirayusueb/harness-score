# Upstream provenance and local changes

This directory vendors `tlc-spec-driven` 3.3.0 from
[`tech-leads-club/agent-skills`](https://github.com/tech-leads-club/agent-skills),
source commit `e7baf4217e57bbcd9cdddfa830546c6a013db845` (2026-09-09).

The skill content is by Felipe Rodrigues and Tech Leads Club and is licensed
under CC-BY-4.0. The bundled Python source is covered by the upstream MIT
license. See [LICENSE](LICENSE) for the upstream licensing notice.

## Harness Score patches

The vendored copy includes two local parser corrections and regression tests:

- `validate_spec.py` inspects acceptance criteria produced by the documented
  template, including its parenthetical header and blank line.
- `validate_tasks.py` derives phase membership from execution-plan diagrams,
  so a task cannot silently depend on a later phase.

These cases were reported upstream in
[`tech-leads-club/agent-skills#162`](https://github.com/tech-leads-club/agent-skills/issues/162).
Run `python -m unittest discover -s .agents/skills/tlc-spec-driven/tests -v`
after every upstream update and remove the patches only after the upstream
regressions pass unchanged.

"""Regression tests for Harness Score's vendored tlc-spec-driven validators."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / "scripts"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_spec = load_module("validate_spec")
validate_tasks = load_module("validate_tasks")


class ValidatorRegressionTests(unittest.TestCase):
    def test_spec_validator_inspects_template_acceptance_criteria(self):
        document = """# Reset Specification

## Problem Statement

Reset behavior needs a precise contract.

## Out of Scope

Nothing else.

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Delivery | Local only | Keeps the test isolated | y |

**Open questions:** none

## User Stories

### P1: Reset

**Acceptance Criteria** (each line is one EARS pattern):

1. The reset flow should be nice and easy to use

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| RESET-01 | P1: Reset | Design | Pending |
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spec.md"
            path.write_text(document, encoding="utf-8")
            errors, _warnings = validate_spec.check(path)

        self.assertTrue(
            any("acceptance criterion has no SHALL" in error for error in errors),
            errors,
        )

    def test_tasks_validator_detects_forward_phase_dependency_from_plan(self):
        document = """# Reset Tasks

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Scripts | unit | Validator regressions | tests/*.py | python -m unittest |

## Gate Check Commands

| Gate Level | When to Use | Command |
| --- | --- | --- |
| Quick | Unit tests | python -m unittest |

## Execution Plan

### Phase 1: Foundation

```
T1 -> T2
```

### Phase 2: Integration

```
T3 -> T4
```

## Task Breakdown

### T1: First task

**Where**: `one.py`
**Depends on**: T4
**Tests**: unit
**Gate**: quick

### T2: Second task

**Where**: `two.py`
**Depends on**: T1
**Tests**: unit
**Gate**: quick

### T3: Third task

**Where**: `three.py`
**Depends on**: T2
**Tests**: unit
**Gate**: quick

### T4: Fourth task

**Where**: `four.py`
**Depends on**: T3
**Tests**: unit
**Gate**: quick
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.md"
            path.write_text(document, encoding="utf-8")
            errors, _warnings = validate_tasks.check(path)

        self.assertIn(
            "T1 (phase 1) depends on T4 (phase 2) - dependencies must point backward or within the same phase",
            errors,
        )


if __name__ == "__main__":
    unittest.main()

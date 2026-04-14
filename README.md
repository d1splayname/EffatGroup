# EffatGroup

COMP 5710 Group Project for group `EffatGroup`

## Group Members

- Joshua Chen
- Kyler Swindle
- Ayush Patel

## Overview

This project implements Verification & Validation for atomic rules extracted from `21 CFR 117.130` using Python scripts, JSON artifacts, and GitHub Actions.

## Engineering Highlights

- Automated CFR-to-JSON pipeline for regulatory requirement extraction
- Deterministic parent-child requirement mapping for atomic rules
- Minimal test-case generation for requirement coverage
- Verification and validation gates in CI
- Forensick evidence artifacts for auditability and debugging

## What This Project Does

1. Parses `inputs/21_CFR_117.130.md` into atomic CFR requirements.
2. Selects 10 atomic rules for the project scope.
3. Generates `requirements.json`.
4. Generates `expected_structure.json`.
5. Generates `test_cases.json`.
6. Verifies requirement and test-case completeness.
7. Validates requirement structure against expected parent-child mappings.
8. Runs the checks automatically in GitHub Actions.

## Repository Layout

```text
EffatGroup/
|-- .github/workflows/cfr-vv.yml
|-- inputs/
|   |-- 21_CFR_117.130.md
|   `-- README.md
|-- scripts/
|   |-- parse_cfr.py
|   |-- generate_expected_structure.py
|   |-- generate_test_cases.py
|   |-- verification.py
|   `-- validation.py
|-- requirements.json
|-- reports/forensick/
|-- expected_structure.json
|-- test_cases.json
`-- README.md
```

## Selected Atomic Rules

The 10 selected rules are:

- `(a)(1)`
- `(a)(2)`
- `(b)(1)(i)`
- `(b)(1)(ii)`
- `(b)(1)(iii)`
- `(b)(2)(i)`
- `(b)(2)(ii)`
- `(b)(2)(iii)`
- `(c)(1)(i)`
- `(c)(1)(ii)`

## Quick Start

Run the project locally with:

```powershell
python scripts/parse_cfr.py
python scripts/generate_expected_structure.py
python scripts/generate_test_cases.py
python scripts/verification.py
python scripts/validation.py
python scripts/generate_forensick_report.py
```

## Current Status

The current local build has:

- generated `requirements.json`
- generated `expected_structure.json`
- generated `test_cases.json`
- passed `verification.py`
- passed `validation.py`

## Forensick Examples

Examples of forensic-style signals that can be shown in this project:

- Missing requirement
- Missing test case
- Invalid requirement ID
- Unexpected structure entry
- CI pass/fail evidence

## Forensick Integration

The project now generates evidence artifacts in `reports/forensick/`:

- `verification_report.json`
- `validation_report.json`
- `summary.json`
- `summary.md`

The five integrated forensic checks are:

- Missing requirement or test-case fields
- Missing test coverage for selected rules
- Invalid requirement or test-case identifier formats
- Unexpected or unmapped parent-child structure
- CI-ready pass/fail status from verification and validation

## Resume Framing

This project is strong enough to describe as:

`Built a Python and GitHub Actions pipeline that converts CFR regulatory text into atomic requirements, auto-generates validation artifacts, and produces forensic audit reports for compliance-focused verification and validation.`

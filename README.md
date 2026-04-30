# EffatGroup

COMP 5710/6710 Software Quality Assurance group project for `EffatGroup`.

## Team Members

- Joshua Chen
- Kyler Swindle
- Ayush Patel

## Objective

This project implements a small Verification and Validation (V&V) pipeline for regulatory requirements extracted from `21 CFR 117.130`.

The project demonstrates how CFR regulatory text can be converted into atomic software requirements, mapped into an expected parent-child structure, covered by generated test cases, and checked automatically through local scripts and GitHub Actions.

## Project Scope

The project focuses on 10 selected atomic rules from `21 CFR 117.130`:

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

## What the Pipeline Does

1. Parses `inputs/21_CFR_117.130.md` into atomic CFR requirements.
2. Generates `requirements.json`.
3. Generates `expected_structure.json`.
4. Generates `test_cases.json`.
5. Verifies that selected rules have required fields and test coverage.
6. Validates requirement structure against the expected parent-child mapping.
7. Generates forensic-style evidence reports in `reports/forensick/`.
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
|   |-- generate_forensick_report.py
|   |-- verification.py
|   `-- validation.py
|-- requirements.json
|-- expected_structure.json
|-- test_cases.json
|-- reports/
|   `-- forensick/
|       |-- verification_report.json
|       |-- validation_report.json
|       |-- summary.json
|       `-- summary.md
`-- README.md
```

## Requirements

- Python 3.8 or newer
- Git
- No external Python packages are required unless future scripts are updated to add dependencies.

## Reproduce Locally on macOS / Linux

From a terminal:

```bash
git clone <repository-url>
cd EffatGroup

python3 scripts/parse_cfr.py
python3 scripts/generate_expected_structure.py
python3 scripts/generate_test_cases.py
python3 scripts/verification.py
python3 scripts/validation.py
python3 scripts/generate_forensick_report.py
```

If your system maps Python 3 to `python` instead of `python3`, use:

```bash
python scripts/parse_cfr.py
python scripts/generate_expected_structure.py
python scripts/generate_test_cases.py
python scripts/verification.py
python scripts/validation.py
python scripts/generate_forensick_report.py
```

## Reproduce Locally on Windows

From PowerShell:

```powershell
git clone <repository-url>
cd EffatGroup

py scripts\parse_cfr.py
py scripts\generate_expected_structure.py
py scripts\generate_test_cases.py
py scripts\verification.py
py scripts\validation.py
py scripts\generate_forensick_report.py
```

Alternative Windows command if `python` is configured:

```powershell
python scripts\parse_cfr.py
python scripts\generate_expected_structure.py
python scripts\generate_test_cases.py
python scripts\verification.py
python scripts\validation.py
python scripts\generate_forensick_report.py
```

## Expected Outputs

After running the scripts, the repository should contain or update:

```text
requirements.json
expected_structure.json
test_cases.json
reports/forensick/verification_report.json
reports/forensick/validation_report.json
reports/forensick/summary.json
reports/forensick/summary.md
```

The verification and validation scripts should complete without errors when the generated artifacts are consistent.

## Verification and Validation Checks

The local and CI checks verify:

- Required requirement fields are present.
- Selected rules have generated test coverage.
- Requirement and test-case identifiers follow the expected format.
- Parent-child requirement mappings match `expected_structure.json`.
- Verification and validation status can be captured as forensic evidence.

## GitHub Actions

The workflow file is located at:

```text
.github/workflows/cfr-vv.yml
```

On each configured GitHub Actions run, the project regenerates artifacts and runs the verification and validation checks. A passing workflow indicates that the repository artifacts are reproducible and satisfy the current project V&V checks.

## Current Status

The current build:

- Generates `requirements.json`.
- Generates `expected_structure.json`.
- Generates `test_cases.json`.
- Passes `verification.py`.
- Passes `validation.py`.
- Generates forensic evidence reports under `reports/forensick/`.

## Notes

This project is intentionally small and deterministic so that the generated artifacts can be reproduced locally and in CI. The purpose is to demonstrate SQA concepts including requirement extraction, verification, validation, test coverage, CI automation, and forensic-style audit evidence.

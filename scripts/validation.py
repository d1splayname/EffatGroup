import json
import re
import sys
from collections import Counter
from pathlib import Path

from forensick_utils import ordered_counts, utc_timestamp, write_json_report


PARENT_ID_RE = re.compile(r"REQ-CFR-\d{3}$")
SUFFIX_RE = re.compile(r"[A-Z]+$")


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def add_failure(failures: list[str], issue_counts: Counter, category: str, message: str) -> None:
    failures.append(message)
    issue_counts[category] += 1


def write_report(status: str, failures: list[str], issue_counts: Counter, requirements: list[dict], expected_structure: dict) -> None:
    report = {
        "report_name": "validation_report",
        "generated_at_utc": utc_timestamp(),
        "status": status,
        "totals": {
            "requirements": len(requirements),
            "parents": len(expected_structure),
            "failures": len(failures),
        },
        "issue_counts": ordered_counts(
            {
                "empty_expected_structure": issue_counts["empty_expected_structure"],
                "invalid_parent_ids": issue_counts["invalid_parent_ids"],
                "invalid_suffixes": issue_counts["invalid_suffixes"],
                "missing_requirements_from_structure": issue_counts["missing_requirements_from_structure"],
                "unexpected_or_unmapped_structure": issue_counts["unexpected_or_unmapped_structure"],
            }
        ),
        "failures": failures,
    }
    report_path = write_json_report("validation_report.json", report)
    print(f"Forensick artifact written: {report_path}")


def main():
    requirements = load_json("requirements.json")
    expected_structure = load_json("expected_structure.json")

    if not requirements and not expected_structure:
        write_report("skipped", [], Counter(), requirements, expected_structure)
        print("Validation skipped: requirements.json and expected_structure.json are empty.")
        sys.exit(0)

    actual_ids = {requirement["requirement_id"] for requirement in requirements}
    failures: list[str] = []
    issue_counts: Counter = Counter()

    if requirements and not expected_structure:
        add_failure(
            failures,
            issue_counts,
            "empty_expected_structure",
            "expected_structure.json is empty while requirements.json contains requirements.",
        )

    for parent_id, suffixes in expected_structure.items():
        if not PARENT_ID_RE.fullmatch(parent_id):
            add_failure(
                failures,
                issue_counts,
                "invalid_parent_ids",
                f"Invalid parent ID in expected_structure.json: {parent_id}",
            )

        if not isinstance(suffixes, list) or not suffixes:
            add_failure(
                failures,
                issue_counts,
                "invalid_suffixes",
                f"Parent {parent_id} must map to a non-empty list of child letters.",
            )
            continue

        for suffix in suffixes:
            if not SUFFIX_RE.fullmatch(suffix):
                add_failure(
                    failures,
                    issue_counts,
                    "invalid_suffixes",
                    f"Invalid child suffix '{suffix}' under parent {parent_id}",
                )
                continue

            requirement_id = f"{parent_id}{suffix}"
            if requirement_id not in actual_ids:
                add_failure(
                    failures,
                    issue_counts,
                    "missing_requirements_from_structure",
                    f"Missing requirement from expected structure: {requirement_id}",
                )

    for requirement_id in actual_ids:
        matched_parent = next((parent for parent in expected_structure if requirement_id.startswith(parent)), None)
        if not matched_parent:
            add_failure(
                failures,
                issue_counts,
                "unexpected_or_unmapped_structure",
                f"Requirement not mapped by expected_structure.json: {requirement_id}",
            )
            continue
        if matched_parent:
            suffix = requirement_id[len(matched_parent) :]
            if suffix not in expected_structure[matched_parent]:
                add_failure(
                    failures,
                    issue_counts,
                    "unexpected_or_unmapped_structure",
                    f"Unexpected requirement not listed in expected_structure.json: {requirement_id}",
                )

    if failures:
        write_report("failed", failures, issue_counts, requirements, expected_structure)
        print("Validation FAILED:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    write_report("passed", failures, issue_counts, requirements, expected_structure)
    print("Validation passed: requirements.json matches expected_structure.json.")
    sys.exit(0)


if __name__ == "__main__":
    main()

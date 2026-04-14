import json
import re
import sys
from collections import Counter
from pathlib import Path

from forensick_utils import ordered_counts, utc_timestamp, write_json_report


REQUIREMENT_ID_RE = re.compile(r"REQ-CFR-\d{3}[A-Z]+$")
PARENT_ID_RE = re.compile(r"REQ-CFR-\d{3}$")
TEST_CASE_ID_RE = re.compile(r"TC-\d{3}$")


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def add_failure(failures: list[str], issue_counts: Counter, category: str, message: str) -> None:
    failures.append(message)
    issue_counts[category] += 1


def write_report(status: str, failures: list[str], issue_counts: Counter, requirements: list[dict], test_cases: list[dict]) -> None:
    report = {
        "report_name": "verification_report",
        "generated_at_utc": utc_timestamp(),
        "status": status,
        "totals": {
            "requirements": len(requirements),
            "test_cases": len(test_cases),
            "failures": len(failures),
        },
        "issue_counts": ordered_counts(
            {
                "duplicate_requirement_ids": issue_counts["duplicate_requirement_ids"],
                "duplicate_test_case_ids": issue_counts["duplicate_test_case_ids"],
                "invalid_identifier_format": issue_counts["invalid_identifier_format"],
                "missing_requirement_fields": issue_counts["missing_requirement_fields"],
                "missing_test_case_fields": issue_counts["missing_test_case_fields"],
                "missing_test_coverage": issue_counts["missing_test_coverage"],
                "orphan_test_cases": issue_counts["orphan_test_cases"],
                "parent_child_mismatches": issue_counts["parent_child_mismatches"],
            }
        ),
        "failures": failures,
    }
    report_path = write_json_report("verification_report.json", report)
    print(f"Forensick artifact written: {report_path}")


def main():
    requirements = load_json("requirements.json")
    test_cases = load_json("test_cases.json")

    if not requirements and not test_cases:
        write_report("skipped", [], Counter(), requirements, test_cases)
        print("Verification skipped: requirements.json and test_cases.json are empty.")
        sys.exit(0)

    failures: list[str] = []
    issue_counts: Counter = Counter()
    requirement_ids: set[str] = set()
    test_case_ids: set[str] = set()
    covered_requirement_ids: set[str] = set()

    for requirement in requirements:
        for field in ["requirement_id", "parent_requirement_id", "source_section", "description"]:
            if field not in requirement:
                add_failure(
                    failures,
                    issue_counts,
                    "missing_requirement_fields",
                    f"Requirement missing field '{field}': {requirement}",
                )

        rid = requirement.get("requirement_id", "")
        parent_id = requirement.get("parent_requirement_id", "")
        description = requirement.get("description", "")
        source_section = requirement.get("source_section", "")

        if rid:
            if not REQUIREMENT_ID_RE.fullmatch(rid):
                add_failure(
                    failures,
                    issue_counts,
                    "invalid_identifier_format",
                    f"Invalid requirement_id format: {rid}",
                )
            if rid in requirement_ids:
                add_failure(failures, issue_counts, "duplicate_requirement_ids", f"Duplicate requirement_id: {rid}")
            requirement_ids.add(rid)

        if parent_id and not PARENT_ID_RE.fullmatch(parent_id):
            add_failure(
                failures,
                issue_counts,
                "invalid_identifier_format",
                f"Invalid parent_requirement_id format: {parent_id}",
            )

        if rid and parent_id and not rid.startswith(parent_id):
            add_failure(
                failures,
                issue_counts,
                "parent_child_mismatches",
                f"Parent-child mismatch: {rid} does not start with {parent_id}",
            )

        if not str(description).strip():
            add_failure(failures, issue_counts, "missing_requirement_fields", f"Empty description for requirement: {rid}")

        if not str(source_section).strip():
            add_failure(failures, issue_counts, "missing_requirement_fields", f"Empty source_section for requirement: {rid}")

    for test_case in test_cases:
        for field in ["test_case_id", "requirement_id", "description", "input_data", "expected_output"]:
            if field not in test_case:
                add_failure(
                    failures,
                    issue_counts,
                    "missing_test_case_fields",
                    f"Test case missing field '{field}': {test_case}",
                )

        test_case_id = test_case.get("test_case_id", "")
        requirement_id = test_case.get("requirement_id", "")

        if test_case_id:
            if not TEST_CASE_ID_RE.fullmatch(test_case_id):
                add_failure(
                    failures,
                    issue_counts,
                    "invalid_identifier_format",
                    f"Invalid test_case_id format: {test_case_id}",
                )
            if test_case_id in test_case_ids:
                add_failure(failures, issue_counts, "duplicate_test_case_ids", f"Duplicate test_case_id: {test_case_id}")
            test_case_ids.add(test_case_id)

        if requirement_id:
            covered_requirement_ids.add(requirement_id)
            if requirement_ids and requirement_id not in requirement_ids:
                add_failure(
                    failures,
                    issue_counts,
                    "orphan_test_cases",
                    f"Test case references unknown requirement_id: {requirement_id}",
                )

    for rid in sorted(requirement_ids):
        if rid not in covered_requirement_ids:
            add_failure(failures, issue_counts, "missing_test_coverage", f"No test case found for requirement: {rid}")

    if failures:
        write_report("failed", failures, issue_counts, requirements, test_cases)
        print("Verification FAILED:")
        for failure in failures:
            print(f"- {failure}")
        sys.exit(1)

    write_report("passed", failures, issue_counts, requirements, test_cases)
    print("Verification passed: requirements and test cases are structurally complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()


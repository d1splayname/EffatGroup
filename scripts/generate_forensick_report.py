import json
from collections import OrderedDict
from pathlib import Path

from forensick_utils import utc_timestamp, write_json_report


VERIFICATION_PATH = Path("reports/forensick/verification_report.json")
VALIDATION_PATH = Path("reports/forensick/validation_report.json")


def load_report(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing forensic report: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_summary(verification: dict, validation: dict) -> dict:
    verification_counts = verification["issue_counts"]
    validation_counts = validation["issue_counts"]

    checks = OrderedDict(
        [
            (
                "missing_requirement_or_test_fields",
                verification_counts["missing_requirement_fields"] + verification_counts["missing_test_case_fields"],
            ),
            ("missing_test_coverage", verification_counts["missing_test_coverage"]),
            ("invalid_identifier_format", verification_counts["invalid_identifier_format"]),
            ("unexpected_or_unmapped_structure", validation_counts["unexpected_or_unmapped_structure"]),
            (
                "ci_ready_status",
                int(verification["status"] == "passed" and validation["status"] == "passed"),
            ),
        ]
    )

    overall_status = "passed" if verification["status"] == "passed" and validation["status"] == "passed" else "failed"

    return {
        "report_name": "forensick_summary",
        "generated_at_utc": utc_timestamp(),
        "overall_status": overall_status,
        "checks": checks,
        "source_reports": [str(VERIFICATION_PATH), str(VALIDATION_PATH)],
        "highlights": [
            "Missing requirement or test-case fields",
            "Missing test coverage for selected atomic rules",
            "Invalid requirement or test-case identifier format",
            "Unexpected or unmapped requirement structure",
            "CI-ready pass/fail status based on verification and validation",
        ],
    }


def write_markdown(summary: dict) -> Path:
    lines = [
        "# Forensick Summary",
        "",
        f"- Generated: {summary['generated_at_utc']}",
        f"- Overall status: {summary['overall_status']}",
        "",
        "## Integrated Checks",
        "",
    ]

    for name, value in summary["checks"].items():
        lines.append(f"- `{name}`: {value}")

    lines.extend(
        [
            "",
            "## Evidence Files",
            "",
        ]
    )

    for report_path in summary["source_reports"]:
        lines.append(f"- `{report_path}`")

    markdown_path = Path("reports/forensick/summary.md")
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return markdown_path


def main():
    verification = load_report(VERIFICATION_PATH)
    validation = load_report(VALIDATION_PATH)
    summary = build_summary(verification, validation)
    write_json_report("summary.json", summary)
    markdown_path = write_markdown(summary)
    print(f"Wrote combined forensick summary to reports/forensick/summary.json and {markdown_path}.")


if __name__ == "__main__":
    main()

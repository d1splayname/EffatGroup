import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path


REPORTS_DIR = Path("reports/forensick")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_reports_dir() -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return REPORTS_DIR


def write_json_report(filename: str, payload: dict) -> Path:
    report_dir = ensure_reports_dir()
    report_path = report_dir / filename
    report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return report_path


def ordered_counts(counts: dict[str, int]) -> OrderedDict[str, int]:
    return OrderedDict((key, counts[key]) for key in sorted(counts))


"""Validate required pipeline inputs before generation.

Usage:
    python scripts/validate_inputs.py

Checks:
- job_description.md is present and non-empty.
- profile.md is present and appears to contain meaningful structured content.
- tracker.md has the required table header columns.
"""

from __future__ import annotations

import os
import sys
from typing import List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JOB_DESCRIPTION = os.path.join(PROJECT_ROOT, "job_description.md")
PROFILE = os.path.join(PROJECT_ROOT, "profile.md")
TRACKER = os.path.join(PROJECT_ROOT, "tracker.md")

REQUIRED_TRACKER_HEADER = "| Job Title | Company | Applied Date | Status | Role Type | Notes |"


def _read_text(path: str) -> str:
    if not os.path.isfile(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def validate() -> List[str]:
    errors: List[str] = []

    job_text = _read_text(JOB_DESCRIPTION).strip()
    if not job_text:
        errors.append("job_description.md is missing or empty.")

    profile_text = _read_text(PROFILE)
    profile_lines = [line.strip() for line in profile_text.splitlines() if line.strip()]
    profile_heading_count = sum(1 for line in profile_lines if line.startswith("## "))
    if not profile_text.strip():
        errors.append("profile.md is missing or empty.")
    elif profile_heading_count < 3:
        errors.append("profile.md appears incomplete (expected multiple structured sections).")

    tracker_text = _read_text(TRACKER)
    if not tracker_text.strip():
        errors.append("tracker.md is missing or empty.")
    elif REQUIRED_TRACKER_HEADER not in tracker_text:
        errors.append(
            "tracker.md does not contain the required table header: "
            "| Job Title | Company | Applied Date | Status | Role Type | Notes |"
        )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Preflight validation failed:")
        for idx, err in enumerate(errors, start=1):
            print(f"{idx}. {err}")
        return 1

    print("Preflight validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

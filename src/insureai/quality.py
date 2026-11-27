"""Small, framework-neutral data quality result model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class QualityResult:
    check_name: str
    passed: bool
    failing_count: int
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_required_columns(actual_columns: Iterable[str], required_columns: Iterable[str]) -> QualityResult:
    """Check that all configured columns exist in the incoming dataset."""
    missing = sorted(set(required_columns) - set(actual_columns))
    return QualityResult(
        check_name="required_columns",
        passed=not missing,
        failing_count=len(missing),
        message="All required columns are present." if not missing else f"Missing columns: {', '.join(missing)}",
    )


def validate_primary_key_values(rows: Iterable[dict[str, Any]], primary_key: str) -> QualityResult:
    """Check for null and duplicate primary-key values in an in-memory batch."""
    seen: set[Any] = set()
    null_count = 0
    duplicate_count = 0

    for row in rows:
        value = row.get(primary_key)
        if value is None or value == "":
            null_count += 1
        elif value in seen:
            duplicate_count += 1
        else:
            seen.add(value)

    failures = null_count + duplicate_count
    return QualityResult(
        check_name="primary_key_integrity",
        passed=failures == 0,
        failing_count=failures,
        message=f"{null_count} null/blank and {duplicate_count} duplicate key values.",
    )

from insureai.quality import validate_primary_key_values, validate_required_columns


def test_required_columns_pass():
    result = validate_required_columns(["claim_id", "status"], ["claim_id"])
    assert result.passed
    assert result.failing_count == 0


def test_required_columns_fail():
    result = validate_required_columns(["status"], ["claim_id"])
    assert not result.passed
    assert result.failing_count == 1


def test_primary_key_detects_null_and_duplicates():
    rows = [
        {"claim_id": "C1"},
        {"claim_id": "C1"},
        {"claim_id": None},
        {"claim_id": "C2"},
    ]
    result = validate_primary_key_values(rows, "claim_id")
    assert not result.passed
    assert result.failing_count == 2
    assert "1 null/blank" in result.message

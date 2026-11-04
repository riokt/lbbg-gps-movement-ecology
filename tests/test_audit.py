from pathlib import Path

from bird_migration.audit import audit_gps


def test_selected_gps_file_has_expected_audit_fields():
    path = Path("data/raw/LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz")
    result = audit_gps(path)
    assert result["rows"] == 441979
    assert result["individual_count"] == 20
    assert result["duplicate_event_ids"] == 0
    assert result["invalid_coordinates"] == 0
    assert result["timestamp_parse_failures"] == 0

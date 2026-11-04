"""Create a reproducible, non-destructive audit of the selected GPS snapshot."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
REPORTS = ROOT / "reports"
GPS = RAW / "LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz"
REFERENCE = RAW / "LBBG_SCHIERMONNIKOOG-reference-data.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_gps(path: Path) -> dict:
    rows = 0
    ids: Counter[str] = Counter()
    columns: list[str] = []
    missing: Counter[str] = Counter()
    duplicates = 0
    seen_events: set[str] = set()
    invalid_coordinates = 0
    timestamps: list[str] = []
    latitudes: list[float] = []
    longitudes: list[float] = []
    with gzip.open(path, "rt", newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        columns = reader.fieldnames or []
        for row in reader:
            rows += 1
            for key, value in row.items():
                if value in (None, ""):
                    missing[key] += 1
            event_id = row.get("event-id", "")
            if event_id in seen_events:
                duplicates += 1
            seen_events.add(event_id)
            ids[row["individual-local-identifier"]] += 1
            timestamps.append(row["timestamp"])
            lat = float(row["location-lat"])
            lon = float(row["location-long"])
            latitudes.append(lat)
            longitudes.append(lon)
            invalid_coordinates += int(not (-90 <= lat <= 90 and -180 <= lon <= 180))
    return {
        "rows": rows,
        "columns": columns,
        "individual_count": len(ids),
        "rows_per_individual": dict(sorted(ids.items())),
        "missing_values": dict(sorted(missing.items())),
        "duplicate_event_ids": duplicates,
        "invalid_coordinates": invalid_coordinates,
        "timestamp_parse_failures": sum(
            1
            for value in timestamps
            if _parse_timestamp(value) is None
        ),
        "temporal_coverage_utc": {"min": min(timestamps), "max": max(timestamps)},
        "coordinate_bounds_wgs84": {
            "latitude_min": min(latitudes),
            "latitude_max": max(latitudes),
            "longitude_min": min(longitudes),
            "longitude_max": max(longitudes),
        },
    }


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=UTC)
    except ValueError:
        return None


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    with (RAW / "datapackage.json").open(encoding="utf-8") as stream:
        package = json.load(stream)
    audit = audit_gps(GPS)
    audit.update(
        {
            "generated_utc": datetime.now(UTC).isoformat(),
            "dataset": "LBBG_SCHIERMONNIKOOG",
            "record_doi": "10.5281/zenodo.20706447",
            "licence": "CC0",
            "files": {
                path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
                for path in RAW.iterdir()
                if path.is_file()
            },
            "research_feasibility": {
                "proceed": True,
                "scope": "Audit GPS fixes first; derive movement steps only after reviewing sampling and outlier fields.",
                "supported_question": "How do GPS-derived location and movement patterns vary by time of day and individual in the publicly available 2017 sample?",
                "limitations": [
                    "This snapshot contains one public year, not the full study period.",
                    "The record notes that data collected since 2021 are not public.",
                    "Raw GPS fixes are repeated observations within individuals.",
                    "No causal environmental interpretation is supported by this audit.",
                ],
            },
            "datapackage_resource_count": len(package["resources"]),
        }
    )
    (REPORTS / "dataset_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    mappings = [
        ("individual_id", "individual-local-identifier", "Unique individual identifier"),
        ("timestamp", "timestamp", "UTC or GPS-time sensor timestamp"),
        ("latitude", "location-lat", "WGS84 latitude, decimal degrees"),
        ("longitude", "location-long", "WGS84 longitude, decimal degrees"),
        ("sensor_type", "sensor-type", "Sensor type; observed value is gps"),
        ("location_error_m", "location-error-numerical", "Numerical location uncertainty; documented by source"),
        ("ground_speed_m_s", "ground-speed", "Ground speed; source datapackage units"),
        ("height_m", "height-above-msl", "Height above mean sea level; source datapackage units"),
    ]
    with (REPORTS / "data_dictionary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["standardized_name", "source_column", "meaning"])
        writer.writerows(mappings)
    (REPORTS / "dataset_decision.md").write_text(
        "# Dataset decision\n\n"
        "Proceed with the Zenodo LBBG_SCHIERMONNIKOOG dataset for Milestone 01. "
        "The 2017 GPS file is downloadable and loadable, the record provides a data dictionary, "
        "and the licence is CC0. Limit the next stage to questions supported by GPS fixes and "
        "individual-level repeated-measures analysis.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

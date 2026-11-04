"""Reusable GPS sampling and movement-step calculations for Notebook 03."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd
from pyproj import Geod

WGS84_GEOD = Geod(ellps="WGS84")


def sort_fixes(fixes: pd.DataFrame) -> pd.DataFrame:
    """Return a stable individual/timestamp/event-sorted copy of GPS fixes."""

    required = {"individual_id", "timestamp_utc", "latitude", "longitude", "event_id"}
    missing = required.difference(fixes.columns)
    if missing:
        raise KeyError(f"Fix table is missing required columns: {sorted(missing)}")
    return fixes.sort_values(
        ["individual_id", "timestamp_utc", "event_id"], kind="mergesort"
    ).reset_index(drop=True)


def sampling_intervals(fixes: pd.DataFrame) -> pd.DataFrame:
    """Calculate consecutive within-individual elapsed times in seconds."""

    ordered = sort_fixes(fixes)
    intervals = ordered[["individual_id", "timestamp_utc", "event_id"]].copy()
    intervals["previous_timestamp_utc"] = intervals.groupby("individual_id")[
        "timestamp_utc"
    ].shift(1)
    intervals["previous_event_id"] = intervals.groupby("individual_id")["event_id"].shift(1)
    intervals["elapsed_time_seconds"] = (
        intervals["timestamp_utc"] - intervals["previous_timestamp_utc"]
    ).dt.total_seconds()
    return intervals


def evaluate_gap_thresholds(
    intervals: pd.Series, thresholds_seconds: Iterable[int]
) -> pd.DataFrame:
    """Report retained/excluded positive intervals for candidate gap thresholds."""

    positive = intervals.dropna().loc[lambda values: values > 0]
    rows = []
    for threshold in thresholds_seconds:
        retained = int((positive <= threshold).sum())
        excluded = int((positive > threshold).sum())
        rows.append(
            {
                "threshold_seconds": int(threshold),
                "threshold_hours": threshold / 3600,
                "positive_intervals": len(positive),
                "retained_steps": retained,
                "excluded_long_gap_steps": excluded,
                "retained_fraction": retained / len(positive),
            }
        )
    return pd.DataFrame(rows)


def derive_step_candidates(fixes: pd.DataFrame, gap_threshold_seconds: int) -> pd.DataFrame:
    """Build consecutive within-individual geodesic step candidates.

    The returned table contains terminal records with ``no_next_fix`` as an
    exclusion reason, and all non-terminal pairs with invalid intervals,
    invalid coordinates, or gaps exceeding the selected threshold. It never
    connects different individuals.
    """

    ordered = sort_fixes(fixes)
    next_columns = [
        "individual_id",
        "event_id",
        "timestamp_utc",
        "latitude",
        "longitude",
        "ground_speed_source",
        "location_error_m",
        "height_above_msl",
        "gps:dop",
        "gps:satellite-count",
        "import-marked-outlier",
        "manually-marked-outlier",
        "visible",
    ]
    available_next_columns = [column for column in next_columns if column in ordered.columns]
    next_fixes = ordered.groupby("individual_id", sort=False)[available_next_columns].shift(-1)

    steps = pd.DataFrame(
        {
            "individual_id": ordered["individual_id"].astype("string"),
            "start_event_id": ordered["event_id"].astype("string"),
            "end_event_id": next_fixes["event_id"].astype("string"),
            "start_timestamp": ordered["timestamp_utc"],
            "end_timestamp": next_fixes["timestamp_utc"],
            "start_latitude": ordered["latitude"],
            "start_longitude": ordered["longitude"],
            "end_latitude": next_fixes["latitude"],
            "end_longitude": next_fixes["longitude"],
            "source_ground_speed_m_s": ordered.get("ground_speed_source"),
            "start_location_error_m": ordered.get("location_error_m"),
            "start_height_above_msl": ordered.get("height_above_msl"),
            "start_gps_dop": ordered.get("gps:dop"),
            "start_gps_satellite_count": ordered.get("gps:satellite-count"),
            "start_import_marked_outlier": ordered.get("import-marked-outlier"),
            "start_manually_marked_outlier": ordered.get("manually-marked-outlier"),
            "start_visible": ordered.get("visible"),
        }
    )
    steps["end_individual_id"] = next_fixes["individual_id"].astype("string")
    steps["elapsed_time_seconds"] = (
        steps["end_timestamp"] - steps["start_timestamp"]
    ).dt.total_seconds()
    steps["same_individual"] = steps["end_individual_id"].eq(steps["individual_id"])

    valid_coordinates = (
        steps["start_latitude"].between(-90, 90)
        & steps["start_longitude"].between(-180, 180)
        & steps["end_latitude"].between(-90, 90)
        & steps["end_longitude"].between(-180, 180)
    )
    valid_time = steps["elapsed_time_seconds"].notna() & (steps["elapsed_time_seconds"] > 0)
    valid_pair = steps["same_individual"] & valid_time & valid_coordinates

    steps["step_distance_m"] = np.nan
    valid_indices = steps.index[valid_pair]
    if len(valid_indices):
        _, _, distances = WGS84_GEOD.inv(
            steps.loc[valid_indices, "start_longitude"].to_numpy(),
            steps.loc[valid_indices, "start_latitude"].to_numpy(),
            steps.loc[valid_indices, "end_longitude"].to_numpy(),
            steps.loc[valid_indices, "end_latitude"].to_numpy(),
        )
        steps.loc[valid_indices, "step_distance_m"] = distances
    steps["average_speed_m_s"] = steps["step_distance_m"] / steps["elapsed_time_seconds"]
    steps["sampling_gap_flag"] = steps["elapsed_time_seconds"] > gap_threshold_seconds

    steps["step_exclusion_reason"] = ""
    steps.loc[steps["end_timestamp"].isna(), "step_exclusion_reason"] = "no_next_fix"
    steps.loc[
        steps["end_timestamp"].notna() & ~steps["same_individual"], "step_exclusion_reason"
    ] = "individual_boundary"
    steps.loc[
        steps["end_timestamp"].notna() & steps["same_individual"] & ~valid_time,
        "step_exclusion_reason",
    ] = "nonpositive_or_invalid_elapsed_time"
    steps.loc[
        steps["end_timestamp"].notna()
        & steps["same_individual"]
        & valid_time
        & ~valid_coordinates,
        "step_exclusion_reason",
    ] = "invalid_coordinate_pair"
    steps.loc[steps["sampling_gap_flag"], "step_exclusion_reason"] = "gap_exceeds_threshold"
    steps["step_retained"] = steps["step_exclusion_reason"].eq("")
    return steps


def add_review_flags(
    retained_steps: pd.DataFrame,
    distance_quantile: float = 0.999,
    speed_quantile: float = 0.999,
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Add transparent, descriptive review flags without removing rows."""

    steps = retained_steps.copy()
    distance_threshold = float(steps["step_distance_m"].quantile(distance_quantile))
    speed_threshold = float(steps["average_speed_m_s"].quantile(speed_quantile))
    steps["large_distance_review_flag"] = steps["step_distance_m"] > distance_threshold
    steps["high_speed_review_flag"] = steps["average_speed_m_s"] > speed_threshold
    steps["gps_dop_review_flag"] = pd.to_numeric(steps["start_gps_dop"], errors="coerce") > 5
    steps["low_satellite_count_review_flag"] = (
        pd.to_numeric(steps["start_gps_satellite_count"], errors="coerce") < 4
    )
    steps["any_review_flag"] = steps[
        [
            "large_distance_review_flag",
            "high_speed_review_flag",
            "gps_dop_review_flag",
            "low_satellite_count_review_flag",
        ]
    ].any(axis=1)
    return steps, {
        "distance_review_quantile": distance_quantile,
        "distance_review_threshold_m": distance_threshold,
        "speed_review_quantile": speed_quantile,
        "speed_review_threshold_m_s": speed_threshold,
    }

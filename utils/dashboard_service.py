import os
import time
from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd

import data_pipeline
from utils.aggregations import (
    action_taken_counts,
    country_insight_metrics,
    ids_ips_alerts_counts,
    incidents_per_destination_country,
    incidents_per_source_country,
    selected_country_insight_metrics,
    top_attack_types,
    top_severity_levels,
)
from utils.plot_utils import (
    plot_action_taken_bar,
    plot_attack_type_bar,
    plot_eu_map,
    plot_global_attackers,
    plot_ids_ips_alerts_pie,
    plot_severity_pie,
)

PROCESSED_CSV_PATH = os.path.join("data", "processed", "filtered_attacks.csv")
REFRESH_WINDOW_SECONDS = 12 * 3600


@dataclass
class DashboardData:
    df_eu: pd.DataFrame
    df_agg: pd.DataFrame
    df_filtered: pd.DataFrame
    panel_caption: str
    country_insights: list[dict]
    attackers_agg: pd.DataFrame
    top_attacks: pd.DataFrame
    top_severity: pd.DataFrame
    action_counts: pd.DataFrame
    ids_ips_counts: pd.DataFrame


def ensure_processed_dataset(
    csv_path: str = PROCESSED_CSV_PATH, refresh_window_seconds: int = REFRESH_WINDOW_SECONDS
) -> str:
    """
    Ensure processed CSV exists and is fresh enough.

    If refresh fails (e.g., Kaggle auth/GeoLite issues) and a processed file already exists,
    gracefully fall back to the existing file instead of failing hard.
    """
    has_existing = os.path.exists(csv_path)
    run_pipeline = not has_existing

    if has_existing:
        try:
            file_age = time.time() - os.path.getmtime(csv_path)
            run_pipeline = file_age >= refresh_window_seconds
        except Exception:
            # If mtime can't be read, attempt refresh but still keep fallback path.
            run_pipeline = True

    if run_pipeline:
        try:
            produced_path = data_pipeline.run_data_pipeline()
            if produced_path and os.path.exists(produced_path):
                return produced_path
            if os.path.exists(csv_path):
                return csv_path
            raise FileNotFoundError("Pipeline did not produce a usable processed CSV.")
        except Exception as exc:
            if os.path.exists(csv_path):
                return csv_path
            raise RuntimeError(
                "Failed to prepare processed dataset and no fallback CSV is available."
            ) from exc

    return csv_path


def load_dashboard_dataset(csv_path: str = PROCESSED_CSV_PATH) -> pd.DataFrame:
    """Load the processed dataset used by the dashboard."""
    ensure_processed_dataset(csv_path=csv_path)
    df_eu = pd.read_csv(csv_path, encoding="utf-8-sig")
    df_eu.columns = df_eu.columns.str.strip()
    return df_eu


def parse_selected_country(event: Any) -> Optional[str]:
    """Extract selected country code/name from a Streamlit plotly chart selection event."""
    if not (event and hasattr(event, "selection")):
        return None
    selection = event.selection
    if not selection or "points" not in selection or len(selection["points"]) == 0:
        return None
    return selection["points"][0].get("location")


def build_dashboard_data(df_eu: pd.DataFrame, selected_country: Optional[str]) -> DashboardData:
    """Build all filtered data frames and aggregations needed by the dashboard."""
    df_agg = incidents_per_destination_country(df_eu)

    if selected_country:
        df_filtered = df_eu[df_eu["destination_country"] == selected_country]
        panel_caption = f"{selected_country}:"
        country_insights = selected_country_insight_metrics(df_eu, selected_country)
    else:
        df_filtered = df_eu
        panel_caption = "Across all EU destination countries:"
        country_insights = country_insight_metrics(df_eu, min_incidents=10)

    attackers_agg = incidents_per_source_country(df_filtered)
    top_attacks = top_attack_types(df_filtered)
    top_severity = top_severity_levels(df_filtered)
    action_counts = action_taken_counts(df_filtered)
    ids_ips_counts = ids_ips_alerts_counts(df_filtered)

    return DashboardData(
        df_eu=df_eu,
        df_agg=df_agg,
        df_filtered=df_filtered,
        panel_caption=panel_caption,
        country_insights=country_insights,
        attackers_agg=attackers_agg,
        top_attacks=top_attacks,
        top_severity=top_severity,
        action_counts=action_counts,
        ids_ips_counts=ids_ips_counts,
    )


def build_eu_map_figure(df_eu: pd.DataFrame):
    """Build the EU destination map figure."""
    df_agg = incidents_per_destination_country(df_eu)
    return plot_eu_map(df_agg)


def build_figures(data: DashboardData) -> dict[str, Any]:
    """Build all Plotly figures from prepared dashboard data."""
    return {
        "global_attackers": plot_global_attackers(data.attackers_agg),
        "attack_types": plot_attack_type_bar(data.top_attacks),
        "severity_levels": plot_severity_pie(data.top_severity),
        "action_taken": plot_action_taken_bar(data.action_counts),
        "ids_ips_alerts": plot_ids_ips_alerts_pie(data.ids_ips_counts),
    }

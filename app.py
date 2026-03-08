import streamlit as st
import pandas as pd
import os
import time

import data_pipeline
from utils.aggregations import (
    aggregate_counts,
    incidents_per_destination_country,
    incidents_per_source_country,
    top_attack_types,
    top_severity_levels,
    action_taken_counts,
    ids_ips_alerts_counts,
    country_insight_metrics,
    selected_country_insight_metrics
)
from utils.plot_utils import (
    plot_eu_map,
    plot_global_attackers,
    plot_attack_type_bar,
    plot_severity_pie,
    plot_action_taken_bar,
    plot_ids_ips_alerts_pie
)

st.set_page_config(layout="wide")
st.title("EU Cybersecurity Incidents: A Dashboard")
st.caption(
    "Click any country on the blue map to apply a filter. "
    "Click country again to clear the selection."
)

st.markdown(
    """
    <style>
    div[class*="st-key-neon_panel_blue_"] {
        border: 2px solid #00ffff;
        border-radius: 10px;
        background-color: #0e1117;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.65);
        padding: 0.35rem;
    }
    div[class*="st-key-neon_panel_red_"] {
        border: 2px solid #ff4d4d;
        border-radius: 10px;
        background-color: #0e1117;
        box-shadow: 0 0 15px rgba(255, 77, 77, 0.65);
        padding: 0.35rem;
    }
    div[class*="st-key-neon_panel_purple_"] {
        border: 2px solid #b266ff;
        border-radius: 10px;
        background-color: #0e1117;
        box-shadow: 0 0 15px rgba(178, 102, 255, 0.65);
        padding: 0.35rem;
        min-height: 320px;
        max-height: 320px;
        overflow-y: auto;
    }
    .insight-item {
        border: 1px solid rgba(178, 102, 255, 0.35);
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(178, 102, 255, 0.13), rgba(178, 102, 255, 0.03));
        padding: 8px 10px;
        margin-bottom: 8px;
    }
    .insight-title {
        font-size: 13px;
        font-weight: 700;
        color: #f2e8ff;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    .insight-country {
        font-size: 13px;
        color: #e9ddff;
        margin-bottom: 2px;
    }
    .insight-metric {
        font-size: 12px;
        color: #cdb7ee;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_neon_plot(fig, panel_key: str, *, selection: bool = False, tone: str = "blue"):
    chart_kwargs = {"on_select": "ignore"}
    if selection:
        chart_kwargs["on_select"] = "rerun"
        chart_kwargs["selection_mode"] = "points"

    with st.container(key=f"neon_panel_{tone}_{panel_key}"):
        return st.plotly_chart(
            fig,
            use_container_width=True,
            height=320,
            key=panel_key,
            config={
                "displayModeBar": True,
                "doubleClick": "reset",
                "responsive": True,
                "scrollZoom": False,
            },
            **chart_kwargs,
        )


# -------------------------------
# 1️⃣ Load processed dataset or run pipeline
# -------------------------------
csv_path = "data/processed/filtered_attacks.csv"
run_pipeline = True
if os.path.exists(csv_path):
    file_age = time.time() - os.path.getmtime(csv_path)
    if file_age < 12 * 3600:
        run_pipeline = False

if run_pipeline:
    data_pipeline.run_data_pipeline()

df_eu = pd.read_csv(csv_path, encoding='utf-8-sig')
df_eu.columns = df_eu.columns.str.strip()

# -------------------------------
# 2️⃣ Initial aggregation for map
# -------------------------------
df_agg = incidents_per_destination_country(df_eu)

# -------------------------------
# 3️⃣ EU map (clickable)
# -------------------------------
fig = plot_eu_map(df_agg)

col1_top, col2_top, col3_top = st.columns([0.7, 1.0, 0.49])

with col1_top:
    event = render_neon_plot(fig, "eu_map", selection=True)

# Determine selected country from map
selected_country = None
if event and hasattr(event, "selection"):
    if event.selection and "points" in event.selection and len(event.selection["points"]) > 0:
        selected_country = event.selection["points"][0].get("location")

# -------------------------------
# 4️⃣ Filter dataset if country selected
# -------------------------------
if selected_country:
    df_filtered = df_eu[df_eu["destination_country"] == selected_country]
    panel_caption = f"{selected_country}:"
    country_insights = selected_country_insight_metrics(df_eu, selected_country)
else:
    df_filtered = df_eu
    panel_caption = "Across all EU destination countries:"
    country_insights = country_insight_metrics(df_eu, min_incidents=10)

# -------------------------------
# 5️⃣ Aggregations using filtered data
# -------------------------------
attackers_agg = incidents_per_source_country(df_filtered)
top_attacks = top_attack_types(df_filtered)
top_severity = top_severity_levels(df_filtered)
action_counts = action_taken_counts(df_filtered)
ids_ips_counts = ids_ips_alerts_counts(df_filtered)

# -------------------------------
# 6️⃣ Create plots
# -------------------------------
fig_attackers = plot_global_attackers(attackers_agg)
fig_bar = plot_attack_type_bar(top_attacks)
fig_severity = plot_severity_pie(top_severity)
fig_action = plot_action_taken_bar(action_counts)
fig_ids_ips = plot_ids_ips_alerts_pie(ids_ips_counts)

# -------------------------------
# Layout with two main rows and two columns each
# -------------------------------

# Top row: EU map (left), Global origin map (right)
with col2_top:
    render_neon_plot(fig_attackers, "global_attackers", tone="red")

with col3_top:
    with st.container(key="neon_panel_purple_country_insights"):
        st.caption(panel_caption)
        if country_insights:
            for insight in country_insights:
                value_text = (
                    f"{insight['value']:.1f}%"
                    if insight['unit'] != 'incidents'
                    else f"{int(insight['value']):,}"
                )
                st.markdown(
                    "<div class='insight-item'>"
                    f"<div class='insight-title'>{insight['emoji']} {insight['title']}</div>"
                    f"<div class='insight-country'>{insight['country']}</div>"
                    f"<div class='insight-metric'>{value_text} {insight['unit']}</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("No country insight metrics available for this dataset.")

# Bottom row: All metrics in a single horizontal row
col1_bottom, col2_bottom, col3_bottom, col4_bottom = st.columns([1.5,1,1.5,1])

with col1_bottom:
    render_neon_plot(fig_action, "action_taken")

with col2_bottom:
    render_neon_plot(fig_ids_ips, "ids_ips_alerts")

with col3_bottom:
    render_neon_plot(fig_bar, "attack_types", tone="red")

with col4_bottom:
    render_neon_plot(fig_severity, "severity_levels", tone="red")

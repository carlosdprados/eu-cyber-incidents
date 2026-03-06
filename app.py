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
    ids_ips_alerts_counts
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

col1_top, col2_top = st.columns(2)

with col1_top:
#    st.subheader("EU Cybersecurity Incidents Map")
    event = st.plotly_chart(
        fig,
        use_container_width=True,
        key="eu_map",
        on_select="rerun",
        selection_mode="points",
        config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        }
    )

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
else:
    df_filtered = df_eu

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
#    st.subheader("Global Origin of Attacks (Source IP Countries)")
    with st.container():
        st.plotly_chart(fig_attackers, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })

# Bottom row: Attack type distribution (left), Additional insights (right)
col1_bottom, col2_bottom = st.columns(2)
with col1_bottom:
#    st.subheader("Attack Type Distribution")
    with st.container():
        st.plotly_chart(fig_bar, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
#    st.subheader("Severity Levels Distribution")
    with st.container():
        st.plotly_chart(fig_severity, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
with col2_bottom:
#    st.subheader("Actions Taken")
    with st.container():
        st.plotly_chart(fig_action, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })


#    st.subheader("IDS/IPS Alerts Counts")
    with st.container():
        st.plotly_chart(fig_ids_ips, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
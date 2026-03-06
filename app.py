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
    firewall_logs_counts,
    ids_ips_alerts_counts
)
from utils.plot_utils import (
    plot_eu_map,
    plot_global_attackers,
    plot_attack_type_bar,
    plot_severity_pie,
    plot_action_taken_bar,
    plot_firewall_logs_pie,
    plot_ids_ips_alerts_pie
)

st.set_page_config(layout="wide")
st.title("EU Cybersecurity Incidents Dashboard")
st.write("Interactive map of major cybersecurity incidents in the EU")

eu_countries = [
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg",
    "Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia",
    "Slovenia", "Spain", "Sweden"
]

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
# 2️⃣ Aggregate incidents and top attacks
# -------------------------------
df_agg = incidents_per_destination_country(df_eu)
attackers_agg = incidents_per_source_country(df_eu)
top_attacks = top_attack_types(df_eu)
top_severity = top_severity_levels(df_eu)
action_counts = action_taken_counts(df_eu)
firewall_counts = firewall_logs_counts(df_eu)
ids_ips_counts = ids_ips_alerts_counts(df_eu)

st.write(f"Loaded EU filtered dataset: {len(df_eu)} rows")
st.write("Number of attacker-origin countries detected:", len(attackers_agg))

# -------------------------------
# 3️⃣ Create plots
# -------------------------------
fig = plot_eu_map(df_agg)
fig_attackers = plot_global_attackers(attackers_agg)
fig_bar = plot_attack_type_bar(top_attacks)
fig_severity = plot_severity_pie(top_severity)
fig_action = plot_action_taken_bar(action_counts)
fig_firewall = plot_firewall_logs_pie(firewall_counts)
fig_ids_ips = plot_ids_ips_alerts_pie(ids_ips_counts)

# -------------------------------
# Layout with two main rows and two columns each
# -------------------------------

# Top row: EU map (left), Global origin map (right)
col1_top, col2_top = st.columns(2)
with col1_top:
    st.subheader("EU Cybersecurity Incidents Map")
    with st.container():
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
with col2_top:
    st.subheader("Global Origin of Attacks (Source IP Countries)")
    with st.container():
        st.plotly_chart(fig_attackers, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })

# Bottom row: Attack type distribution (left), Additional insights (right)
col1_bottom, col2_bottom = st.columns(2)
with col1_bottom:
    st.subheader("Attack Type Distribution")
    with st.container():
        st.plotly_chart(fig_bar, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
    st.subheader("Severity Levels Distribution")
    with st.container():
        st.plotly_chart(fig_severity, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
with col2_bottom:
    st.subheader("Actions Taken")
    with st.container():
        st.plotly_chart(fig_action, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
    st.subheader("Firewall Logs Counts")
    with st.container():
        st.plotly_chart(fig_firewall, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
    st.subheader("IDS/IPS Alerts Counts")
    with st.container():
        st.plotly_chart(fig_ids_ips, use_container_width=True, config={
            'displayModeBar': True,
            'doubleClick': 'reset',
            'responsive': True
        })
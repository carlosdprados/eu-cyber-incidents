import streamlit as st
from utils.dashboard_service import (
    build_eu_map_figure,
    build_dashboard_data,
    build_figures,
    load_dashboard_dataset,
    parse_selected_country,
)
from utils.ui_components import apply_dashboard_styles, render_insights_panel, render_neon_plot

st.set_page_config(layout="wide")
st.title("EU Cybersecurity Incidents: A Dashboard")
st.caption(
    "Click any country on the blue map to apply a filter. "
    "Click country again to clear the selection."
)

apply_dashboard_styles()


# -------------------------------
# 1️⃣ Load processed dataset or run pipeline
# -------------------------------
df_eu = load_dashboard_dataset()
fig_eu_map = build_eu_map_figure(df_eu)

# -------------------------------
# 3️⃣ EU map (clickable)
# -------------------------------
col1_top, col2_top, col3_top = st.columns([0.7, 1.0, 0.49])

with col1_top:
    event = render_neon_plot(fig_eu_map, "eu_map", selection=True)

# Determine selected country from map
selected_country = parse_selected_country(event)
dashboard_data = build_dashboard_data(df_eu, selected_country)
figures = build_figures(dashboard_data)

# -------------------------------
# 5️⃣ Aggregations using filtered data
# -------------------------------
# Built in dashboard_service.build_dashboard_data + build_figures.

# -------------------------------
# Layout with two main rows and two columns each
# -------------------------------

# Top row: EU map (left), Global origin map (right)
with col2_top:
    render_neon_plot(figures["global_attackers"], "global_attackers", tone="red")

with col3_top:
    render_insights_panel(dashboard_data.panel_caption, dashboard_data.country_insights)

# Bottom row: All metrics in a single horizontal row
col1_bottom, col2_bottom, col3_bottom, col4_bottom = st.columns([1.5,1,1.5,1])

with col1_bottom:
    render_neon_plot(figures["action_taken"], "action_taken")

with col2_bottom:
    render_neon_plot(figures["ids_ips_alerts"], "ids_ips_alerts")

with col3_bottom:
    render_neon_plot(figures["attack_types"], "attack_types", tone="red")

with col4_bottom:
    render_neon_plot(figures["severity_levels"], "severity_levels", tone="red")

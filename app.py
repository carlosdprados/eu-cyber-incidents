import streamlit as st

from utils.dashboard_service import (
    build_dashboard_data,
    build_eu_map_figure,
    build_figures,
    load_dashboard_dataset,
    parse_selected_country,
)
from utils.ui_components import apply_dashboard_styles, render_insights_panel, render_neon_plot

st.set_page_config(layout="wide")


def _is_probably_mobile_client() -> bool:
    """Best-effort device detection based on request user agent."""
    context = getattr(st, "context", None)
    if context is None:
        return False
    headers = getattr(context, "headers", {}) or {}
    user_agent = str(headers.get("user-agent", "")).lower()
    return any(token in user_agent for token in ("iphone", "ipad", "android", "mobile"))


auto_mobile_layout = _is_probably_mobile_client()
with st.sidebar:
    mobile_layout = st.toggle(
        "Mobile-friendly layout",
        value=auto_mobile_layout,
        help="Stacks all panels vertically and reduces chart heights for smaller screens.",
    )

if mobile_layout:
    st.title("EU Cybersecurity Incidents - A Dashboard")
    st.caption("by @carlosdprados")
else:
    title_col, byline_col = st.columns([0.8, 0.2])
    with title_col:
        st.title("EU Cybersecurity Incidents - A Dashboard")
    with byline_col:
        st.markdown(
            "<div style='text-align: right; padding-top: 1.2rem; color: #9aa0a6;'>by @carlosdprados</div>",
            unsafe_allow_html=True,
        )

st.caption(
    "Click any country on the blue map to apply a filter. "
    "Click country again to clear the selection."
)

apply_dashboard_styles()


def _render_plot_compat(
    fig,
    panel_key: str,
    *,
    selection: bool = False,
    tone: str = "blue",
    height: int = 320,
):
    """
    Render plot with backward compatibility for older render_neon_plot signatures.

    Some environments may have cached an older version of `render_neon_plot`
    that doesn't support the `height` keyword argument.
    """
    try:
        return render_neon_plot(
            fig,
            panel_key,
            selection=selection,
            tone=tone,
            height=height,
        )
    except TypeError as exc:
        if "unexpected keyword argument 'height'" not in str(exc):
            raise
        return render_neon_plot(
            fig,
            panel_key,
            selection=selection,
            tone=tone,
        )


# -------------------------------
# 1️⃣ Load processed dataset or run pipeline
# -------------------------------
df_eu = load_dashboard_dataset()
fig_eu_map = build_eu_map_figure(df_eu)

# -------------------------------
# 3️⃣ EU map (clickable)
# -------------------------------
chart_height = 280 if mobile_layout else 320

if mobile_layout:
    event = _render_plot_compat(
        fig_eu_map,
        "eu_map",
        selection=True,
        height=chart_height,
    )
else:
    col1_top, col2_top, col3_top = st.columns([0.7, 1.0, 0.49])
    with col1_top:
        event = _render_plot_compat(
            fig_eu_map,
            "eu_map",
            selection=True,
            height=chart_height,
        )

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

if mobile_layout:
    _render_plot_compat(
        figures["global_attackers"],
        "global_attackers",
        tone="red",
        height=chart_height,
    )
    render_insights_panel(dashboard_data.panel_caption, dashboard_data.country_insights)
    _render_plot_compat(figures["action_taken"], "action_taken", height=chart_height)
    _render_plot_compat(figures["ids_ips_alerts"], "ids_ips_alerts", height=chart_height)
    _render_plot_compat(
        figures["attack_types"],
        "attack_types",
        tone="red",
        height=chart_height,
    )
    _render_plot_compat(
        figures["severity_levels"],
        "severity_levels",
        tone="red",
        height=chart_height,
    )
else:
    # Top row: EU map (left), Global origin map (middle), insights panel (right)
    with col2_top:
        _render_plot_compat(
            figures["global_attackers"],
            "global_attackers",
            tone="red",
            height=chart_height,
        )

    with col3_top:
        render_insights_panel(dashboard_data.panel_caption, dashboard_data.country_insights)

    # Bottom row: all metrics in a single horizontal row
    col1_bottom, col2_bottom, col3_bottom, col4_bottom = st.columns([1.5, 1, 1.5, 1])

    with col1_bottom:
        _render_plot_compat(figures["action_taken"], "action_taken", height=chart_height)

    with col2_bottom:
        _render_plot_compat(figures["ids_ips_alerts"], "ids_ips_alerts", height=chart_height)

    with col3_bottom:
        _render_plot_compat(
            figures["attack_types"],
            "attack_types",
            tone="red",
            height=chart_height,
        )

    with col4_bottom:
        _render_plot_compat(
            figures["severity_levels"],
            "severity_levels",
            tone="red",
            height=chart_height,
        )

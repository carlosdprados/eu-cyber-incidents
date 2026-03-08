import streamlit as st

DASHBOARD_STYLES = """
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
"""


def apply_dashboard_styles() -> None:
    """Inject dashboard CSS styles."""
    st.markdown(DASHBOARD_STYLES, unsafe_allow_html=True)


def render_neon_plot(fig, panel_key: str, *, selection: bool = False, tone: str = "blue"):
    """Render a plotly chart inside a neon-styled container."""
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


def render_insights_panel(panel_caption: str, country_insights: list[dict]) -> None:
    """Render the right-side insights panel cards."""
    with st.container(key="neon_panel_purple_country_insights"):
        st.caption(panel_caption)
        if country_insights:
            for insight in country_insights:
                value_text = (
                    f"{insight['value']:.1f}%"
                    if insight["unit"] != "incidents"
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

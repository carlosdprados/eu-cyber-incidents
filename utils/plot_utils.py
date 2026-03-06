import pandas as pd
import plotly.express as px


def plot_eu_map(df_agg: pd.DataFrame):
    """
    Create a choropleth map of EU cybersecurity incidents.
    Expects df_agg with columns: ['name', 'count'] and optionally 'hover_text'.
    Returns a Plotly figure.
    """
    hover_data = {'count': True}
    if 'hover_text' in df_agg.columns:
        hover_data['hover_text'] = True
    fig = px.choropleth(
        df_agg,
        locations='name',
        locationmode='country names',
        color='count',
        hover_name='name',
        hover_data=hover_data,
        color_continuous_scale='Reds',
        template='plotly_dark',
        title='EU Cybersecurity Incidents'
    )
    # If hover_text is present, use it for hovertemplate
    if 'hover_text' in df_agg.columns:
        fig.update_traces(
            hovertemplate=df_agg['hover_text']
        )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        geo=dict(
            bgcolor='#0E1117',
            showframe=False,
            showcoastlines=True,
            projection_type='mercator',
            center=dict(lat=54, lon=15),
            lataxis_range=[35, 72],
            lonaxis_range=[-10, 35]
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        autosize=True,
    )
    return fig


def plot_global_attackers(df_agg: pd.DataFrame):
    """
    Create a global choropleth map showing source countries of attacks.
    Expects df_agg with columns: ['name', 'count']
    Returns a Plotly figure.
    """
    fig = px.choropleth(
        df_agg,
        locations='name',
        locationmode='country names',
        color='count',
        hover_name='name',
        color_continuous_scale='Reds',
        template='plotly_dark',
        title='Global Attacker Origins'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        geo=dict(
            bgcolor='#0E1117',
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        autosize=True,
    )
    return fig


def plot_attack_type_bar(df_agg: pd.DataFrame):
    """
    Create a bar chart of attack types with dynamic y-axis and 10% margin.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    ymax = df_agg['count'].max()
    ymin = ymax * 0.90  # start at 90% of the max
    margin = max(1, int(ymax * 0.01))
    ymax = ymax + margin
    fig = px.bar(
        df_agg,
        x='name',
        y='count',
        color='count',
        color_continuous_scale='Reds',
        template='plotly_dark',
        title='Attack Types'
    )
    fig.update_layout(
        yaxis=dict(range=[ymin, ymax]),
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        margin=dict(l=40, r=10, t=40, b=40),
        autosize=True,
        xaxis_title=None,
        yaxis_title=None,
    )
    return fig


def plot_severity_pie(df_agg: pd.DataFrame):
    """
    Create a pie chart of counts of severity levels.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    fig = px.pie(
        df_agg,
        names='name',
        values='count',
        color_discrete_sequence=px.colors.sequential.Reds,
        template='plotly_dark',
        title='Severity Level Distribution'
    )
    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        autosize=True,
    )
    return fig


def plot_ids_ips_alerts_pie(df_agg: pd.DataFrame):
    """
    Create a pie chart of IDS/IPS Alerts presence.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    fig = px.pie(
        df_agg,
        names='name',
        values='count',
        color_discrete_sequence=px.colors.sequential.Reds,
        template='plotly_dark',
        title='IDS/IPS Alerts Presence'
    )
    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        autosize=True,
    )
    return fig


def plot_firewall_logs_pie(df_agg: pd.DataFrame):
    """
    Create a pie chart of Firewall Logs presence.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    fig = px.pie(
        df_agg,
        names='name',
        values='count',
        color_discrete_sequence=px.colors.sequential.Reds,
        template='plotly_dark',
        title='Firewall Logs Presence'
    )
    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        autosize=True,
    )
    return fig


def plot_action_taken_bar(df_agg: pd.DataFrame):
    """
    Create a bar chart of 'Action Taken' counts with dynamic y-axis and 10% margin.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    ymax = df_agg['count'].max()
    ymin = ymax * 0.90  # start at 90% of the max
    margin = max(1, int(ymax * 0.01))
    ymax = ymax + margin
    fig = px.bar(
        df_agg,
        x='name',
        y='count',
        color='count',
        color_continuous_scale='Reds',
        template='plotly_dark',
        title='Action Taken'
    )
    fig.update_layout(
        yaxis=dict(range=[ymin, ymax]),
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        margin=dict(l=40, r=10, t=40, b=40),
        autosize=True,
        xaxis_title=None,
        yaxis_title=None,
    )
    return fig
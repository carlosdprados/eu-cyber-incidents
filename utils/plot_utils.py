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
        color_continuous_scale='Blues',
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
        title='Global Attacker Origins (Source IP Countries)'
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
    attack_order = ['DDoS', 'Malware', 'Intrusion']
    attack_color_map = {
        'DDoS': 'rgb(103, 0, 13)',       # dark red
        'Malware': 'rgb(251, 106, 74)',  # medium red
        'Intrusion': 'rgb(254, 224, 210)'  # light red
    }
    df_plot = df_agg.copy()
    df_plot['name'] = pd.Categorical(df_plot['name'], categories=attack_order, ordered=True)
    df_plot = df_plot.sort_values('name')

    ymax = df_plot['count'].max()
    ymin = df_plot['count'].min() * 0.90
    margin = max(1, int(ymax * 0.01))
    ymax = ymax + margin
    fig = px.bar(
        df_plot,
        x='name',
        y='count',
        color='name',
        color_discrete_map=attack_color_map,
        category_orders={'name': attack_order},
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
        legend_title_text='',
    )
    return fig


def plot_severity_pie(df_agg: pd.DataFrame):
    """
    Create a pie chart of counts of severity levels.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    severity_order = ['High', 'Medium', 'Low']
    df_plot = df_agg.copy()
    df_plot['name'] = pd.Categorical(df_plot['name'], categories=severity_order, ordered=True)
    df_plot = df_plot.sort_values('name')

    severity_color_map = {
        'High': 'rgb(103, 0, 13)',      # dark red
        'Medium': 'rgb(251, 106, 74)',  # mid red
        'Low': 'rgb(254, 224, 210)',    # light red
    }
    fig = px.pie(
        df_plot,
        names='name',
        values='count',
        color='name',
        color_discrete_map=severity_color_map,
        category_orders={'name': severity_order},
        template='plotly_dark',
        title=None
    )
    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        autosize=True,
        legend_title_text='<b>Severity Levels</b>',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(l=10, r=10, t=70, b=10),
    )
    return fig


def plot_ids_ips_alerts_pie(df_agg: pd.DataFrame):
    """
    Create a pie chart of IDS/IPS Alerts presence.
    Expects df_agg with columns: ['name', 'count'] (pre-aggregated data).
    Returns a Plotly figure.
    """
    ids_ips_order = ['Alert Data', 'No Alert Data']
    df_plot = df_agg.copy()
    df_plot['name'] = pd.Categorical(df_plot['name'], categories=ids_ips_order, ordered=True)
    df_plot = df_plot.sort_values('name')

    ids_ips_color_map = {
        'Alert Data': 'rgb(8, 48, 107)',      # dark blue
        'No Alert Data': 'rgb(222, 235, 247)' # light blue
    }
    fig = px.pie(
        df_plot,
        names='name',
        values='count',
        color='name',
        color_discrete_map=ids_ips_color_map,
        category_orders={'name': ids_ips_order},
        template='plotly_dark',
        title=None
    )
    fig.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        autosize=True,
        legend_title_text='<b>IDS/IPS Alerts</b>',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        margin=dict(l=10, r=10, t=70, b=10),
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
    action_order = ['Blocked', 'Ignored', 'Logged']
    action_color_map = {
        'Blocked': 'rgb(8, 48, 107)',     # dark blue
        'Ignored': 'rgb(107, 174, 214)',  # medium blue
        'Logged': 'rgb(222, 235, 247)'    # light blue
    }
    df_plot = df_agg.copy()
    df_plot['name'] = pd.Categorical(df_plot['name'], categories=action_order, ordered=True)
    df_plot = df_plot.sort_values('name')

    ymax = df_plot['count'].max()
    ymin = df_plot['count'].min() * 0.90
    margin = max(1, int(ymax * 0.01))
    ymax = ymax + margin
    fig = px.bar(
        df_plot,
        x='name',
        y='count',
        color='name',
        color_discrete_map=action_color_map,
        category_orders={'name': action_order},
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
        legend_title_text='',
    )
    return fig

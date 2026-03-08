import pandas as pd


def aggregate_counts(df: pd.DataFrame, column: str, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of unique values in a specified column, optionally returning top N.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing the column to aggregate.
        column (str): Column name to aggregate counts for.
        top_n (int, optional): Number of top entries to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'], sorted by descending count.

    Usage:
        To get counts of 'Attack Type':
            aggregate_counts(df, 'Attack Type', top_n=5)
    """
    if column not in df.columns:
        # Return empty DataFrame with correct columns if column missing
        return pd.DataFrame(columns=['name', 'count'])
    df = df.copy()
    df = df.dropna(subset=[column])
    if df.empty:
        # Return empty DataFrame with correct columns if no data after dropna
        return pd.DataFrame(columns=['name', 'count'])
    counts = df[column].value_counts()
    if top_n is not None:
        counts = counts.head(top_n)
    result = counts.reset_index()
    result.columns = ['name', 'count']
    return result


def incidents_per_destination_country(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate the number of incidents per destination country.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'destination_country' column.
        top_n (int, optional): Number of top countries to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing countries and incident counts.
    """
    return aggregate_counts(df, 'destination_country', top_n)


def incidents_per_source_country(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate the number of incidents per source country.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'source_country' column.
        top_n (int, optional): Number of top countries to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing countries and incident counts.
    """
    return aggregate_counts(df, 'source_country', top_n)


def top_attack_types(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of attack types.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Attack Type' column.
        top_n (int, optional): Number of top attack types to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing attack types and counts.
    """
    return aggregate_counts(df, 'Attack Type', top_n)


def top_severity_levels(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of severity levels.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Severity Level' column.
        top_n (int, optional): Number of top severity levels to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing severity levels and counts.
    """
    return aggregate_counts(df, 'Severity Level', top_n)


def action_taken_counts(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of actions taken.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Action Taken' column.
        top_n (int, optional): Number of top actions to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing actions taken and counts.
    """
    return aggregate_counts(df, 'Action Taken', top_n)


def firewall_logs_counts(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of firewall log types.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Firewall Logs' column.
        top_n (int, optional): Number of top firewall log types to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing firewall log types and counts.
    """
    if 'Firewall Logs' not in df.columns:
        return pd.DataFrame(columns=['name', 'count'])
    df = df.copy()
    # Replace blank or empty entries with "No Log Data"
    df['Firewall Logs'] = df['Firewall Logs'].fillna('').astype(str)
    df.loc[df['Firewall Logs'].str.strip() == '', 'Firewall Logs'] = 'No Log Data'
    counts = df['Firewall Logs'].value_counts()
    if top_n is not None:
        counts = counts.head(top_n)
    result = counts.reset_index()
    result.columns = ['name', 'count']
    return result


def ids_ips_alerts_counts(df: pd.DataFrame, top_n: int = None) -> pd.DataFrame:
    """
    Aggregate counts of IDS/IPS alert types.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'IDS/IPS Alerts' column.
        top_n (int, optional): Number of top IDS/IPS alert types to return. If None, return all.

    Returns:
        pd.DataFrame: DataFrame with columns ['name', 'count'] representing IDS/IPS alert types and counts.
    """
    if 'IDS/IPS Alerts' not in df.columns:
        return pd.DataFrame(columns=['name', 'count'])
    df = df.copy()
    # Replace blank or empty entries with "No Alert Data"
    df['IDS/IPS Alerts'] = df['IDS/IPS Alerts'].fillna('').astype(str)
    df.loc[df['IDS/IPS Alerts'].str.strip() == '', 'IDS/IPS Alerts'] = 'No Alert Data'
    counts = df['IDS/IPS Alerts'].value_counts()
    if top_n is not None:
        counts = counts.head(top_n)
    result = counts.reset_index()
    result.columns = ['name', 'count']
    return result


def country_insight_metrics(df: pd.DataFrame, min_incidents: int = 10) -> list[dict]:
    """
    Compute country-level insight metrics for dashboard callouts.

    Parameters:
        df (pd.DataFrame): DataFrame containing destination country and incident attributes.
        min_incidents (int): Minimum incidents required to be considered in ratio rankings.

    Returns:
        list[dict]: List of insight dictionaries with keys:
            ['emoji', 'title', 'country', 'value', 'unit']
    """
    required_columns = {'destination_country', 'Action Taken', 'Severity Level'}
    if not required_columns.issubset(df.columns):
        return []

    df_plot = df.copy()
    df_plot['destination_country'] = df_plot['destination_country'].fillna('').astype(str).str.strip()
    df_plot = df_plot[df_plot['destination_country'] != '']
    if df_plot.empty:
        return []

    df_plot['Action Taken'] = df_plot['Action Taken'].fillna('').astype(str).str.strip()
    df_plot['Severity Level'] = df_plot['Severity Level'].fillna('').astype(str).str.strip()

    country_totals = df_plot.groupby('destination_country').size().rename('total')
    if country_totals.empty:
        return []

    eligible_countries = country_totals[country_totals >= min_incidents].index
    if len(eligible_countries) == 0:
        eligible_countries = country_totals.index

    def ratio_series(column: str, positive_label: str) -> pd.Series:
        counts = (
            df_plot[df_plot[column] == positive_label]
            .groupby('destination_country')
            .size()
            .reindex(country_totals.index, fill_value=0)
        )
        return (counts / country_totals).loc[eligible_countries]

    blocked_ratio = ratio_series('Action Taken', 'Blocked')
    ignored_ratio = ratio_series('Action Taken', 'Ignored')
    high_severity_ratio = ratio_series('Severity Level', 'High')

    insights = [
        {
            'emoji': '🛡️',
            'title': 'Most Effective Blocker',
            'country': blocked_ratio.idxmax(),
            'value': blocked_ratio.max() * 100,
            'unit': 'blocked',
        },
        {
            'emoji': '😴',
            'title': 'Laziest Response',
            'country': ignored_ratio.idxmax(),
            'value': ignored_ratio.max() * 100,
            'unit': 'ignored',
        },
        {
            'emoji': '🔥',
            'title': 'Highest High-Severity Share',
            'country': high_severity_ratio.idxmax(),
            'value': high_severity_ratio.max() * 100,
            'unit': 'high severity',
        },
    ]
    return insights


def selected_country_insight_metrics(
    df: pd.DataFrame, country: str, min_source_incidents: int = 2
) -> list[dict]:
    """
    Compute source-country attacker insights for a selected destination country.

    Parameters:
        df (pd.DataFrame): DataFrame containing incidents.
        country (str): Destination country selected from the map.

    Returns:
        list[dict]: List of insight dictionaries with keys:
            ['emoji', 'title', 'country', 'value', 'unit']
    """
    required_columns = {
        'destination_country',
        'source_country',
        'Attack Type',
        'Severity Level',
        'Action Taken',
    }
    if not required_columns.issubset(df.columns):
        return []

    df_plot = df.copy()
    df_plot['destination_country'] = df_plot['destination_country'].fillna('').astype(str).str.strip()
    df_plot = df_plot[df_plot['destination_country'] == country]
    if df_plot.empty:
        return []

    df_plot['source_country'] = df_plot['source_country'].fillna('').astype(str).str.strip()
    df_plot = df_plot[df_plot['source_country'] != '']
    if df_plot.empty:
        return []

    df_plot['Action Taken'] = df_plot['Action Taken'].fillna('').astype(str).str.strip()
    df_plot['Attack Type'] = df_plot['Attack Type'].fillna('').astype(str).str.strip()
    df_plot['Severity Level'] = df_plot['Severity Level'].fillna('').astype(str).str.strip()
    source_totals = df_plot.groupby('source_country').size()
    if source_totals.empty:
        return []

    min_source_incidents = max(1, int(min_source_incidents))
    eligible_sources = source_totals[source_totals >= min_source_incidents].index
    if len(eligible_sources) == 0:
        eligible_sources = source_totals.index

    non_blocked_counts = (
        df_plot[df_plot['Action Taken'].isin(['Ignored', 'Logged'])]
        .groupby('source_country')
        .size()
        .reindex(source_totals.index, fill_value=0)
    )
    penetration_ratio = (non_blocked_counts / source_totals).loc[eligible_sources]

    malware_counts = (
        df_plot[df_plot['Attack Type'] == 'Malware']
        .groupby('source_country')
        .size()
        .reindex(source_totals.index, fill_value=0)
    )
    malware_ratio = (malware_counts / source_totals).loc[eligible_sources]

    high_severity_counts = (
        df_plot[df_plot['Severity Level'] == 'High']
        .groupby('source_country')
        .size()
        .reindex(source_totals.index, fill_value=0)
    )
    high_severity_ratio = (high_severity_counts / source_totals).loc[eligible_sources]

    top_penetrator = penetration_ratio.idxmax()
    top_malware = malware_ratio.idxmax()
    top_high_severity = high_severity_ratio.idxmax()
    
    def source_label(name: str) -> str:
        count = int(source_totals[name])
        noun = 'incident' if count == 1 else 'incidents'
        return f"{name} ({count:,} {noun})"

    return [
        {
            'emoji': '🎯',
            'title': 'Most Effective Penetrator',
            'country': (
                f"{source_label(top_penetrator)} | "
                f"{int(non_blocked_counts[top_penetrator]):,} non-blocked"
            ),
            'value': penetration_ratio.max() * 100,
            'unit': 'non-blocked share',
        },
        {
            'emoji': '🧬',
            'title': 'Most Malware-Focused Attacker',
            'country': (
                f"{source_label(top_malware)} | "
                f"{int(malware_counts[top_malware]):,} malware"
            ),
            'value': malware_ratio.max() * 100,
            'unit': 'malware share',
        },
        {
            'emoji': '🔥',
            'title': 'Highest High-Severity Attacker',
            'country': (
                f"{source_label(top_high_severity)} | "
                f"{int(high_severity_counts[top_high_severity]):,} high severity"
            ),
            'value': high_severity_ratio.max() * 100,
            'unit': 'high-severity share',
        },
    ]

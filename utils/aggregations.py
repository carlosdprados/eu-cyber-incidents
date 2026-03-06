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

"""
utils/geoip_utils.py

This module provides utilities for mapping IP addresses to countries using the GeoLite2 database and for filtering cybersecurity attack data for European Union countries.

Functions:
- ip_to_country(ip, db_path): Resolve a single IP address to a country.
- map_ips_to_countries(df, db_path): Add source and destination country columns to a DataFrame.
- filter_eu_attacks(df, eu_countries): Filter DataFrame rows where attacks involve EU countries.

Usage:
    from utils.geoip_utils import map_ips_to_countries, filter_eu_attacks
    df = map_ips_to_countries(df)
    df_eu = filter_eu_attacks(df, eu_countries)
"""

import pandas as pd
import geoip2.database
from typing import Optional, List


def ip_to_country(ip: str, db_path: str = "GeoLite2-Country.mmdb") -> Optional[str]:
    """
    Map an IP address to its corresponding country name using the GeoLite2 database.

    Parameters:
        ip (str): The IP address to resolve.
        db_path (str): Path to the GeoLite2-Country.mmdb database file.

    Returns:
        Optional[str]: Country name if resolved successfully; otherwise, None.
    """
    try:
        with geoip2.database.Reader(db_path) as reader:
            response = reader.country(ip)
            return response.country.name
    except Exception:
        return None


def map_ips_to_countries(df: pd.DataFrame, db_path: str = "GeoLite2-Country.mmdb") -> pd.DataFrame:
    """
    Add 'source_country' and 'destination_country' columns to a DataFrame by mapping IP addresses.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'Source IP Address' and 'Destination IP Address' columns.
        db_path (str): Path to the GeoLite2-Country.mmdb database file.

    Returns:
        pd.DataFrame: A copy of the input DataFrame with 'source_country' and 'destination_country' columns added.
    """
    df = df.copy()
    df['source_country'] = df['Source IP Address'].apply(lambda ip: ip_to_country(ip, db_path))
    df['destination_country'] = df['Destination IP Address'].apply(lambda ip: ip_to_country(ip, db_path))
    return df


def filter_eu_attacks(df: pd.DataFrame, eu_countries: List[str]) -> pd.DataFrame:
    """
    Filter the DataFrame to include only rows where either the source or destination country is in the EU.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'source_country' and 'destination_country' columns.
        eu_countries (List[str]): List of country names representing the EU.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only attacks involving EU countries.
    """
    return df[(df['source_country'].isin(eu_countries)) | (df['destination_country'].isin(eu_countries))].copy()

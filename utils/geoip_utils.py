"""
utils/geoip_utils.py

This module provides utilities for mapping IP addresses to countries using the GeoLite2 database and for filtering cybersecurity attack data for European Union countries.

Functions:
- ip_to_country(ip, db_path): Resolve a single IP address to a country.
- map_ips_to_countries(df, db_path): Add source and destination country columns to a DataFrame.
- filter_eu_attacks(df, eu_countries): Filter DataFrame rows where attacks affect EU countries.

Usage:
    from utils.geoip_utils import map_ips_to_countries, filter_eu_attacks
    df = map_ips_to_countries(df)
    df_eu = filter_eu_attacks(df, eu_countries)
"""

from typing import List, Optional

import geoip2.database
import pandas as pd


def _ip_to_country_with_reader(ip: str, reader: geoip2.database.Reader) -> Optional[str]:
    """Resolve one IP with an already-open GeoLite2 reader."""
    try:
        response = reader.country(ip)
        return response.country.name
    except Exception:
        return None


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
            return _ip_to_country_with_reader(ip, reader)
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
    try:
        with geoip2.database.Reader(db_path) as reader:
            df['source_country'] = df['Source IP Address'].map(
                lambda ip: _ip_to_country_with_reader(ip, reader)
            )
            df['destination_country'] = df['Destination IP Address'].map(
                lambda ip: _ip_to_country_with_reader(ip, reader)
            )
    except Exception:
        # Keep pipeline behavior resilient if GeoLite2 DB is unavailable/corrupt.
        df['source_country'] = None
        df['destination_country'] = None
    return df


def filter_eu_attacks(df: pd.DataFrame, eu_countries: List[str]) -> pd.DataFrame:
    """
    Filter the DataFrame to include only rows where the destination country is in the EU.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'source_country' and 'destination_country' columns.
        eu_countries (List[str]): List of country names representing the EU.

    Returns:
        pd.DataFrame: Filtered DataFrame containing only attacks affecting EU countries.
    """
    return df[df['destination_country'].isin(eu_countries)].copy()

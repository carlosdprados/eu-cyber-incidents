"""
utils/data_export.py

Utility functions for exporting processed datasets used by the EU Cyber Incidents
dashboard project.

This module is responsible for persisting intermediate datasets to disk before
any aggregation or visualization steps are performed. In particular, it stores
the filtered dataset containing only attacks involving EU countries,
while removing large or unnecessary fields (e.g., "Payload Data") before persistence.
If a previously exported file already exists and is less than 12 hours old,
the export step is skipped to avoid unnecessary processing.

Usage:
    from utils.data_export import export_filtered_dataset

    export_filtered_dataset(df_eu)
"""

import os
import time
import pandas as pd

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
DEFAULT_FILENAME = "filtered_attacks.csv"


def export_filtered_dataset(df: pd.DataFrame, filename: str = DEFAULT_FILENAME) -> str:
    """
    Export a filtered DataFrame to the processed data directory.

    This function saves the DataFrame containing EU-related cyber incidents
    to the `data/processed` directory so it can be reused by the application
    without recomputing the filtering step.

    If a processed file with the same name already exists and is less than
    12 hours old, the export step is skipped and the existing file path is
    returned. This prevents unnecessary recomputation and disk writes.

    Prior to export, large or unnecessary columns such as "Payload Data"
    are removed to keep the processed dataset lightweight.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the filtered cyber attack records.
    filename : str, optional
        Name of the CSV file to save. Defaults to 'filtered_attacks.csv'.

    Returns
    -------
    str
        Full path to the saved CSV file.
    """
    output_path = os.path.join(PROCESSED_DIR, filename)

    # Skip export if a recent processed file already exists
    try:
        if os.path.exists(output_path):
            file_age = time.time() - os.path.getmtime(output_path)
            if file_age < 12 * 3600:
                return output_path
    except Exception:
        # If file age cannot be determined, continue with export
        pass

    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Remove large or unnecessary columns before exporting
    df = df.drop(columns=["Payload Data"], errors="ignore")

    df.to_csv(output_path, index=False)

    return output_path

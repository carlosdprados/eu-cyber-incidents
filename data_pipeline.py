"""
data_pipeline.py

Pipeline script for preparing the dataset used in the EU Cyber Incidents project.

The pipeline performs the following steps:

1. Load the raw dataset from Kaggle using the data loader utility.
2. Map source and destination IP addresses to countries using GeoLite2.
3. Filter the dataset to retain only incidents involving EU countries.
4. Export the filtered dataset to `data/processed/filtered_attacks.csv`.

This script prepares the dataset before any aggregation or visualization steps.
"""

import os
import time
from utils.data_loader import get_dataset
from utils.geoip_utils import map_ips_to_countries, filter_eu_attacks
from utils.data_export import export_filtered_dataset
from utils.eu_countries import EU_COUNTRIES

PROCESSED_PATH = os.path.join("data", "processed", "filtered_attacks.csv")


def run_data_pipeline():
    """
    Execute the data preparation pipeline.

    Returns
    -------
    str
        Path to the exported filtered CSV file.
    """

    # Skip processing if the processed CSV exists and is fresh
    if os.path.exists(PROCESSED_PATH):
        try:
            if time.time() - os.path.getmtime(PROCESSED_PATH) < 12 * 3600:
                print(f"Processed CSV is fresh, skipping pipeline: {PROCESSED_PATH}")
                return PROCESSED_PATH
        except Exception:
            pass  # If file age cannot be determined, continue processing

    # Step 1: Load dataset
    df = get_dataset()

    # Step 2: Map IP addresses to countries
    df = map_ips_to_countries(df)

    # Step 3: Filter incidents involving EU countries
    df_eu = filter_eu_attacks(df, EU_COUNTRIES)

    # Step 4: Export filtered dataset
    output_path = export_filtered_dataset(df_eu)

    return output_path


if __name__ == "__main__":
    path = run_data_pipeline()
    print(f"Filtered dataset exported to: {path}")
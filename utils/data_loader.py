"""
utils/data_loader.py

This module provides functions to download, cache, and load the cybersecurity attack dataset from KaggleHub.

Functions:
- download_dataset(): Downloads the latest dataset from KaggleHub and returns the CSV path.
- load_csv(csv_path): Loads a CSV file into a pandas DataFrame.
- get_dataset(cache=True): Returns the dataset, using a locally cached copy if available and recent (less than 12 hours old).

Usage:
    from utils.data_loader import get_dataset
    df = get_dataset()
"""

import os
import pandas as pd
import kagglehub
import time

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
KAGGLE_DATASET_NAME = 'teamincribo/cyber-security-attacks'


def download_dataset() -> str:
    """Download the Kaggle dataset and return the CSV path."""
    os.makedirs(DATA_RAW_DIR, exist_ok=True)
    path = kagglehub.dataset_download(KAGGLE_DATASET_NAME)
    for file in os.listdir(path):
        if file.endswith('.csv'):
            return os.path.join(path, file)
    raise FileNotFoundError('No CSV file found in the Kaggle dataset.')


def load_csv(csv_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(csv_path)


def get_dataset(cache: bool = True) -> pd.DataFrame:
    """Return the dataset, using cache if available and recent."""
    cached_csv = os.path.join(DATA_RAW_DIR, 'cyber_security_attacks.csv')
    if cache and os.path.exists(cached_csv):
        try:
            if time.time() - os.path.getmtime(cached_csv) < 12 * 3600:
                return load_csv(cached_csv)
        except Exception:
            pass
    csv_path = download_dataset()
    df = pd.read_csv(csv_path)
    if cache:
        os.makedirs(DATA_RAW_DIR, exist_ok=True)
        df.to_csv(cached_csv, index=False)
        return load_csv(cached_csv)
    return df

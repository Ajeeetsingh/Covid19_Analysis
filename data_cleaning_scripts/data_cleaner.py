# data_cleaner.py

import pandas as pd


def clean_dataset(df, date_columns=None, numeric_columns=None, text_columns=None):
    """
    Cleans the given dataset by handling missing values, removing duplicates,
    converting data types, and standardizing text.

    Parameters:
        df (pd.DataFrame): The dataset to clean.
        date_columns (list): List of columns to convert to datetime.
        numeric_columns (list): List of columns to convert to numeric.
        text_columns (list): List of columns to clean and standardize text.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    # Handle missing values
    df.fillna(0, inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Convert date columns to datetime
    if date_columns:
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Convert numeric columns to proper format
    if numeric_columns:
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Standardize text columns
    if text_columns:
        for col in text_columns:
            df[col] = df[col].str.strip().str.title()

    return df

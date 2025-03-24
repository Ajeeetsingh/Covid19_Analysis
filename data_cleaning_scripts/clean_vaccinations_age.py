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
    # 1. Handle missing values
    df.fillna(0, inplace=True)  # Replace all NaN values with 0 (customize as needed)

    # 2. Remove duplicates
    df.drop_duplicates(inplace=True)

    # 3. Convert date columns to datetime
    if date_columns:
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 4. Convert numeric columns to proper format
    if numeric_columns:
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 5. Standardize text columns
    if text_columns:
        for col in text_columns:
            df[col] = df[col].str.strip().str.title()  # Remove leading/trailing spaces and capitalize words

    # Return the cleaned DataFrame
    return df


# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\vaccinations_age.csv'  # Replace with your file path
vaccinations_age = pd.read_csv(file_path)

# Inspect the dataset
print("Before Cleaning:")
print(vaccinations_age.info())
print(vaccinations_age.head())

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'people_with_booster_per_hundred']  # numeric column names
text_columns = ['country', 'age_group']  # text column names

# Clean the dataset
vaccinations_age_cleaned = clean_dataset(
    vaccinations_age,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
vaccinations_age_cleaned.to_csv(output_path, index=False)

# Inspect the cleaned dataset
print("\nAfter Cleaning:")
print(vaccinations_age_cleaned.info())
print(vaccinations_age_cleaned.head())

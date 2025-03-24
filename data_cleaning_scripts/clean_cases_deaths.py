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
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\cases_deaths.csv'  # Replace with your file path
cases_deaths = pd.read_csv(file_path)

# Inspect the dataset
print("Before Cleaning:")
print(cases_deaths.info())
print(cases_deaths.head())

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['new_cases', 'total_cases', 'new_deaths', 'total_deaths',
                   'weekly_cases', 'weekly_deaths', 'weekly_pct_growth_cases', 'weekly_pct_growth_deaths',
                   'biweekly_cases', 'biweekly_deaths', 'biweekly_pct_growth_cases', 'biweekly_pct_growth_deaths',
                   'new_cases_per_million', 'new_deaths_per_million', 'total_cases_per_million', 'total_deaths_per_million',
                   'weekly_cases_per_million', 'weekly_deaths_per_million', 'biweekly_cases_per_million', 'biweekly_deaths_per_million',
                   'total_deaths_per_100k', 'new_deaths_per_100k', 'new_cases_7_day_avg_right', 'new_deaths_7_day_avg_right',
                   'new_cases_per_million_7_day_avg_right', 'new_deaths_per_million_7_day_avg_right',
                   'new_deaths_per_100k_7_day_avg_right', 'cfr', 'cfr_100_cases', 'cfr_short_term',
                   'days_since_100_total_cases', 'days_since_5_total_deaths', 'days_since_1_total_cases_per_million',
                   'days_since_0_1_total_deaths_per_million', 'days_since_100_total_cases_and_5m_pop',
                   'total_deaths_last12m', 'total_deaths_per_100k_last12m', 'total_deaths_per_million_last12m']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
cases_deaths_cleaned = clean_dataset(
    cases_deaths,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
cases_deaths_cleaned.to_csv(output_path, index=False)

# Inspect the cleaned dataset
print("\nAfter Cleaning:")
print(cases_deaths_cleaned.info())
print(cases_deaths_cleaned.head())

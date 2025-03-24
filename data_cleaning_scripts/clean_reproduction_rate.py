# clean_reproduction_rate.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\reproduction_rate.csv'
reproduction_rate_data = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['r', 'ci_95_u', 'ci_95_l', 'ci_65_u', 'ci_65_l', 'days_infectious']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
reproduction_rate_cleaned = clean_dataset(
    reproduction_rate_data,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\reproduction_rate_cleaned.csv'
reproduction_rate_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

# clean_testing.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\testing.csv'
testing_data = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['total_tests', 'new_tests', 'total_tests_per_thousand', 'new_tests_per_thousand',
                   'new_tests_7day_smoothed', 'new_tests_per_thousand_7day_smoothed']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
testing_cleaned = clean_dataset(
    testing_data,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\testing_cleaned.csv'
testing_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

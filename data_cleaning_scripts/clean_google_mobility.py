# clean_google_mobility.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\google_mobility.csv'
google_mobility = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['trend']  # numeric column names
text_columns = ['country', 'place']  # text column names

# Clean the dataset
google_mobility_cleaned = clean_dataset(
    google_mobility,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\google_mobility_cleaned.csv'
google_mobility_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")


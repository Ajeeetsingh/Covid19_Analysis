# clean_hospital.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\hospital.csv'
hospital = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['daily_occupancy_icu', 'daily_occupancy_icu_per_1m', 'daily_occupancy_hosp', 'daily_occupancy_hosp_per_1m',
                   'weekly_admissions_icu', 'weekly_admissions_icu_per_1m', 'weekly_admissions_hosp',
                   'weekly_admissions_hosp_per_1m']  # numeric column names
text_columns = ['country', 'country_code']  # text column names

# Clean the dataset
hospital_cleaned = clean_dataset(
    hospital,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\hospital_cleaned.csv'
hospital_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

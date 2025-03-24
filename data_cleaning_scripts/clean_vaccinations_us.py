# clean_vaccinations_us.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\vaccinations_us.csv'
vaccinations_us = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['total_vaccinations', 'total_distributed', 'people_vaccinated', 'people_fully_vaccinated_per_hundred',
                   'total_vaccinations_per_hundred', 'people_fully_vaccinated', 'people_vaccinated_per_hundred',
                   'distributed_per_hundred', 'daily_vaccinations_raw', 'daily_vaccinations', 'daily_vaccinations_per_million',
                   'share_doses_used', 'total_boosters', 'total_boosters_per_hundred']  # numeric column names
text_columns = ['state']  # text column names

# Clean the dataset
vaccinations_us_cleaned = clean_dataset(
    vaccinations_us,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_us_cleaned.csv'
vaccinations_us_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

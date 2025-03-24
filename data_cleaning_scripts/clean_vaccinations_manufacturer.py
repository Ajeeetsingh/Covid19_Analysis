# clean_vaccinations_manufacturer.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\vaccinations_manufacturer.csv'
vaccination_manufacturer = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['total_vaccinations']  # numeric column names
text_columns = ['country', 'vaccine']  # text column names

# Clean the dataset
vaccination_manufacturer_cleaned = clean_dataset(
    vaccination_manufacturer,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_manufacturer_cleaned.csv'
vaccination_manufacturer_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

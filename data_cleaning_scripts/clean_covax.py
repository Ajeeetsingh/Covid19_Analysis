# clean_covax.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\covax.csv'
covax = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['year', 'delivered', 'only_donated', 'only_announced', 'delivered_per_gdp', 'only_donated_per_gdp',
                   'only_announced_per_gdp', 'delivered_per_used', 'only_donated_per_used', 'only_announced_per_used',
                   'delivered_per_capita', 'only_donated_per_capita', 'only_announced_per_capita']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
covax_cleaned = clean_dataset(
    covax,
    date_columns=None,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\covax_cleaned.csv'
covax_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

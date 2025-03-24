# clean_Attitudes (YouGov).py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\Attitudes (YouGov).csv'
Attitudes = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['people_vaccinated_per_hundred', 'uncertain_covid_vaccinate_this_week_pct_pop',
                   'unwillingness_covid_vaccinate_this_week_pct_pop', 'willingness_covid_vaccinate_this_week_pct_pop']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
Attitudes_cleaned = clean_dataset(
    Attitudes,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Attitudes_cleaned.csv'
Attitudes_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

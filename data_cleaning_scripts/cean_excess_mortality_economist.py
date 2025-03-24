# clean_excess_mortality_economist.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\excess_mortality_economist.csv'
economist_data = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['cumulative_estimated_daily_excess_deaths', 'cumulative_estimated_daily_excess_deaths_ci_95_top',
                   'cumulative_estimated_daily_excess_deaths_ci_95_bot', 'cumulative_estimated_daily_excess_deaths_per_100k',
                   'cumulative_estimated_daily_excess_deaths_ci_95_top_per_100k', 'cumulative_estimated_daily_excess_deaths_ci_95_bot_per_100k',
                   'estimated_daily_excess_deaths', 'estimated_daily_excess_deaths_ci_95_top', 'estimated_daily_excess_deaths_ci_95_bot',
                   'estimated_daily_excess_deaths_per_100k', 'estimated_daily_excess_deaths_ci_95_top_per_100k',
                   'estimated_daily_excess_deaths_ci_95_bot_per_100k', 'cumulative_estimated_daily_excess_deaths_last12m',
                   'cumulative_estimated_daily_excess_deaths_per_100k_last12m', 'cumulative_estimated_daily_excess_deaths_ci_95_bot_last12m',
                   'cumulative_estimated_daily_excess_deaths_ci_95_bot_per_100k_last12m', 'cumulative_estimated_daily_excess_deaths_ci_95_top_last12m',
                   'cumulative_estimated_daily_excess_deaths_ci_95_top_per_100k_last12m']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
excess_mortality_economist_cleaned = clean_dataset(
    economist_data,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_economist_cleaned.csv'
excess_mortality_economist_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

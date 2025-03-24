# clean_excess_mortality.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\excess_mortality.csv'
excess_mortality = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['time', 'time_unit', 'average_deaths_2015_2019_all_ages', 'p_avg_0_14', 'p_avg_15_64', 'p_avg_65_74',
                   'p_avg_75_84', 'p_avg_85p', 'p_avg_all_ages', 'projected_deaths_since_2020_all_ages', 'p_proj_0_14',
                   'p_proj_15_64', 'p_proj_65_74', 'p_proj_75_84', 'p_proj_85p', 'p_proj_all_ages', 'excess_proj_all_ages',
                   'deaths_since_2020_all_ages', 'deaths_2010_all_ages', 'deaths_2011_all_ages', 'deaths_2012_all_ages',
                   'deaths_2013_all_ages', 'deaths_2014_all_ages', 'deaths_2015_all_ages', 'deaths_2016_all_ages',
                   'deaths_2017_all_ages', 'deaths_2018_all_ages', 'deaths_2019_all_ages', 'deaths_2020_all_ages',
                   'deaths_2021_all_ages', 'deaths_2022_all_ages', 'deaths_2023_all_ages', 'deaths_2024_all_ages',
                   'cum_excess_proj_all_ages', 'cum_proj_deaths_all_ages', 'cum_p_proj_all_ages',
                   'excess_per_million_proj_all_ages', 'cum_excess_per_million_proj_all_ages',
                   'cum_excess_proj_all_ages_last12m', 'cum_excess_per_million_proj_all_ages_last12m']  # numeric column names
text_columns = ['entity']  # text column names

# Clean the dataset
excess_mortality_cleaned = clean_dataset(
    excess_mortality,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv'
excess_mortality_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

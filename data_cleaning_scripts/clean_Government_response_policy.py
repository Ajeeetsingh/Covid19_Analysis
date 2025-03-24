# clean_Government_response_policy.py

import pandas as pd
from data_cleaner import clean_dataset

# Load the dataset
file_path = 'F:\\PycharmProjects\\Covid_19_Project\\OWID_Covid_Data\\Government_response_policy.csv'
Government_response_policy = pd.read_csv(file_path)

# Define columns for cleaning
date_columns = ['date']  # date column name(s)
numeric_columns = ['c1m_school_closing', 'c2m_workplace_closing', 'c3m_cancel_public_events', 'c4m_restrictions_on_gatherings',
                   'c5m_close_public_transport', 'c6m_stay_at_home_requirements', 'c7m_restrictions_on_internal_movement',
                   'c8ev_international_travel_controls', 'e1_income_support', 'e2_debt_contract_relief', 'e3_fiscal_measures',
                   'e4_international_support', 'h1_public_information_campaigns', 'h2_testing_policy', 'h3_contact_tracing',
                   'h4_emergency_investment_in_healthcare', 'h5_investment_in_vaccines', 'h6m_facial_coverings', 'h7_vaccination_policy',
                   'v2a_vaccine_availability__summary', 'v2b_vaccine_age_eligibility_availability_age_floor__general_population_summary',
                   'v2c_vaccine_age_eligibility_availability_age_floor__at_risk_summary', 'stringency_index', 'containment_health_index',
                   'v2_vaccine_availability__summary', 'v2_pregnant_people', 'stringency_index_nonvax', 'stringency_index_vax',
                   'stringency_index_weighted_average']  # numeric column names
text_columns = ['country']  # text column names

# Clean the dataset
Government_response_policy_cleaned = clean_dataset(
    Government_response_policy,
    date_columns=date_columns,
    numeric_columns=numeric_columns,
    text_columns=text_columns
)

# Save the cleaned dataset to a new file
output_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
Government_response_policy_cleaned.to_csv(output_path, index=False)

print("Dataset cleaned and saved!")

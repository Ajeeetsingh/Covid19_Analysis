import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Define required columns for each dataset
required_columns = {
    'cases_deaths': ['country', 'date', 'new_cases_per_million', 'cfr', 'weekly_cases'],
    'vaccinations': ['country', 'date', 'people_vaccinated_per_hundred'],
    'government_response': ['country', 'date', 'stringency_index'],
    'mobility': ['country', 'date', 'trend']
}


class RegressionAnalysis:
    def __init__(self, data):
        """
        Initialize the RegressionAnalysis class with data.
        """
        self.data = data

    def train_linear_regression(self, X, y):
        """
        Train a linear regression model.

        Parameters:
            X (pd.DataFrame): Independent variables.
            y (pd.Series): Dependent variable.
        """
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the linear regression model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Mean Absolute Error: {mae}")
        print(f"R^2 Score: {r2}")

    def predict(self, X):
        """
        Make predictions using the trained model.

        Parameters:
            X (pd.DataFrame): Independent variables.
        """
        return self.model.predict(X)

    def plot_regression(self, X, y, xlabel, ylabel, title):
        """
        Plot the regression results.

        Parameters:
            X (pd.Series): Independent variable.
            y (pd.Series): Dependent variable.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X, y=y, label='Actual Data')

        # Convert X to a DataFrame to ensure it's 2D
        X_df = pd.DataFrame(X, columns=[X.name])

        # Predict using the model
        y_pred = self.model.predict(X_df)

        # Plot the regression line
        sns.lineplot(x=X, y=y_pred, color='red', label='Regression Line')

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()


# Helper Functions
def analyze_vaccination_vs_cfr(regression_analysis, country='United States'):
    """
    Analyze the impact of vaccination rates on case fatality rate (CFR).
    """
    # Filter data for the specified country
    country_data = regression_analysis.data[regression_analysis.data['country'] == country]

    # Prepare independent and dependent variables
    X = country_data[['people_vaccinated_per_hundred']]
    y = country_data['cfr']

    # Train the regression model
    regression_analysis.train_linear_regression(X, y)

    # Plot the regression results
    regression_analysis.plot_regression(
        X['people_vaccinated_per_hundred'], y,
        xlabel='Vaccination Rate (%)',
        ylabel='Case Fatality Rate (CFR)',
        title='Vaccination Rate vs. Case Fatality Rate'
    )


def analyze_policy_stringency_vs_cases(regression_analysis, country='United States'):
    """
    Analyze the impact of policy stringency on new cases.
    """
    # Filter data for the specified country
    country_data = regression_analysis.data[regression_analysis.data['country'] == country]

    # Prepare independent and dependent variables
    X = country_data[['stringency_index']]
    y = country_data['new_cases_per_million']

    # Train the regression model
    regression_analysis.train_linear_regression(X, y)

    # Plot the regression results
    regression_analysis.plot_regression(
        X['stringency_index'], y,
        xlabel='Stringency Index',
        ylabel='New Cases per Million',
        title='Policy Stringency vs. New Cases'
    )


def analyze_mobility_vs_case_growth(regression_analysis, country='United States'):
    """
    Analyze the impact of mobility on case growth rates.
    """
    # Filter data for the specified country
    country_data = regression_analysis.data[regression_analysis.data['country'] == country].copy()

    # Calculate weekly percentage growth in cases
    country_data.loc[:, 'weekly_pct_growth_cases'] = country_data['weekly_cases'].pct_change() * 100

    # Replace infinite values with NaN and drop them
    country_data.replace([np.inf, -np.inf], np.nan, inplace=True)
    country_data.dropna(subset=['weekly_pct_growth_cases'], inplace=True)

    # Prepare independent and dependent variables
    X = country_data[['trend']]
    y = country_data['weekly_pct_growth_cases']

    # Train the regression model
    regression_analysis.train_linear_regression(X, y)

    # Plot the regression results
    regression_analysis.plot_regression(
        X['trend'], y,
        xlabel='Mobility Trend',
        ylabel='Weekly Case Growth (%)',
        title='Mobility vs. Case Growth'
    )


# Main Function
def main():
    # File paths
    cases_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
    vaccinations_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
    government_response_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
    mobility_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\google_mobility_cleaned.csv'

    # Load datasets with only required columns
    cases_data = pd.read_csv(cases_path, usecols=required_columns['cases_deaths'])
    vaccinations_data = pd.read_csv(vaccinations_path, usecols=required_columns['vaccinations'])
    government_response_data = pd.read_csv(government_response_path, usecols=required_columns['government_response'])
    mobility_data = pd.read_csv(mobility_path, usecols=required_columns['mobility'])

    # Convert date columns to datetime
    cases_data['date'] = pd.to_datetime(cases_data['date'])
    vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])
    government_response_data['date'] = pd.to_datetime(government_response_data['date'])
    mobility_data['date'] = pd.to_datetime(mobility_data['date'])

    # Merge datasets
    merged_data = pd.merge(cases_data, vaccinations_data, on=['country', 'date'], how='inner')
    merged_data = pd.merge(merged_data, government_response_data, on=['country', 'date'], how='inner')
    merged_data = pd.merge(merged_data, mobility_data, on=['country', 'date'], how='inner')

    # Initialize the RegressionAnalysis class
    regression_analysis = RegressionAnalysis(merged_data)

    # Perform regression analysis
    analyze_vaccination_vs_cfr(regression_analysis, country='Argentina')
    analyze_policy_stringency_vs_cases(regression_analysis, country='Argentina')
    analyze_mobility_vs_case_growth(regression_analysis, country='Argentina')


if __name__ == "__main__":
    main()

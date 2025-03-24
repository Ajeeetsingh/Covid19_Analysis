from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import joblib


class TimeSeriesForecasting:
    def __init__(self, data):
        """
        Initialize the TimeSeriesForecasting class with data.
        """
        self.data = data

    def train_prophet_model(self, country, target_column, date_column='date'):
        """
        Train a Prophet model for a specific country and target column.

        Parameters:
            country (str): The country to filter data for.
            target_column (str): The column to forecast (e.g., 'new_cases', 'people_vaccinated_per_hundred').
            date_column (str): The column containing dates (default is 'date').
        """
        # Filter data for the specified country and target column
        country_data = self.data[self.data['country'] == country][[date_column, target_column]]
        country_data.columns = ['ds', 'y']  # Prophet requires columns named 'ds' and 'y'

        # Debug: Print the filtered data
        # print(f"Filtered data for {country}:\n{country_data}")

        # Check if there are enough non-NaN rows
        if country_data['y'].count() < 2:
            raise ValueError(f"Not enough data for {country}. Found {country_data['y'].count()} non-NaN rows.")

        # Initialize and train the Prophet model
        self.model = Prophet()
        self.model.fit(country_data)

    def predict_future(self, periods=30):
        """
        Generate forecasts for the next `periods` days.

        Parameters:
            periods (int): Number of days to forecast (default is 30).
        """
        future = self.model.make_future_dataframe(periods=periods)
        self.forecast = self.model.predict(future)
        return self.forecast

    def plot_forecast(self, title='COVID-19 Forecast', xlabel='Date', ylabel='Value'):
        """
        Plot the forecast.

        Parameters:
            title (str): Title of the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
        """
        fig = self.model.plot(self.forecast)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    def save_model(self, filename):
        """
        Save the trained model to a file.

        Parameters:
            filename (str): Name of the file to save the model.
        """
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        """
        Load a trained model from a file.

        Parameters:
            filename (str): Name of the file to load the model from.
        """
        self.model = joblib.load(filename)


# Helper Functions
def forecast_cases(ts_forecasting, country='United States'):
    """
    Forecast new cases for a specific country.
    """
    # Train the model for new cases
    ts_forecasting.train_prophet_model(country=country, target_column='new_cases')

    # Generate and plot forecasts
    forecast = ts_forecasting.predict_future(periods=30)
    ts_forecasting.plot_forecast(title='COVID-19 Case Forecast', ylabel='New Cases')

    # Save the model
    ts_forecasting.save_model('prophet_cases_model.pkl')


def forecast_vaccinations(ts_forecasting, country='United States'):
    """
    Forecast vaccination rates for a specific country.
    """
    # Train the model for vaccination rates
    ts_forecasting.train_prophet_model(country=country, target_column='people_vaccinated_per_hundred')

    # Generate and plot forecasts
    forecast = ts_forecasting.predict_future(periods=30)
    ts_forecasting.plot_forecast(title='Vaccination Rate Forecast', ylabel='Vaccination Rate (%)')

    # Save the model
    ts_forecasting.save_model('prophet_vaccinations_model.pkl')


def forecast_excess_mortality(ts_forecasting, country='United States'):
    """
    Forecast excess mortality for a specific country.
    """
    # Train the model for excess mortality
    ts_forecasting.train_prophet_model(country=country, target_column='excess_proj_all_ages')

    # Generate and plot forecasts
    forecast = ts_forecasting.predict_future(periods=30)
    ts_forecasting.plot_forecast(title='Excess Mortality Forecast', ylabel='Excess Mortality')

    # Save the model
    ts_forecasting.save_model('prophet_mortality_model.pkl')


# Main Function
def main():
    # Load datasets
    cases_data = pd.read_csv('F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv')
    cases_data['date'] = pd.to_datetime(cases_data['date'])

    vaccinations_data = pd.read_csv('F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv')
    vaccinations_data['date'] = pd.to_datetime(vaccinations_data['date'])

    excess_mortality_data = pd.read_csv('F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv')
    excess_mortality_data['date'] = pd.to_datetime(excess_mortality_data['date'])
    excess_mortality_data.rename(columns={'entity': 'country'}, inplace=True)

    # Initialize the TimeSeriesForecasting class for each dataset
    # ts_cases = TimeSeriesForecasting(cases_data)
    # ts_vaccinations = TimeSeriesForecasting(vaccinations_data)
    ts_mortality = TimeSeriesForecasting(excess_mortality_data)

    # Perform forecasting for each dataset
    # forecast_cases(ts_cases, country='United States')
    # forecast_vaccinations(ts_vaccinations, country='Argentina')
    forecast_excess_mortality(ts_mortality, country='United States')


if __name__ == "__main__":
    main()

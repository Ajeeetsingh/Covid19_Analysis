import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class TestingHealthcareAnalysis:
    def __init__(self):
        """
        Initialize the TestingHealthcareAnalysis class with file paths.
        """
        testing_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\testing_cleaned.csv'
        healthcare_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\hospital_cleaned.csv'
        cases_deaths_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
        excess_mortality_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv'

        # Load datasets
        self.testing = pd.read_csv(testing_path)
        self.healthcare = pd.read_csv(healthcare_path)
        self.healthcare.columns = self.healthcare.columns.str.strip()
        self.cases_deaths = pd.read_csv(cases_deaths_path)
        self.excess_mortality = pd.read_csv(excess_mortality_path)

        # Convert date columns to datetime
        self.testing['date'] = pd.to_datetime(self.testing['date'])
        self.healthcare['date'] = pd.to_datetime(self.healthcare['date'])
        self.cases_deaths['date'] = pd.to_datetime(self.cases_deaths['date'])
        self.excess_mortality['date'] = pd.to_datetime(self.excess_mortality['date'])
        self.excess_mortality.rename(columns={'entity': 'country'}, inplace=True)

    def _process_testing_rates_over_time_data(self, country):
        """
        Process data for testing rates over time analysis.
        """
        country_data = self.testing[self.testing['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_testing_rates_over_time_chart(self, data, country):
        """
        Generate a line chart for testing rates over time analysis.
        """
        fig = px.line(data, x='date', y='new_tests_per_thousand',
                      title=f'Testing Rates Over Time in {country}',
                      labels={'new_tests_per_thousand': 'New Tests per Thousand'})
        fig.update_layout(xaxis_title='Date', yaxis_title='New Tests per Thousand')
        return fig

    def _plot_testing_rates_over_time_map(self, data, country):
        """
        Generate a map for testing rates over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'new_tests_per_thousand': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_tests_per_thousand',  # Use testing rates for coloring
                            title=f'Testing Rates by Country',
                            labels={'new_tests_per_thousand': 'New Tests per Thousand'})
        return fig

    def _plot_testing_rates_over_time_table(self, data):
        """
        Generate a table for testing rates over time analysis.
        """
        table = dash_table.DataTable(
            id='testing-rates-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_testing_rates_over_time(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for testing rates over time analysis.
        """
        data = self._process_testing_rates_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_testing_rates_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_testing_rates_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_testing_rates_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_testing_vs_case_detection_data(self, country):
        """
        Process data for testing vs. case detection analysis.
        """
        merged_data = pd.merge(
            self.testing,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_testing_vs_case_detection_chart(self, data, country):
        """
        Generate a scatter plot for testing vs. case detection analysis.
        """
        fig = px.scatter(data, x='new_tests_per_thousand', y='new_cases_per_million',
                         title=f'Testing Rates vs. Case Detection in {country}',
                         labels={'new_tests_per_thousand': 'New Tests per Thousand',
                                 'new_cases_per_million': 'New Cases per Million'})
        fig.update_layout(xaxis_title='New Tests per Thousand', yaxis_title='New Cases per Million')
        return fig

    def _plot_testing_vs_case_detection_map(self, data, country):
        """
        Generate a map for testing vs. case detection analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'new_tests_per_thousand': 'mean',
            'new_cases_per_million': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_cases_per_million',  # Use case detection for coloring
                            title=f'Case Detection by Country',
                            labels={'new_cases_per_million': 'New Cases per Million'})
        return fig

    def _plot_testing_vs_case_detection_table(self, data):
        """
        Generate a table for testing vs. case detection analysis.
        """
        table = dash_table.DataTable(
            id='testing-vs-case-detection-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_testing_vs_case_detection(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for testing vs. case detection analysis.
        """
        data = self._process_testing_vs_case_detection_data(country)

        if visualization_type == 'chart':
            fig = self._plot_testing_vs_case_detection_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_testing_vs_case_detection_map(data, country)
        elif visualization_type == 'table':
            return self._plot_testing_vs_case_detection_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_healthcare_capacity_over_time_data(self, country):
        """
        Process data for healthcare capacity over time analysis.
        """
        country_data = self.healthcare[self.healthcare['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_healthcare_capacity_over_time_chart(self, data, country):
        """
        Generate a line chart for healthcare capacity over time analysis.
        """
        fig = px.line(data, x='date', y=['daily_occupancy_icu_per_1m', 'daily_occupancy_hosp_per_1m'],
                      title=f'Healthcare Capacity Over Time in {country}',
                      labels={'value': 'Occupancy per Million', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Occupancy per Million', legend_title='Metric')
        return fig

    def _plot_healthcare_capacity_over_time_map(self, data, country):
        """
        Generate a map for healthcare capacity over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'daily_occupancy_icu_per_1m': 'mean',
            'daily_occupancy_hosp_per_1m': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='daily_occupancy_icu_per_1m',  # Use ICU occupancy for coloring
                            title=f'Healthcare Capacity by Country',
                            labels={'daily_occupancy_icu_per_1m': 'ICU Occupancy per Million'})
        return fig

    def _plot_healthcare_capacity_over_time_table(self, data):
        """
        Generate a table for healthcare capacity over time analysis.
        """
        table = dash_table.DataTable(
            id='healthcare-capacity-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_healthcare_capacity_over_time(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for healthcare capacity over time analysis.
        """
        data = self._process_healthcare_capacity_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_healthcare_capacity_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_healthcare_capacity_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_healthcare_capacity_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_healthcare_capacity_vs_cfr_data(self, country):
        """
        Process data for healthcare capacity vs. case fatality rate (CFR) analysis.
        """
        merged_data = pd.merge(
            self.healthcare,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_healthcare_capacity_vs_cfr_chart(self, data, country):
        """
        Generate a scatter plot for healthcare capacity vs. case fatality rate (CFR) analysis.
        """
        fig = px.scatter(data, x='daily_occupancy_icu_per_1m', y='cfr',
                         title=f'Healthcare Capacity vs. Case Fatality Rate in {country}',
                         labels={'daily_occupancy_icu_per_1m': 'ICU Occupancy per Million',
                                 'cfr': 'Case Fatality Rate (%)'})
        fig.update_layout(xaxis_title='ICU Occupancy per Million', yaxis_title='Case Fatality Rate (%)')
        return fig

    def _plot_healthcare_capacity_vs_cfr_map(self, data, country):
        """
        Generate a map for healthcare capacity vs. case fatality rate (CFR) analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'daily_occupancy_icu_per_1m': 'mean',
            'cfr': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='cfr',  # Use case fatality rate for coloring
                            title=f'Case Fatality Rate by Country',
                            labels={'cfr': 'Case Fatality Rate (%)'})
        return fig

    def _plot_healthcare_capacity_vs_cfr_table(self, data):
        """
        Generate a table for healthcare capacity vs. case fatality rate (CFR) analysis.
        """
        table = dash_table.DataTable(
            id='healthcare-capacity-vs-cfr-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_healthcare_capacity_vs_cfr(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for healthcare capacity vs. case fatality rate (CFR) analysis.
        """
        data = self._process_healthcare_capacity_vs_cfr_data(country)

        if visualization_type == 'chart':
            fig = self._plot_healthcare_capacity_vs_cfr_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_healthcare_capacity_vs_cfr_map(data, country)
        elif visualization_type == 'table':
            return self._plot_healthcare_capacity_vs_cfr_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_healthcare_capacity_vs_excess_mortality_data(self, country):
        """
        Process data for healthcare capacity vs. excess mortality analysis.
        """
        merged_data = pd.merge(
            self.healthcare,
            self.excess_mortality,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_healthcare_capacity_vs_excess_mortality_chart(self, data, country):
        """
        Generate a scatter plot for healthcare capacity vs. excess mortality analysis.
        """
        fig = px.scatter(data, x='daily_occupancy_icu_per_1m', y='excess_proj_all_ages',
                         title=f'Healthcare Capacity vs. Excess Mortality in {country}',
                         labels={'daily_occupancy_icu_per_1m': 'ICU Occupancy per Million',
                                 'excess_proj_all_ages': 'Excess Mortality'})
        fig.update_layout(xaxis_title='ICU Occupancy per Million', yaxis_title='Excess Mortality')
        return fig

    def _plot_healthcare_capacity_vs_excess_mortality_map(self, data, country):
        """
        Generate a map for healthcare capacity vs. excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'daily_occupancy_icu_per_1m': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_healthcare_capacity_vs_excess_mortality_table(self, data):
        """
        Generate a table for healthcare capacity vs. excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='healthcare-capacity-vs-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_healthcare_capacity_vs_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for healthcare capacity vs. excess mortality analysis.
        """
        data = self._process_healthcare_capacity_vs_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_healthcare_capacity_vs_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_healthcare_capacity_vs_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_healthcare_capacity_vs_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_testing_healthcare_by_country_data(self):
        """
        Process data for testing and healthcare capacity by country analysis.
        """
        # Aggregate testing and healthcare data by country
        testing_by_country = self.testing.groupby('country')['new_tests_per_thousand'].max().reset_index()
        healthcare_by_country = self.healthcare.groupby('country')['daily_occupancy_icu_per_1m'].max().reset_index()

        # Merge testing and healthcare data
        merged_data = pd.merge(testing_by_country, healthcare_by_country, on='country')
        return merged_data

    def _plot_testing_healthcare_by_country_chart(self, data):
        """
        Generate a bar chart for testing and healthcare capacity by country analysis.
        """
        fig = px.bar(data, x='country', y=['new_tests_per_thousand', 'daily_occupancy_icu_per_1m'],
                     title='Testing Rates and Healthcare Capacity by Country',
                     labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Country', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_testing_healthcare_by_country_map(self, data):
        """
        Generate a map for testing and healthcare capacity by country analysis.
        """
        # Create a choropleth map
        fig = px.choropleth(data, locations='country', locationmode='country names',
                            color='new_tests_per_thousand',  # Use testing rates for coloring
                            title=f'Testing Rates by Country',
                            labels={'new_tests_per_thousand': 'New Tests per Thousand'})
        return fig

    def _plot_testing_healthcare_by_country_table(self, data):
        """
        Generate a table for testing and healthcare capacity by country analysis.
        """
        table = dash_table.DataTable(
            id='testing-healthcare-by-country-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_testing_healthcare_by_country(self, visualization_type='chart'):
        """
        Generate the specified visualization for testing and healthcare capacity by country analysis.
        """
        data = self._process_testing_healthcare_by_country_data()

        if visualization_type == 'chart':
            fig = self._plot_testing_healthcare_by_country_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_testing_healthcare_by_country_map(data)
        elif visualization_type == 'table':
            return self._plot_testing_healthcare_by_country_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


# Example usage
if __name__ == "__main__":
    # Initialize the class with file paths
    testing_healthcare_analysis = TestingHealthcareAnalysis()

    # Generate a chart
    # chart = testing_healthcare_analysis.plot_testing_healthcare_by_country(country='United States',
    # visualization_type='chart')
    # chart.show()

    chart = testing_healthcare_analysis.plot_testing_healthcare_by_country(visualization_type='chart')
    chart.show()

    # Generate a map
    map = testing_healthcare_analysis.plot_testing_healthcare_by_country(visualization_type='map')
    map.show()

    # Generate a table
    table = testing_healthcare_analysis.plot_testing_healthcare_by_country(visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

    # Run the Dash app
    app.run(debug=True)

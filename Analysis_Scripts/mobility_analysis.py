import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class MobilityAnalysis:
    def __init__(self):
        """
        Initialize the MobilityAnalysis class with file paths.
        """
        mobility_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\google_mobility_cleaned.csv'
        cases_deaths_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
        government_response_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
        vaccinations_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
        excess_mortality_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv'

        # Load datasets
        self.mobility = pd.read_csv(mobility_path)
        self.cases_deaths = pd.read_csv(cases_deaths_path)
        self.government_response = pd.read_csv(government_response_path)
        self.vaccinations = pd.read_csv(vaccinations_path)
        self.excess_mortality = pd.read_csv(excess_mortality_path)

        # Convert date columns to datetime
        self.mobility['date'] = pd.to_datetime(self.mobility['date'])
        self.cases_deaths['date'] = pd.to_datetime(self.cases_deaths['date'])
        self.government_response['date'] = pd.to_datetime(self.government_response['date'])
        self.vaccinations['date'] = pd.to_datetime(self.vaccinations['date'])
        self.excess_mortality['date'] = pd.to_datetime(self.excess_mortality['date'])
        self.excess_mortality.rename(columns={'entity': 'country'}, inplace=True)

    def _process_mobility_trends_over_time_data(self, country):
        """
        Process data for mobility trends over time analysis.
        """
        country_data = self.mobility[self.mobility['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_mobility_trends_over_time_chart(self, data, country):
        """
        Generate a line chart for mobility trends over time analysis.
        """
        fig = px.line(data, x='date', y='trend', color='place',
                      title=f'Mobility Trends Over Time in {country}',
                      labels={'trend': 'Mobility Trend', 'place': 'Place'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Mobility Trend', legend_title='Place')
        return fig

    def _plot_mobility_trends_over_time_map(self, data, country):
        """
        Generate a map for mobility trends over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'trend': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='trend',  # Use mobility trend for coloring
                            title=f'Mobility Trends by Country',
                            labels={'trend': 'Mobility Trend'})
        return fig

    def _plot_mobility_trends_over_time_table(self, data):
        """
        Generate a table for mobility trends over time analysis.
        """
        table = dash_table.DataTable(
            id='mobility-trends-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_trends_over_time(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for mobility trends over time analysis.
        """
        data = self._process_mobility_trends_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_mobility_trends_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_mobility_trends_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_mobility_trends_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_mobility_trends_by_country_data(self):
        """
        Process data for mobility trends by country analysis.
        """
        mobility_by_country = self.mobility.groupby(['country', 'place'])['trend'].mean().reset_index()
        return mobility_by_country

    def _plot_mobility_trends_by_country_chart(self, data):
        """
        Generate a bar chart for mobility trends by country analysis.
        """
        fig = px.bar(data, x='country', y='trend', color='place',
                     title='Mobility Trends by Country',
                     labels={'trend': 'Average Mobility Trend', 'country': 'Country', 'place': 'Place'})
        fig.update_layout(xaxis_title='Country', yaxis_title='Average Mobility Trend', legend_title='Place')
        return fig

    def _plot_mobility_trends_by_country_map(self, data):
        """
        Generate a map for mobility trends by country analysis.
        """
        # Create a choropleth map
        fig = px.choropleth(data, locations='country', locationmode='country names',
                            color='trend',  # Use mobility trend for coloring
                            title='Mobility Trends by Country',
                            labels={'trend': 'Average Mobility Trend'})
        return fig

    def _plot_mobility_trends_by_country_table(self, data):
        """
        Generate a table for mobility trends by country analysis.
        """
        table = dash_table.DataTable(
            id='mobility-trends-by-country-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_trends_by_country(self, visualization_type='chart'):
        """
        Generate the specified visualization for mobility trends by country analysis.
        """
        data = self._process_mobility_trends_by_country_data()

        if visualization_type == 'chart':
            fig = self._plot_mobility_trends_by_country_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_mobility_trends_by_country_map(data)
        elif visualization_type == 'table':
            return self._plot_mobility_trends_by_country_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_mobility_vs_case_growth_data(self, country):
        """
        Process data for mobility vs. case growth analysis.
        """
        merged_data = pd.merge(
            self.mobility,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_mobility_vs_case_growth_chart(self, data, country):
        """
        Generate a scatter plot for mobility vs. case growth analysis.
        """
        fig = px.scatter(data, x='trend', y='weekly_pct_growth_cases', color='place',
                         title=f'Mobility vs. Case Growth in {country}',
                         labels={'trend': 'Mobility Trend', 'weekly_pct_growth_cases': 'Weekly Case Growth (%)',
                                 'place': 'Place'})
        fig.update_layout(xaxis_title='Mobility Trend', yaxis_title='Weekly Case Growth (%)', legend_title='Place')
        return fig

    def _plot_mobility_vs_case_growth_map(self, data, country):
        """
        Generate a map for mobility vs. case growth analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'trend': 'mean',
            'weekly_pct_growth_cases': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='weekly_pct_growth_cases',  # Use case growth for coloring
                            title=f'Case Growth by Country',
                            labels={'weekly_pct_growth_cases': 'Weekly Case Growth (%)'})
        return fig

    def _plot_mobility_vs_case_growth_table(self, data):
        """
        Generate a table for mobility vs. case growth analysis.
        """
        table = dash_table.DataTable(
            id='mobility-vs-case-growth-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_vs_case_growth(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for mobility vs. case growth analysis.
        """
        data = self._process_mobility_vs_case_growth_data(country)

        if visualization_type == 'chart':
            fig = self._plot_mobility_vs_case_growth_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_mobility_vs_case_growth_map(data, country)
        elif visualization_type == 'table':
            return self._plot_mobility_vs_case_growth_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_mobility_vs_policies_data(self, country):
        """
        Process data for mobility vs. policies analysis.
        """
        merged_data = pd.merge(
            self.mobility,
            self.government_response,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country].copy()  # Use .copy() to avoid the warning

        if country_data.empty:
            raise ValueError(f"No data available for {country}.")

        # Ensure correct data types using .loc
        country_data.loc[:, 'date'] = pd.to_datetime(country_data['date'])
        country_data.loc[:, 'trend'] = pd.to_numeric(country_data['trend'])
        country_data.loc[:, 'stringency_index'] = pd.to_numeric(country_data['stringency_index'])

        # Drop rows with missing values
        country_data = country_data.dropna(subset=['trend', 'stringency_index'])

        # Aggregate data by date (if necessary) and retain the 'country' column
        country_data_aggregated = country_data.groupby(['country', 'date']).agg({
            'trend': 'mean',
            'stringency_index': 'mean'
        }).reset_index()

        return country_data_aggregated

    def _plot_mobility_vs_policies_chart(self, data, country):
        """
        Generate a line chart for mobility vs. policies analysis.
        """
        fig = px.line(data, x='date', y=['trend', 'stringency_index'],
                      title=f'Mobility vs. Government Policies in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_mobility_vs_policies_map(self, data, country):
        """
        Generate a map for mobility vs. policies analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'trend': 'mean',
            'stringency_index': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='trend',  # Use mobility trend for coloring
                            title=f'Mobility vs. Government Policies by Country',
                            labels={'trend': 'Mobility Trend'})
        return fig

    def _plot_mobility_vs_policies_table(self, data):
        """
        Generate a table for mobility vs. policies analysis.
        """
        table = dash_table.DataTable(
            id='mobility-vs-policies-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_vs_policies(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for mobility vs. policies analysis.
        """
        data = self._process_mobility_vs_policies_data(country)

        if visualization_type == 'chart':
            fig = self._plot_mobility_vs_policies_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_mobility_vs_policies_map(data, country)
        elif visualization_type == 'table':
            return self._plot_mobility_vs_policies_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_mobility_vs_vaccination_data(self, country):
        """
        Process data for mobility vs. vaccination analysis.
        """
        merged_data = pd.merge(
            self.mobility,
            self.vaccinations,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_mobility_vs_vaccination_chart(self, data, country):
        """
        Generate a scatter plot for mobility vs. vaccination analysis.
        """
        fig = px.scatter(data, x='people_vaccinated_per_hundred', y='trend', color='place',
                         title=f'Mobility vs. Vaccination Rate in {country}',
                         labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)', 'trend': 'Mobility Trend',
                                 'place': 'Place'})
        fig.update_layout(xaxis_title='Vaccination Rate (%)', yaxis_title='Mobility Trend', legend_title='Place')
        return fig

    def _plot_mobility_vs_vaccination_map(self, data, country):
        """
        Generate a map for mobility vs. vaccination analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'trend': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='trend',  # Use mobility trend for coloring
                            title=f'Mobility vs. Vaccination Rate by Country',
                            labels={'trend': 'Mobility Trend'})
        return fig

    def _plot_mobility_vs_vaccination_table(self, data):
        """
        Generate a table for mobility vs. vaccination analysis.
        """
        table = dash_table.DataTable(
            id='mobility-vs-vaccination-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_vs_vaccination(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for mobility vs. vaccination analysis.
        """
        data = self._process_mobility_vs_vaccination_data(country)

        if visualization_type == 'chart':
            fig = self._plot_mobility_vs_vaccination_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_mobility_vs_vaccination_map(data, country)
        elif visualization_type == 'table':
            return self._plot_mobility_vs_vaccination_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_mobility_vs_excess_mortality_data(self, country):
        """
        Process data for mobility vs. excess mortality analysis.
        """
        merged_data = pd.merge(
            self.mobility,
            self.excess_mortality,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_mobility_vs_excess_mortality_chart(self, data, country):
        """
        Generate a scatter plot for mobility vs. excess mortality analysis.
        """
        fig = px.scatter(data, x='trend', y='excess_proj_all_ages', color='place',
                         title=f'Mobility vs. Excess Mortality in {country}',
                         labels={'trend': 'Mobility Trend', 'excess_proj_all_ages': 'Excess Mortality',
                                 'place': 'Place'})
        fig.update_layout(xaxis_title='Mobility Trend', yaxis_title='Excess Mortality', legend_title='Place')
        return fig

    def _plot_mobility_vs_excess_mortality_map(self, data, country):
        """
        Generate a map for mobility vs. excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'trend': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_mobility_vs_excess_mortality_table(self, data):
        """
        Generate a table for mobility vs. excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='mobility-vs-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_mobility_vs_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for mobility vs. excess mortality analysis.
        """
        data = self._process_mobility_vs_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_mobility_vs_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_mobility_vs_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_mobility_vs_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


# Example usage
if __name__ == "__main__":
    # Initialize the class with file paths
    mobility_analysis = MobilityAnalysis()

    # Generate a chart
    # chart = mobility_analysis.plot_mobility_trends_over_time(country='Austria', visualization_type='chart')
    chart = mobility_analysis.plot_mobility_vs_excess_mortality(country='Austria', visualization_type='chart')
    chart.show(browser=True)

    # Generate a map
    map = mobility_analysis.plot_mobility_vs_excess_mortality(country='Austria', visualization_type='map')
    map.show(browser=True)

    # Generate a table
    table = mobility_analysis.plot_mobility_vs_excess_mortality(country='Austria', visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

    # # Run the Dash app
    # if __name__ == "__main__":
    app.run(debug=True)

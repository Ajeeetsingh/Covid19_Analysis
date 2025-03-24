import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class PolicyAnalysis:
    def __init__(self):
        """
        Initialize the PolicyAnalysis class with file paths.
        """
        government_response_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
        cases_deaths_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
        mobility_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\google_mobility_cleaned.csv'
        vaccinations_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
        excess_mortality_path = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv'

        # Load datasets
        self.government_response = pd.read_csv(government_response_path)
        self.cases_deaths = pd.read_csv(cases_deaths_path)
        self.mobility = pd.read_csv(mobility_path)
        self.vaccinations = pd.read_csv(vaccinations_path)
        self.excess_mortality = pd.read_csv(excess_mortality_path)

        # Convert date columns to datetime
        self.government_response['date'] = pd.to_datetime(self.government_response['date'])
        self.cases_deaths['date'] = pd.to_datetime(self.cases_deaths['date'])
        self.mobility['date'] = pd.to_datetime(self.mobility['date'])
        self.vaccinations['date'] = pd.to_datetime(self.vaccinations['date'])
        self.excess_mortality['date'] = pd.to_datetime(self.excess_mortality['date'])
        self.excess_mortality.rename(columns={'entity': 'country'}, inplace=True)

    def _process_policy_stringency_over_time_data(self, country):
        """
        Process data for policy stringency over time analysis.
        """
        country_data = self.government_response[self.government_response['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_stringency_over_time_chart(self, data, country):
        """
        Generate a line chart for policy stringency over time analysis.
        """
        fig = px.line(data, x='date', y='stringency_index',
                      title=f'Policy Stringency Over Time in {country}',
                      labels={'stringency_index': 'Stringency Index'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Stringency Index')
        return fig

    def _plot_policy_stringency_over_time_map(self, data, country):
        """
        Generate a map for policy stringency over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'stringency_index': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='stringency_index',  # Use stringency index for coloring
                            title=f'Policy Stringency by Country',
                            labels={'stringency_index': 'Stringency Index'})
        return fig

    def _plot_policy_stringency_over_time_table(self, data):
        """
        Generate a table for policy stringency over time analysis.
        """
        table = dash_table.DataTable(
            id='policy-stringency-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_stringency_over_time(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy stringency over time analysis.
        """
        data = self._process_policy_stringency_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_stringency_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_stringency_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_stringency_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_impact_on_cases_deaths_data(self, country):
        """
        Process data for policy impact on cases and deaths analysis.
        """
        merged_data = pd.merge(
            self.government_response,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_impact_on_cases_deaths_chart(self, data, country):
        """
        Generate a line chart for policy impact on cases and deaths analysis.
        """
        fig = px.line(data, x='date', y=['stringency_index', 'new_cases_per_million', 'new_deaths_per_million'],
                      title=f'Policy Impact on Cases and Deaths in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_policy_impact_on_cases_deaths_map(self, data, country):
        """
        Generate a map for policy impact on cases and deaths analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'stringency_index': 'mean',
            'new_cases_per_million': 'mean',
            'new_deaths_per_million': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_cases_per_million',  # Use new cases per million for coloring
                            title=f'Policy Impact on Cases and Deaths by Country',
                            labels={'new_cases_per_million': 'New Cases per Million'})
        return fig

    def _plot_policy_impact_on_cases_deaths_table(self, data):
        """
        Generate a table for policy impact on cases and deaths analysis.
        """
        table = dash_table.DataTable(
            id='policy-impact-on-cases-deaths-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_impact_on_cases_deaths(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy impact on cases and deaths analysis.
        """
        data = self._process_policy_impact_on_cases_deaths_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_impact_on_cases_deaths_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_impact_on_cases_deaths_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_impact_on_cases_deaths_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_impact_on_mobility_data(self, country):
        """
        Process data for policy impact on mobility analysis.
        """
        merged_data = pd.merge(
            self.government_response,
            self.mobility,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_impact_on_mobility_chart(self, data, country):
        """
        Generate a line chart for policy impact on mobility analysis.
        """
        fig = px.line(data, x='date', y=['stringency_index', 'trend'],
                      title=f'Policy Impact on Mobility in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_policy_impact_on_mobility_map(self, data, country):
        """
        Generate a map for policy impact on mobility analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'stringency_index': 'mean',
            'trend': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='trend',  # Use mobility trend for coloring
                            title=f'Policy Impact on Mobility by Country',
                            labels={'trend': 'Mobility Trend'})
        return fig

    def _plot_policy_impact_on_mobility_table(self, data):
        """
        Generate a table for policy impact on mobility analysis.
        """
        table = dash_table.DataTable(
            id='policy-impact-on-mobility-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_impact_on_mobility(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy impact on mobility analysis.
        """
        data = self._process_policy_impact_on_mobility_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_impact_on_mobility_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_impact_on_mobility_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_impact_on_mobility_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_impact_on_vaccination_data(self, country):
        """
        Process data for policy impact on vaccination analysis.
        """
        merged_data = pd.merge(
            self.government_response,
            self.vaccinations,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_impact_on_vaccination_chart(self, data, country):
        """
        Generate a line chart for policy impact on vaccination analysis.
        """
        fig = px.line(data, x='date', y=['stringency_index', 'people_vaccinated_per_hundred'],
                      title=f'Policy Impact on Vaccination Rates in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_policy_impact_on_vaccination_map(self, data, country):
        """
        Generate a map for policy impact on vaccination analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'stringency_index': 'mean',
            'people_vaccinated_per_hundred': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='people_vaccinated_per_hundred',  # Use vaccination rate for coloring
                            title=f'Policy Impact on Vaccination Rates by Country',
                            labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)'})
        return fig

    def _plot_policy_impact_on_vaccination_table(self, data):
        """
        Generate a table for policy impact on vaccination analysis.
        """
        table = dash_table.DataTable(
            id='policy-impact-on-vaccination-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_impact_on_vaccination(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy impact on vaccination analysis.
        """
        data = self._process_policy_impact_on_vaccination_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_impact_on_vaccination_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_impact_on_vaccination_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_impact_on_vaccination_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_impact_on_excess_mortality_data(self, country):
        """
        Process data for policy impact on excess mortality analysis.
        """
        merged_data = pd.merge(
            self.government_response,
            self.excess_mortality,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_impact_on_excess_mortality_chart(self, data, country):
        """
        Generate a line chart for policy impact on excess mortality analysis.
        """
        fig = px.line(data, x='date', y=['stringency_index', 'excess_proj_all_ages'],
                      title=f'Policy Impact on Excess Mortality in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_policy_impact_on_excess_mortality_map(self, data, country):
        """
        Generate a map for policy impact on excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'stringency_index': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Policy Impact on Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_policy_impact_on_excess_mortality_table(self, data):
        """
        Generate a table for policy impact on excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='policy-impact-on-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_impact_on_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy impact on excess mortality analysis.
        """
        data = self._process_policy_impact_on_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_impact_on_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_impact_on_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_impact_on_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_effectiveness_by_country_data(self):
        """
        Process data for policy effectiveness by country analysis.
        """
        merged_data = pd.merge(
            self.government_response,
            self.cases_deaths,
            on=['country', 'date']
        )

        # Calculate policy effectiveness (e.g., reduction in cases/deaths per unit of stringency)
        policy_effectiveness = merged_data.groupby('country').apply(
            lambda x: (x['new_cases_per_million'].max() - x['new_cases_per_million'].min()) / x[
                'stringency_index'].max()
        ).reset_index(name='policy_effectiveness')
        return policy_effectiveness

    def _plot_policy_effectiveness_by_country_chart(self, data):
        """
        Generate a bar chart for policy effectiveness by country analysis.
        """
        fig = px.bar(data, x='country', y='policy_effectiveness',
                      title='Policy Effectiveness by Country',
                      labels={'policy_effectiveness': 'Policy Effectiveness', 'country': 'Country'})
        fig.update_layout(xaxis_title='Country', yaxis_title='Policy Effectiveness')
        return fig

    def _plot_policy_effectiveness_by_country_map(self, data):
        """
        Generate a map for policy effectiveness by country analysis.
        """
        # Create a choropleth map
        fig = px.choropleth(data, locations='country', locationmode='country names',
                            color='policy_effectiveness',  # Use policy effectiveness for coloring
                            title=f'Policy Effectiveness by Country',
                            labels={'policy_effectiveness': 'Policy Effectiveness'})
        return fig

    def _plot_policy_effectiveness_by_country_table(self, data):
        """
        Generate a table for policy effectiveness by country analysis.
        """
        table = dash_table.DataTable(
            id='policy-effectiveness-by-country-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_effectiveness_by_country(self, visualization_type='chart'):
        """
        Generate the specified visualization for policy effectiveness by country analysis.
        """
        data = self._process_policy_effectiveness_by_country_data()

        if visualization_type == 'chart':
            fig = self._plot_policy_effectiveness_by_country_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_policy_effectiveness_by_country_map(data)
        elif visualization_type == 'table':
            return self._plot_policy_effectiveness_by_country_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


# Example usage
if __name__ == "__main__":
    # Initialize the class with file paths
    policy_analysis = PolicyAnalysis()

    # Generate a chart
    # chart = policy_analysis.plot_policy_impact_on_excess_mortality(country='Lithuania', visualization_type='chart')
    # chart.show()

    # Generate a chart
    chart = policy_analysis.plot_policy_effectiveness_by_country(visualization_type='chart')
    chart.show()

    # Generate a map
    map = policy_analysis.plot_policy_effectiveness_by_country(visualization_type='map')
    map.show()

    # Generate a table
    table = policy_analysis.plot_policy_effectiveness_by_country(visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

    # Run the Dash app
    app.run(debug=True)

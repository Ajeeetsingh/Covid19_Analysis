import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class CasesDeathAnalysis:
    def __init__(self):
        """
        Initialize the CaseDeathAnalysis class with the file path.
        """
        cases_deaths_file = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
        government_response_file = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv'
        reproduction_rate_file = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\reproduction_rate_cleaned.csv'
        testing_file = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\testing_cleaned.csv'

        self.cases_deaths = pd.read_csv(cases_deaths_file)
        self.government_response = pd.read_csv(government_response_file)
        self.reproduction_rate = pd.read_csv(reproduction_rate_file)
        self.testing = pd.read_csv(testing_file)

        # Convert date columns to datetime
        self.cases_deaths['date'] = pd.to_datetime(self.cases_deaths['date'])
        self.government_response['date'] = pd.to_datetime(self.government_response['date'])
        self.reproduction_rate['date'] = pd.to_datetime(self.reproduction_rate['date'])
        self.testing['date'] = pd.to_datetime(self.testing['date'])

    # Data Processing Method
    def _process_cfr_data(self):
        """
        Process data for Case Fatality Rate (CFR) analysis.
        """
        # Group by 'country' and calculate the latest CFR
        cfr_data = self.cases_deaths.groupby('country').apply(
            lambda x: (x['total_deaths'].max() / x['total_cases'].max()) * 100 if x['total_cases'].max() != 0 else 0
        ).reset_index(name='cfr')

        return cfr_data

    # Visualization Methods
    def _plot_cfr_chart(self, data):
        """
        Generate a bar chart for CFR analysis.
        """
        fig = px.bar(data, x='country', y='cfr', title='Case Fatality Rate (CFR) by Country',
                     labels={'cfr': 'CFR (%)', 'country': 'Country'})
        fig.update_layout(xaxis_tickangle=-90)
        return fig

    def _plot_cfr_map(self, data):
        """
        Generate a choropleth map for CFR analysis.
        """
        fig = px.choropleth(data, locations='country', locationmode='country names', color='cfr',
                            title='Case Fatality Rate (CFR) by Country',
                            labels={'cfr': 'CFR (%)'})
        return fig

    def _plot_cfr_table(self, data):
        """
        Generate a table for CFR analysis.
        """
        table = dash_table.DataTable(
            id='cfr-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_cfr(self, visualization_type='chart'):
        """
        Generate the specified visualization for CFR analysis.
        """
        data = self._process_cfr_data()

        if visualization_type == 'chart':
            fig = self._plot_cfr_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_cfr_map(data)
        elif visualization_type == 'table':
            return self._plot_cfr_table(data)  # Tables are already Dash components
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        # Wrap the Plotly figure in a dcc.Graph component
        return dcc.Graph(figure=fig)

    def _process_weekly_biweekly_growth_data(self, country):
        """
        Process data for weekly/biweekly growth analysis.
        """
        country_data = self.cases_deaths[self.cases_deaths['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_weekly_biweekly_growth_chart(self, data, country):
        """
        Generate a line chart for weekly/biweekly growth analysis.
        """
        fig = px.line(data, x='date', y=['weekly_pct_growth_cases', 'biweekly_pct_growth_cases',
                                         'weekly_pct_growth_deaths', 'biweekly_pct_growth_deaths'],
                      title=f'Weekly and Biweekly Growth Rates in {country}',
                      labels={'value': 'Growth Rate (%)', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Growth Rate (%)', legend_title='Metric')
        return fig

    def _plot_weekly_biweekly_growth_map(self, data, country):
        """
        Generate a map for weekly/biweekly growth analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'weekly_pct_growth_cases': 'mean',
            'biweekly_pct_growth_cases': 'mean',
            'weekly_pct_growth_deaths': 'mean',
            'biweekly_pct_growth_deaths': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='weekly_pct_growth_cases',  # Use one metric for coloring
                            title=f'Weekly Case Growth Rates by Country',
                            labels={'weekly_pct_growth_cases': 'Weekly Case Growth (%)'})
        return fig

    def _plot_weekly_biweekly_growth_table(self, data):
        """
        Generate a table for weekly/biweekly growth analysis.
        """
        table = dash_table.DataTable(
            id='weekly-biweekly-growth-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_weekly_biweekly_growth(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for weekly/biweekly growth analysis.
        """
        data = self._process_weekly_biweekly_growth_data(country)

        if visualization_type == 'chart':
            fig = self._plot_weekly_biweekly_growth_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_weekly_biweekly_growth_map(data, country)
        elif visualization_type == 'table':
            return self._plot_weekly_biweekly_growth_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart' or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_cases_deaths_per_million_data(self):
        """
        Process data for cases/deaths per million analysis.
        """
        cases_deaths_per_million = self.cases_deaths.groupby('country').agg({
            'new_cases_per_million': 'max',
            'new_deaths_per_million': 'max'
        }).reset_index()
        return cases_deaths_per_million

    def _plot_cases_deaths_per_million_chart(self, data):
        """
        Generate a bar chart for cases/deaths per million analysis.
        """
        fig = px.bar(data, x='country', y=['new_cases_per_million', 'new_deaths_per_million'],
                     title='Cases and Deaths per Million by Country',
                     labels={'value': 'Count per Million', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Country', yaxis_title='Count per Million', legend_title='Metric')
        return fig

    def _plot_cases_deaths_per_million_map(self, data):
        """
        Generate a map for cases/deaths per million analysis.
        """
        # Create a choropleth map
        fig = px.choropleth(data, locations='country', locationmode='country names',
                            color='new_cases_per_million',  # Use one metric for coloring
                            title='Cases per Million by Country',
                            labels={'new_cases_per_million': 'Cases per Million'})
        return fig

    def _plot_cases_deaths_per_million_table(self, data):
        """
        Generate a table for cases/deaths per million analysis.
        """
        table = dash_table.DataTable(
            id='cases-deaths-per-million-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_cases_deaths_per_million(self, visualization_type='chart'):
        """
        Generate the specified visualization for cases/deaths per million analysis.
        """
        data = self._process_cases_deaths_per_million_data()

        if visualization_type == 'chart':
            fig = self._plot_cases_deaths_per_million_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_cases_deaths_per_million_map(data)
        elif visualization_type == 'table':
            return self._plot_cases_deaths_per_million_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart' or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_policy_impact_data(self, country):
        """
        Process data for policy impact analysis.
        """
        merged_data = pd.merge(
            self.cases_deaths,
            self.government_response,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_policy_impact_chart(self, data, country):
        """
        Generate a line chart for policy impact analysis.
        """
        fig = px.line(data, x='date', y=['new_cases_per_million', 'new_deaths_per_million'],
                      title=f'Impact of Government Policies on Cases and Deaths in {country}',
                      labels={'value': 'Count per Million', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Count per Million', legend_title='Metric')
        return fig

    def _plot_policy_impact_map(self, data, country):
        """
        Generate a map for policy impact analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'new_cases_per_million': 'mean',
            'new_deaths_per_million': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_cases_per_million',  # Use one metric for coloring
                            title=f'Impact of Government Policies on Cases in {country}',
                            labels={'new_cases_per_million': 'Cases per Million'})
        return fig

    def _plot_policy_impact_table(self, data):
        """
        Generate a table for policy impact analysis.
        """
        table = dash_table.DataTable(
            id='policy-impact-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_policy_impact(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for policy impact analysis.
        """
        data = self._process_policy_impact_data(country)

        if visualization_type == 'chart':
            fig = self._plot_policy_impact_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_policy_impact_map(data, country)
        elif visualization_type == 'table':
            return self._plot_policy_impact_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart' or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_reproduction_rate_trends_data(self, country):
        """
        Process data for reproduction rate trends analysis.
        """
        country_data = self.reproduction_rate[self.reproduction_rate['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_reproduction_rate_trends_chart(self, data, country):
        """
        Generate a scatter plot for reproduction rate trends analysis.
        """
        fig = px.scatter(data, x='date', y='r', title=f'Reproduction Rate (R) Trends in {country}',
                         labels={'r': 'Reproduction Rate (R)'})

        # Add confidence intervals
        fig.add_scatter(x=data['date'], y=data['ci_95_l'], mode='lines', line=dict(color='gray', dash='dash'),
                        name='95% CI Lower')
        fig.add_scatter(x=data['date'], y=data['ci_95_u'], mode='lines', line=dict(color='gray', dash='dash'),
                        name='95% CI Upper', fill='tonexty', fillcolor='rgba(0,0,0,0.2)')

        fig.update_layout(xaxis_title='Date', yaxis_title='Reproduction Rate (R)', legend_title='Metric')
        return fig

    def _plot_reproduction_rate_trends_map(self, data, country):
        """
        Generate a map for reproduction rate trends analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'r': 'mean',
            'ci_95_l': 'mean',
            'ci_95_u': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='r',  # Use reproduction rate for coloring
                            title=f'Reproduction Rate (R) Trends by Country',
                            labels={'r': 'Reproduction Rate (R)'})
        return fig

    def _plot_reproduction_rate_trends_table(self, data):
        """
        Generate a table for reproduction rate trends analysis.
        """
        table = dash_table.DataTable(
            id='reproduction-rate-trends-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_reproduction_rate_trends(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for reproduction rate trends analysis.
        """
        data = self._process_reproduction_rate_trends_data(country)

        if visualization_type == 'chart':
            fig = self._plot_reproduction_rate_trends_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_reproduction_rate_trends_map(data, country)
        elif visualization_type == 'table':
            return self._plot_reproduction_rate_trends_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_testing_vs_case_detection_data(self, country):
        """
        Process data for testing vs. case detection analysis.
        """
        merge_data = pd.merge(
            self.testing,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merge_data[merge_data['country'] == country]
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
                            color='new_tests_per_thousand',  # Use testing rate for coloring
                            title=f'Testing Rates vs. Case Detection by Country',
                            labels={'new_tests_per_thousand': 'New Tests per Thousand'})
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

    def _process_case_trends_data(self, country):
        """
        Process data for case trends analysis.
        """
        country_data = self.cases_deaths[self.cases_deaths['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_case_trends_chart(self, data, country):
        """
        Generate a line chart for case trends analysis.
        """
        fig = px.line(data, x='date', y=['new_cases', 'total_cases'],
                      title=f'Cases Trends in {country}',
                      labels={'value': 'Number of Cases', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Number of Cases', legend_title='Metric')
        return fig

    def _plot_case_trends_map(self, data, country):
        """
        Generate a map for case trends analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'new_cases': 'mean',
            'total_cases': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_cases',  # Use new cases for coloring
                            title=f'Case Trends by Country',
                            labels={'new_cases': 'New Cases'})
        return fig

    def _plot_case_trends_table(self, data):
        """
        Generate a table for case trends analysis.
        """
        table = dash_table.DataTable(
            id='case-trends-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_case_trends(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for case trends analysis.
        """
        data = self._process_case_trends_data(country)

        if visualization_type == 'chart':
            fig = self._plot_case_trends_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_case_trends_map(data, country)
        elif visualization_type == 'table':
            return self._plot_case_trends_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_death_trends_data(self, country):
        """
        Process data for death trends analysis.
        """
        country_data = self.cases_deaths[self.cases_deaths['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_death_trends_chart(self, data, country):
        """
        Generate a line chart for death trends analysis.
        """
        fig = px.line(data, x='date', y=['new_deaths', 'total_deaths'],
                      title=f'Death Trends in {country}',
                      labels={'value': 'Number of Deaths', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Number of Deaths', legend_title='Metric')
        return fig

    def _plot_death_trends_map(self, data, country):
        """
        Generate a map for death trends analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'new_deaths': 'mean',
            'total_deaths': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='new_deaths',  # Use new deaths for coloring
                            title=f'Death Trends by Country',
                            labels={'new_deaths': 'New Deaths'})
        return fig

    def _plot_death_trends_table(self, data):
        """
        Generate a table for death trends analysis.
        """
        table = dash_table.DataTable(
            id='death-trends-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_death_trends(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for death trends analysis.
        """
        data = self._process_death_trends_data(country)

        if visualization_type == 'chart':
            fig = self._plot_death_trends_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_death_trends_map(data, country)
        elif visualization_type == 'table':
            return self._plot_death_trends_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_cfr_data_by_country(self, country):
        """
        Process data for CFR over time analysis.
        """
        country_data = self.cases_deaths[self.cases_deaths['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_cfr_by_country_chart(self, data, country):
        """
        Generate a line chart for CFR over time analysis.
        """
        fig = px.line(data, x='date', y='cfr',
                      title=f'Case Fatality Rate (CFR) in {country}',
                      labels={'cfr': 'CFR (%)'})
        fig.update_layout(xaxis_title='Date', yaxis_title='CFR (%)')
        return fig

    def _plot_cfr_by_country_map(self, data, country):
        """
        Generate a map for CFR over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'cfr': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='cfr',  # Use CFR for coloring
                            title=f'Case Fatality Rate (CFR) by Country',
                            labels={'cfr': 'CFR (%)'})
        return fig

    def _plot_cfr_by_country_table(self, data):
        """
        Generate a table for CFR over time analysis.
        """
        table = dash_table.DataTable(
            id='cfr-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_cfr_by_country(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for CFR over time analysis.
        """
        data = self._process_cfr_data_by_country(country)

        if visualization_type == 'chart':
            fig = self._plot_cfr_by_country_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_cfr_by_country_map(data, country)
        elif visualization_type == 'table':
            return self._plot_cfr_by_country_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


if __name__ == "__main__":

    # Initialize the class
    cases_death_analysis = CasesDeathAnalysis()

    # Generate a chart
    chart = cases_death_analysis.plot_cfr_by_country(country='United States', visualization_type='chart')
    chart.show()

    # Generate a map
    map = cases_death_analysis.plot_cfr_by_country(country='United States', visualization_type='map')
    map.show()

    # Generate a table
    table = cases_death_analysis.plot_cfr_by_country(country='United States', visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

    # Run the Dash app
    # if __name__ == "__main__":
    app.run(debug=True)

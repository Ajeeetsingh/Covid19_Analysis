import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class VaccinationAnalysis:
    def __init__(self):
        """
        Initialize the VaccinationAnalysis class with file paths.
        """
        # File paths
        global_vaccinations = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv'
        us_vaccination = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_us_cleaned.csv'
        attitudes = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Attitudes_cleaned.csv'
        manufacture = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_manufacturer_cleaned.csv'
        cases_death = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\cases_deaths_cleaned.csv'
        reproduction_rate = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\reproduction_rate_cleaned.csv'
        excess_mortality = 'F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv'

        # Load datasets
        self.global_vaccination = pd.read_csv(global_vaccinations)
        self.us_vaccination = pd.read_csv(us_vaccination)
        self.attitudes = pd.read_csv(attitudes)
        self.manufacturer_data = pd.read_csv(manufacture)
        self.cases_deaths = pd.read_csv(cases_death)
        self.reproduction_rate = pd.read_csv(reproduction_rate)
        self.excess_mortality = pd.read_csv(excess_mortality)

        # Convert data columns to datetime
        self.global_vaccination['date'] = pd.to_datetime(self.global_vaccination['date'])
        self.us_vaccination['date'] = pd.to_datetime(self.us_vaccination['date'])
        self.attitudes['date'] = pd.to_datetime(self.attitudes['date'])
        self.manufacturer_data['date'] = pd.to_datetime(self.manufacturer_data['date'])
        self.cases_deaths['date'] = pd.to_datetime(self.cases_deaths['date'])
        self.reproduction_rate['date'] = pd.to_datetime(self.reproduction_rate['date'])

        self.excess_mortality['date'] = pd.to_datetime(self.excess_mortality['date'])
        self.excess_mortality.rename(columns={'entity': 'country'}, inplace=True)

    def _process_vaccination_rates_over_time_data(self, country):
        """
        Process data for vaccination rates over time analysis.
        """
        if country == 'United States':
            data = self.us_vaccination
        else:
            data = self.global_vaccination[self.global_vaccination['country'] == country]
            if data.empty:
                raise ValueError(f"No data available for {country}.")
        return data

    def _plot_vaccination_rates_over_time_chart(self, data, country):
        """
        Generate a line chart for vaccination rates over time analysis.
        """
        fig = px.line(data, x='date', y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
                                         'people_with_booster_per_hundred'],
                      title=f'Vaccination Rates Over Time in {country}',
                      labels={'value': 'Percentage of Population', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Percentage of Population', legend_title='Metric')
        return fig

    def _plot_vaccination_rates_over_time_map(self, data, country):
        """
        Generate a map for vaccination rates over time analysis, focusing on the selected country.
        """
        # Filter data for the selected country
        country_data = data[data['country'] == country]

        # Create a choropleth map focused on the selected country
        fig = px.choropleth(country_data, locations='country', locationmode='country names',
                            color='people_vaccinated_per_hundred',  # Use vaccination rate for coloring
                            title=f'Vaccination Rates in {country}',
                            labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)'})
        return fig

    def _plot_vaccination_rates_over_time_table(self, data):
        """
        Generate a table for vaccination rates over time analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-rates-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_rates_over_time(self, country='Argentina', visualization_type='chart'):
        """
        Generate the specified visualization for vaccination rates over time analysis.
        """
        data = self._process_vaccination_rates_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_rates_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_rates_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_rates_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_attitudes_data(self, country):
        """
        Process data for vaccination attitudes analysis.
        """
        country_data = self.attitudes[self.attitudes['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_vaccination_attitudes_chart(self, data, country):
        """
        Generate a line chart for vaccination attitudes analysis.
        """
        fig = px.line(data, x='date', y=['willingness_covid_vaccinate_this_week_pct_pop',
                                         'uncertain_covid_vaccinate_this_week_pct_pop',
                                         'unwillingness_covid_vaccinate_this_week_pct_pop'],
                      title=f'Vaccination Attitudes Over Time in {country}',
                      labels={'value': 'Percentage of Population', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Percentage of Population', legend_title='Metric')
        return fig

    def _plot_vaccination_attitudes_map(self, data, country):
        """
        Generate a map for vaccination attitudes analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'willingness_covid_vaccinate_this_week_pct_pop': 'mean',
            'uncertain_covid_vaccinate_this_week_pct_pop': 'mean',
            'unwillingness_covid_vaccinate_this_week_pct_pop': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='willingness_covid_vaccinate_this_week_pct_pop',  # Use willingness for coloring
                            title=f'Vaccination Attitudes by Country',
                            labels={'willingness_covid_vaccinate_this_week_pct_pop': 'Willingness (%)'})
        return fig

    def _plot_vaccination_attitudes_table(self, data):
        """
        Generate a table for vaccination attitudes analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-attitudes-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_attitudes(self, country='Australia', visualization_type='chart'):
        """
        Generate the specified visualization for vaccination attitudes analysis.
        """
        data = self._process_vaccination_attitudes_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_attitudes_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_attitudes_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_attitudes_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_by_age_group_data(self, country, date='2023-01-01'):
        """
        Process data for vaccination by age group analysis.
        """
        if country == 'United States':
            raise ValueError("Age group data not available for the United States in this dataset.")

        age_data = self.global_vaccination[
            (self.global_vaccination['country'] == country) &
            (self.global_vaccination['date'] == date)
            ]
        if age_data.empty:
            raise ValueError(f"No data available for {country} on {date}.")
        return age_data

    def _plot_vaccination_by_age_group_chart(self, data, country, date):
        """
        Generate a bar chart for vaccination by age group analysis.
        """
        fig = px.bar(data, x='age_group', y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred'],
                     title=f'Vaccination Rates by Age Group in {country} on {date}',
                     labels={'value': 'Percentage of Population', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Age Group', yaxis_title='Percentage of Population', legend_title='Metric')
        return fig

    def _plot_vaccination_by_age_group_map(self, data, country, date):
        """
        Generate a map for vaccination by age group analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'people_fully_vaccinated_per_hundred': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='people_vaccinated_per_hundred',  # Use vaccination rate for coloring
                            title=f'Vaccination Rates by Age Group in {country} on {date}',
                            labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)'})
        return fig

    def _plot_vaccination_by_age_group_table(self, data):
        """
        Generate a table for vaccination by age group analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-by-age-group-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_by_age_group(self, country, date='2023-01-01', visualization_type='chart'):
        """
        Generate the specified visualization for vaccination by age group analysis.
        """
        data = self._process_vaccination_by_age_group_data(country, date)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_by_age_group_chart(data, country, date)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_by_age_group_map(data, country, date)
        elif visualization_type == 'table':
            return self._plot_vaccination_by_age_group_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_by_manufacturer_data(self, country):
        """
        Process data for vaccination by manufacturer analysis.
        """
        country_data = self.manufacturer_data[self.manufacturer_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_vaccination_by_manufacturer_chart(self, data, country):
        """
        Generate a bar chart for vaccination by manufacturer analysis.
        """
        fig = px.bar(data, x='vaccine', y='total_vaccinations',
                     title=f'Total Vaccination by Manufacturer in {country}',
                     labels={'total_vaccinations': 'Total Vaccinations', 'vaccine': 'Vaccine Manufacturer'})
        fig.update_layout(xaxis_title='Vaccine Manufacturer', yaxis_title='Total Vaccinations')
        return fig

    def _plot_vaccination_by_manufacturer_map(self, data, country):
        """
        Generate a map for vaccination by manufacturer analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'total_vaccinations': 'sum'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='total_vaccinations',  # Use total vaccinations for coloring
                            title=f'Total Vaccination by Manufacturer in {country}',
                            labels={'total_vaccinations': 'Total Vaccinations'})
        return fig

    def _plot_vaccination_by_manufacturer_table(self, data):
        """
        Generate a table for vaccination by manufacturer analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-by-manufacturer-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_by_manufacturer(self, country='Argentina', visualization_type='chart'):
        """
        Generate the specified visualization for vaccination by manufacturer analysis.
        """
        data = self._process_vaccination_by_manufacturer_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_by_manufacturer_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_by_manufacturer_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_by_manufacturer_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_vs_cfr_data(self, country):
        """
        Process data for vaccination vs. CFR analysis.
        """
        if country == 'United States':
            vaccination_data = self.us_vaccination
            vaccination_data['country'] = 'United States'  # Add country column for merging
        else:
            vaccination_data = self.global_vaccination

        # Merge vaccination data with case and death data
        merged_data = pd.merge(
            vaccination_data,
            self.cases_deaths,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_vaccination_vs_cfr_chart(self, data, country):
        """
        Generate a scatter plot for vaccination vs. CFR analysis.
        """
        fig = px.scatter(data, x='people_vaccinated_per_hundred', y='cfr',
                         title=f'Vaccination Rate vs. Case Fatality Rate in {country}',
                         labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)',
                                 'cfr': 'Case Fatality Rate (%)'})
        fig.update_layout(xaxis_title='Vaccination Rate (%)', yaxis_title='Case Fatality Rate (%)')
        return fig

    def _plot_vaccination_vs_cfr_map(self, data, country):
        """
        Generate a map for vaccination vs. CFR analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'cfr': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='cfr',  # Use CFR for coloring
                            title=f'Case Fatality Rate by Country',
                            labels={'cfr': 'Case Fatality Rate (%)'})
        return fig

    def _plot_vaccination_vs_cfr_table(self, data):
        """
        Generate a table for vaccination vs. CFR analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-vs-cfr-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_vs_cfr(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for vaccination vs. CFR analysis.
        """
        data = self._process_vaccination_vs_cfr_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_vs_cfr_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_vs_cfr_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_vs_cfr_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_vs_reproduction_rate_data(self, country):
        """
        Process data for vaccination vs. reproduction rate analysis.
        """
        merged_data = pd.merge(
            self.global_vaccination,
            self.reproduction_rate,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_vaccination_vs_reproduction_rate_chart(self, data, country):
        """
        Generate a line chart for vaccination vs. reproduction rate analysis.
        """
        fig = px.line(data, x='date', y=['people_vaccinated_per_hundred', 'r'],
                      title=f'Vaccination Rate vs. Reproduction Rate in {country}',
                      labels={'value': 'Rate', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Rate', legend_title='Metric')
        return fig

    def _plot_vaccination_vs_reproduction_rate_map(self, data, country):
        """
        Generate a map for vaccination vs. reproduction rate analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'r': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='r',  # Use reproduction rate for coloring
                            title=f'Reproduction Rate by Country',
                            labels={'r': 'Reproduction Rate (R)'})
        return fig

    def _plot_vaccination_vs_reproduction_rate_table(self, data):
        """
        Generate a table for vaccination vs. reproduction rate analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-vs-reproduction-rate-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_vs_reproduction_rate(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for vaccination vs. reproduction rate analysis.
        """
        data = self._process_vaccination_vs_reproduction_rate_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_vs_reproduction_rate_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_vs_reproduction_rate_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_vs_reproduction_rate_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_vaccination_vs_excess_mortality_data(self, country):
        """
        Process data for vaccination vs. excess mortality analysis.
        """
        merged_data = pd.merge(
            self.global_vaccination,
            self.excess_mortality,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_vaccination_vs_excess_mortality_chart(self, data, country):
        """
        Generate a scatter plot for vaccination vs. excess mortality analysis.
        """
        fig = px.scatter(data, x='people_vaccinated_per_hundred', y='excess_proj_all_ages',
                         title=f'Vaccination Rate vs. Excess Mortality in {country}',
                         labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)',
                                 'excess_proj_all_ages': 'Excess Mortality'})
        fig.update_layout(xaxis_title='Vaccination Rate (%)', yaxis_title='Excess Mortality')
        return fig

    def _plot_vaccination_vs_excess_mortality_map(self, data, country):
        """
        Generate a map for vaccination vs. excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_vaccination_vs_excess_mortality_table(self, data):
        """
        Generate a table for vaccination vs. excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='vaccination-vs-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_vaccination_vs_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for vaccination vs. excess mortality analysis.
        """
        data = self._process_vaccination_vs_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_vaccination_vs_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_vaccination_vs_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_vaccination_vs_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_us_vaccination_trends_data(self):
        """
        Process data for US vaccination trends analysis.
        """
        return self.us_vaccination

    def _plot_us_vaccination_trends_chart(self, data):
        """
        Generate a line chart for US vaccination trends analysis.
        """
        fig = px.line(data, x='date', y=['people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred',
                                         'total_boosters_per_hundred'],
                      title='Vaccination Trends in the United States',
                      labels={'value': 'Percentage of Population', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Percentage of Population', legend_title='Metric')
        return fig

    def _plot_us_vaccination_trends_map(self, data):
        """
        Generate a map for US vaccination trends analysis.
        """
        # Aggregate data by state for the map
        aggregated_data = data.groupby('state').agg({
            'people_vaccinated_per_hundred': 'mean',
            'people_fully_vaccinated_per_hundred': 'mean',
            'total_boosters_per_hundred': 'mean'
        }).reset_index()

        # Filter out non-state entries
        valid_states = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois',
            'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
            'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
            'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota',
            'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ]
        aggregated_data = aggregated_data[aggregated_data['state'].isin(valid_states)]

        # Ensure state names are in title case
        aggregated_data['state'] = aggregated_data['state'].str.title()

        # Create a choropleth map for US states
        fig = px.choropleth(aggregated_data,
                            locations='state',  # Column containing state names
                            locationmode='USA-states',  # Use 'USA-states' for U.S. state-level maps
                            color='people_vaccinated_per_hundred',  # Use vaccination rate for coloring
                            scope="usa",  # Focus on the USA
                            title='Vaccination Trends in the United States',
                            labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)'},
                            color_continuous_scale='Blues',  # Use a color scale
                            range_color=[0, 100])  # Set the range of the color scale from 0 to 100

        return fig

    def _plot_us_vaccination_trends_table(self, data):
        """
        Generate a table for US vaccination trends analysis.
        """
        table = dash_table.DataTable(
            id='us-vaccination-trends-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_us_vaccination_trends(self, visualization_type='chart'):
        """
        Generate the specified visualization for US vaccination trends analysis.
        """
        data = self._process_us_vaccination_trends_data()

        if visualization_type == 'chart':
            fig = self._plot_us_vaccination_trends_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_us_vaccination_trends_map(data)
        elif visualization_type == 'table':
            return self._plot_us_vaccination_trends_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


if __name__ == "__main__":

    # Initialize the class with file paths
    vaccination_analysis = VaccinationAnalysis()

    # Generate a chart
    # chart = vaccination_analysis.plot_vaccination_by_age_group(country='Uruguay', date='2021-03-01',
    # visualization_type='chart')
    chart = vaccination_analysis.plot_vaccination_rates_over_time(country='Argentina', visualization_type='chart')
    chart.show()

    # Generate a map
    map = vaccination_analysis.plot_vaccination_rates_over_time(country='Argentina', visualization_type='map')
    map.show()

    # Generate a table
    table = vaccination_analysis.plot_vaccination_rates_over_time(country='Argentina', visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

# Run the Dash app
# if __name__ == "__main__":
    app.run(debug=True)


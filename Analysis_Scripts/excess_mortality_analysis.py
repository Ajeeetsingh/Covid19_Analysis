import pandas as pd
import plotly.express as px
from dash import Dash, html, dash_table
from dash import dcc


class ExcessMortalityAnalysis:
    def __init__(self):
        """
        Initialize the ExcessMortalityAnalysis class with file paths.
        """
        excess_mortality_path = "F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\excess_mortality_cleaned.csv"
        vaccinations_path = "F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\vaccinations_age_cleaned_new.csv"
        government_response_path = "F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\Government_response_policy_cleaned.csv"
        healthcare_path = "F:\\PycharmProjects\\Covid_19_Project\\cleaned_data\\hospital_cleaned.csv"

        # Load dataset
        self.excess_mortality = pd.read_csv(excess_mortality_path)
        self.vaccinations = pd.read_csv(vaccinations_path)
        self.government_response = pd.read_csv(government_response_path)
        self.healthcare = pd.read_csv(healthcare_path)
        self.healthcare.columns = self.healthcare.columns.str.strip()

        # Convert date column to datetime
        self.excess_mortality['date'] = pd.to_datetime(self.excess_mortality['date'])
        self.excess_mortality.rename(columns={'entity': 'country'}, inplace=True)
        self.vaccinations['date'] = pd.to_datetime(self.vaccinations['date'])
        self.government_response['date'] = pd.to_datetime(self.government_response['date'])
        self.healthcare['date'] = pd.to_datetime(self.healthcare['date'])

    def _process_excess_mortality_over_time_data(self, country):
        """
        Process data for excess mortality over time analysis.
        """
        country_data = self.excess_mortality[self.excess_mortality['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_excess_mortality_over_time_chart(self, data, country):
        """
        Generate a line chart for excess mortality over time analysis.
        """
        fig = px.line(data, x='date', y='excess_proj_all_ages',
                      title=f'Excess Mortality Over Time in {country}',
                      labels={'excess_proj_all_ages': 'Excess Mortality'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Excess Mortality')
        return fig

    def _plot_excess_mortality_over_time_map(self, data, country):
        """
        Generate a map for excess mortality over time analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_excess_mortality_over_time_table(self, data):
        """
        Generate a table for excess mortality over time analysis.
        """
        table = dash_table.DataTable(
            id='excess-mortality-over-time-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_excess_mortality_over_time(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for excess mortality over time analysis.
        """
        data = self._process_excess_mortality_over_time_data(country)

        if visualization_type == 'chart':
            fig = self._plot_excess_mortality_over_time_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_excess_mortality_over_time_map(data, country)
        elif visualization_type == 'table':
            return self._plot_excess_mortality_over_time_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_age_specific_excess_mortality_data(self, country):
        """
        Process data for age-specific excess mortality analysis.
        """
        country_data = self.excess_mortality[self.excess_mortality['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")

        # Select age-specific columns and include the 'country' column
        age_columns = ['p_avg_0_14', 'p_avg_15_64', 'p_avg_65_74', 'p_avg_75_84', 'p_avg_85p']
        age_data = country_data[['date', 'country'] + age_columns].melt(
            id_vars=['date', 'country'], var_name='Age Group', value_name='Excess Mortality'
        )
        return age_data

    def _plot_age_specific_excess_mortality_chart(self, data, country):
        """
        Generate a line chart for age-specific excess mortality analysis.
        """
        # Debugging: Print the data to check its contents
        # print(data.head())

        fig = px.line(data, x='date', y='Excess Mortality', color='Age Group',
                      title=f'Age-Specific Excess Mortality Rates in {country}',
                      labels={'Excess Mortality': 'Excess Mortality'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Excess Mortality', legend_title='Age Group')
        return fig

    def _plot_age_specific_excess_mortality_map(self, data, country):
        """
        Generate a map for age-specific excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country', as_index=False).agg({
            'Excess Mortality': 'mean'
        })

        # Create a choropleth map
        fig = px.choropleth(aggregated_data,
                            locations='country',
                            locationmode='country names',
                            color='Excess Mortality',  # Use excess mortality for coloring
                            title=f'Age-Specific Excess Mortality in {country}',
                            labels={'Excess Mortality': 'Excess Mortality'})
        return fig

    def _plot_age_specific_excess_mortality_table(self, data):
        """
        Generate a table for age-specific excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='age-specific-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10,
            sort_action='native',  # Enable sorting
            filter_action='native',  # Enable filtering
            style_table={'height': '300px', 'overflowY': 'auto'}  # Add scroll for large datasets
        )
        return table

    def plot_age_specific_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for age-specific excess mortality analysis.
        """
        data = self._process_age_specific_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_age_specific_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_age_specific_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_age_specific_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_projected_vs_actual_deaths_data(self, country):
        """
        Process data for projected vs. actual deaths analysis.
        """
        country_data = self.excess_mortality[self.excess_mortality['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_projected_vs_actual_deaths_chart(self, data, country):
        """
        Generate a line chart for projected vs. actual deaths analysis.
        """
        fig = px.line(data, x='date', y=['projected_deaths_since_2020_all_ages', 'deaths_since_2020_all_ages'],
                      title=f'Projected vs. Actual Deaths in {country}',
                      labels={'value': 'Number of Deaths', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Number of Deaths', legend_title='Metric')
        return fig

    def _plot_projected_vs_actual_deaths_map(self, data, country):
        """
        Generate a map for projected vs. actual deaths analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'projected_deaths_since_2020_all_ages': 'mean',
            'deaths_since_2020_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='projected_deaths_since_2020_all_ages',  # Use projected deaths for coloring
                            title=f'Projected Deaths by Country',
                            labels={'projected_deaths_since_2020_all_ages': 'Projected Deaths'})
        return fig

    def _plot_projected_vs_actual_deaths_table(self, data):
        """
        Generate a table for projected vs. actual deaths analysis.
        """
        table = dash_table.DataTable(
            id='projected-vs-actual-deaths-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_projected_vs_actual_deaths(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for projected vs. actual deaths analysis.
        """
        data = self._process_projected_vs_actual_deaths_data(country)

        if visualization_type == 'chart':
            fig = self._plot_projected_vs_actual_deaths_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_projected_vs_actual_deaths_map(data, country)
        elif visualization_type == 'table':
            return self._plot_projected_vs_actual_deaths_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_cumulative_excess_mortality_data(self, country):
        """
        Process data for cumulative excess mortality analysis.
        """
        country_data = self.excess_mortality[self.excess_mortality['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_cumulative_excess_mortality_chart(self, data, country):
        """
        Generate a line chart for cumulative excess mortality analysis.
        """
        fig = px.line(data, x='date', y='cum_excess_proj_all_ages',
                      title=f'Cumulative Excess Mortality in {country}',
                      labels={'cum_excess_proj_all_ages': 'Cumulative Excess Mortality'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Excess Mortality')
        return fig

    def _plot_cumulative_excess_mortality_map(self, data, country):
        """
        Generate a map for cumulative excess mortality analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'cum_excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='cum_excess_proj_all_ages',  # Use cumulative excess mortality for coloring
                            title=f'Cumulative Excess Mortality by Country',
                            labels={'cum_excess_proj_all_ages': 'Cumulative Excess Mortality'})
        return fig

    def _plot_cumulative_excess_mortality_table(self, data):
        """
        Generate a table for cumulative excess mortality analysis.
        """
        table = dash_table.DataTable(
            id='cumulative-excess-mortality-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_cumulative_excess_mortality(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for cumulative excess mortality analysis.
        """
        data = self._process_cumulative_excess_mortality_data(country)

        if visualization_type == 'chart':
            fig = self._plot_cumulative_excess_mortality_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_cumulative_excess_mortality_map(data, country)
        elif visualization_type == 'table':
            return self._plot_cumulative_excess_mortality_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_excess_mortality_by_country_data(self):
        """
        Process data for excess mortality by country analysis.
        """
        excess_mortality_by_country = self.excess_mortality.groupby('country')[
            'excess_proj_all_ages'].max().reset_index()
        return excess_mortality_by_country

    def _plot_excess_mortality_by_country_chart(self, data):
        """
        Generate a bar chart for excess mortality by country analysis.
        """
        fig = px.bar(data, x='country', y='excess_proj_all_ages',
                     title='Excess Mortality by Country',
                     labels={'excess_proj_all_ages': 'Excess Mortality', 'country': 'Country'})
        fig.update_layout(xaxis_title='Country', yaxis_title='Excess Mortality')
        return fig

    def _plot_excess_mortality_by_country_map(self, data):
        """
        Generate a map for excess mortality by country analysis.
        """
        # Create a choropleth map
        fig = px.choropleth(data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title='Excess Mortality by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_excess_mortality_by_country_table(self, data):
        """
        Generate a table for excess mortality by country analysis.
        """
        table = dash_table.DataTable(
            id='excess-mortality-by-country-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_excess_mortality_by_country(self, visualization_type='chart'):
        """
        Generate the specified visualization for excess mortality by country analysis.
        """
        data = self._process_excess_mortality_by_country_data()

        if visualization_type == 'chart':
            fig = self._plot_excess_mortality_by_country_chart(data)
        elif visualization_type == 'map':
            fig = self._plot_excess_mortality_by_country_map(data)
        elif visualization_type == 'table':
            return self._plot_excess_mortality_by_country_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_excess_mortality_vs_vaccination_data(self, country):
        """
        Process data for excess mortality vs. vaccination analysis.

        This function resamples the data to a weekly frequency and computes the mean
        for each week. It does not use exact dates but rather aggregates data into
        weekly averages for analysis.
        """
        # Clean country names
        self.excess_mortality['country'] = self.excess_mortality['country'].str.strip().str.title()
        self.vaccinations['country'] = self.vaccinations['country'].str.strip().str.title()

        # Select only numeric columns for resampling
        numeric_cols_excess = ['excess_proj_all_ages']  # Add other numeric columns if needed
        numeric_cols_vaccinations = ['people_vaccinated_per_hundred']  # Add other numeric columns if needed

        # Resample excess_mortality to weekly frequency
        excess_mortality_resampled = (
            self.excess_mortality[['country', 'date'] + numeric_cols_excess]
            .set_index('date')
            .groupby('country')
            .resample('W')
            .mean()
            .reset_index()
        )

        # Resample vaccinations to weekly frequency
        vaccinations_resampled = (
            self.vaccinations[['country', 'date'] + numeric_cols_vaccinations]
            .set_index('date')
            .groupby('country')
            .resample('W')
            .mean()
            .reset_index()
        )

        # Merge the resampled datasets
        merged_data = pd.merge(
            excess_mortality_resampled,
            vaccinations_resampled,
            on=['country', 'date']
        )

        # Filter data for the specified country
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data
    def _plot_excess_mortality_vs_vaccination_chart(self, data, country):
        """
        Generate a scatter plot for excess mortality vs. vaccination analysis.
        """
        fig = px.scatter(data, x='people_vaccinated_per_hundred', y='excess_proj_all_ages',
                         title=f'Excess Mortality vs. Vaccination Rate in {country}',
                         labels={'people_vaccinated_per_hundred': 'Vaccination Rate (%)',
                                 'excess_proj_all_ages': 'Excess Mortality'})
        fig.update_layout(xaxis_title='Vaccination Rate (%)', yaxis_title='Excess Mortality')
        return fig

    def _plot_excess_mortality_vs_vaccination_map(self, data, country):
        """
        Generate a map for excess mortality vs. vaccination analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'people_vaccinated_per_hundred': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality vs. Vaccination Rate by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_excess_mortality_vs_vaccination_table(self, data):
        """
        Generate a table for excess mortality vs. vaccination analysis.
        """
        table = dash_table.DataTable(
            id='excess-mortality-vs-vaccination-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_excess_mortality_vs_vaccination(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for excess mortality vs. vaccination analysis.
        """
        data = self._process_excess_mortality_vs_vaccination_data(country)

        if visualization_type == 'chart':
            fig = self._plot_excess_mortality_vs_vaccination_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_excess_mortality_vs_vaccination_map(data, country)
        elif visualization_type == 'table':
            return self._plot_excess_mortality_vs_vaccination_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_excess_mortality_vs_policies_data(self, country):
        """
        Process data for excess mortality vs. policies analysis.
        """
        merged_data = pd.merge(
            self.excess_mortality,
            self.government_response,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_excess_mortality_vs_policies_chart(self, data, country):
        """
        Generate a line chart for excess mortality vs. policies analysis.
        """
        fig = px.line(data, x='date', y=['excess_proj_all_ages', 'stringency_index'],
                      title=f'Excess Mortality vs. Government Policies in {country}',
                      labels={'value': 'Value', 'variable': 'Metric'})
        fig.update_layout(xaxis_title='Date', yaxis_title='Value', legend_title='Metric')
        return fig

    def _plot_excess_mortality_vs_policies_map(self, data, country):
        """
        Generate a map for excess mortality vs. policies analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'excess_proj_all_ages': 'mean',
            'stringency_index': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality vs. Government Policies by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_excess_mortality_vs_policies_table(self, data):
        """
        Generate a table for excess mortality vs. policies analysis.
        """
        table = dash_table.DataTable(
            id='excess-mortality-vs-policies-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_excess_mortality_vs_policies(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for excess mortality vs. policies analysis.
        """
        data = self._process_excess_mortality_vs_policies_data(country)

        if visualization_type == 'chart':
            fig = self._plot_excess_mortality_vs_policies_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_excess_mortality_vs_policies_map(data, country)
        elif visualization_type == 'table':
            return self._plot_excess_mortality_vs_policies_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)

    def _process_excess_mortality_vs_healthcare_data(self, country):
        """
        Process data for excess mortality vs. healthcare analysis.
        """
        merged_data = pd.merge(
            self.excess_mortality,
            self.healthcare,
            on=['country', 'date']
        )
        country_data = merged_data[merged_data['country'] == country]
        if country_data.empty:
            raise ValueError(f"No data available for {country}.")
        return country_data

    def _plot_excess_mortality_vs_healthcare_chart(self, data, country):
        """
        Generate a scatter plot for excess mortality vs. healthcare analysis.
        """
        fig = px.scatter(data, x='daily_occupancy_icu_per_1m', y='excess_proj_all_ages',
                         title=f'Excess Mortality vs. ICU Occupancy in {country}',
                         labels={'daily_occupancy_icu_per_1m': 'ICU Occupancy per Million',
                                 'excess_proj_all_ages': 'Excess Mortality'})
        fig.update_layout(xaxis_title='ICU Occupancy per Million', yaxis_title='Excess Mortality')
        return fig

    def _plot_excess_mortality_vs_healthcare_map(self, data, country):
        """
        Generate a map for excess mortality vs. healthcare analysis.
        """
        # Aggregate data by country for the map
        aggregated_data = data.groupby('country').agg({
            'daily_occupancy_icu_per_1m': 'mean',
            'excess_proj_all_ages': 'mean'
        }).reset_index()

        # Create a choropleth map
        fig = px.choropleth(aggregated_data, locations='country', locationmode='country names',
                            color='excess_proj_all_ages',  # Use excess mortality for coloring
                            title=f'Excess Mortality vs. ICU Occupancy by Country',
                            labels={'excess_proj_all_ages': 'Excess Mortality'})
        return fig

    def _plot_excess_mortality_vs_healthcare_table(self, data):
        """
        Generate a table for excess mortality vs. healthcare analysis.
        """
        table = dash_table.DataTable(
            id='excess-mortality-vs-healthcare-table',
            columns=[{"name": i, "id": i} for i in data.columns],
            data=data.to_dict('records'),
            page_size=10
        )
        return table

    def plot_excess_mortality_vs_healthcare(self, country, visualization_type='chart'):
        """
        Generate the specified visualization for excess mortality vs. healthcare analysis.
        """
        data = self._process_excess_mortality_vs_healthcare_data(country)

        if visualization_type == 'chart':
            fig = self._plot_excess_mortality_vs_healthcare_chart(data, country)
        elif visualization_type == 'map':
            fig = self._plot_excess_mortality_vs_healthcare_map(data, country)
        elif visualization_type == 'table':
            return self._plot_excess_mortality_vs_healthcare_table(data)
        else:
            raise ValueError("Invalid visualization type. Choose 'chart', 'map', or 'table'.")

        return dcc.Graph(figure=fig)


# Example usage
if __name__ == "__main__":

    # Initialize the class with file paths
    excess_mortality_analysis = ExcessMortalityAnalysis()

    # Generate a chart
    chart = excess_mortality_analysis.plot_excess_mortality_vs_healthcare(country='Austria', visualization_type='chart')
    chart.show()

    # Generate a map
    map = excess_mortality_analysis.plot_excess_mortality_vs_healthcare(country='Austria', visualization_type='map')
    map.show()

    # Generate a table
    table = excess_mortality_analysis.plot_excess_mortality_vs_healthcare(country='Austria', visualization_type='table')

    # Create a minimal Dash app to display the table
    app = Dash(__name__)
    app.layout = html.Div([table])

# # Run the Dash app
# if __name__ == "__main__":
    app.run(debug=True)

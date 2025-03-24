import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from cases_death_analysis import CasesDeathAnalysis
from vaccination_analysis import VaccinationAnalysis
from policy_analysis import PolicyAnalysis
from testing_healthcare_analysis import TestingHealthcareAnalysis
from excess_mortality_analysis import ExcessMortalityAnalysis
from mobility_analysis import MobilityAnalysis

# List of countries
countries = [
    'United States', 'India', 'Qatar', 'Mauritania', 'Africa', 'Czechia', 'Bulgaria', 'Netherlands', 'Afghanistan',
    'Lithuania', 'Peru', 'Madagascar', 'Mauritius', 'Andorra', 'Aruba', 'Marshall Islands', 'Montserrat', 'Brazil',
    'Congo', 'Iceland', 'Pitcairn', 'Bolivia', 'Niger', 'North Macedonia', 'Palau', 'Greenland', 'Suriname', 'Vatican',
    'Palestine', 'Iran', 'Indonesia', 'Latvia', 'Finland', 'Egypt', 'United Arab Emirates', 'Gibraltar', 'Greece',
    'Russia', 'Belgium', 'Ukraine', 'Belarus', 'Senegal', 'North Korea', 'Armenia', 'Colombia', 'Romania', 'Poland',
    'Comoros', 'Panama', 'Tuvalu', 'Cambodia', 'Taiwan', 'Cuba', 'South Africa', 'Israel', 'Yemen', 'Grenada', 'Morocco'
    , 'Samoa', 'Argentina', 'Turkey', 'Ireland', 'Hong Kong', 'Zimbabwe', 'Japan', 'Thailand', 'Benin', 'Kenya', 'Nepal'
    , 'Philippines', 'Tonga', 'Singapore', 'Anguilla', 'Gabon', 'Burundi', 'Namibia', 'Myanmar', 'Europe', 'Uruguay',
    'Nigeria', 'France', 'Uzbekistan', 'New Caledonia', 'Australia', 'Bangladesh', 'Georgia', 'Sierra Leone', 'Canada',
    'Saudi Arabia', 'Slovakia',  'New Zealand', 'China', 'Norway', 'Bahrain', 'United Kingdom', 'Liechtenstein'
    , 'South Korea', 'Asia', 'Portugal', 'Germany', 'Sweden', 'Bahamas', 'Iraq', 'Spain', 'Denmark', 'Pakistan'
]
countries.sort()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize the classes
cases_death_analysis = CasesDeathAnalysis()
vaccination_analysis = VaccinationAnalysis()
policy_analysis = PolicyAnalysis()
testing_healthcare_analysis = TestingHealthcareAnalysis()
excess_mortality_analysis = ExcessMortalityAnalysis()
mobility_analysis = MobilityAnalysis()

# Define the layout
app.layout = html.Div([
    # Header
    dbc.Row([
        dbc.Col(html.H1("COVID-19 Data Explorer", style={
            'font-size': '36px',
            'font-weight': 'bold',
            'color': '#2c3e50',
            'text-align': 'center',
            'margin-top': '10px',  # Reduced top margin
            'margin-bottom': '10px'  # Reduced bottom margin
        }), className="mb-2")  # Reduced margin bottom
    ], style={'padding': '10px', 'background-color': '#f8f9fa'}),  # Reduced padding

    # Filters and Visualizations
    dbc.Row([
        # Left Side: Filters and Navigation
        dbc.Col([
            # Search Bar
            dcc.Dropdown(
                id='search-bar',
                options=[{'label': country, 'value': country} for country in countries],
                placeholder="Type to search for a country",
                style={'width': '100%'},
                searchable=True,
                multi=True
            ),

            # Country List with Scroll Bar
            html.Div([
                html.Label("Sort by relevance", style={'font-weight': 'bold', 'color': '#495057'}),  # Styled label
                html.Div(
                    dcc.Checklist(
                        id='country-checklist',
                        options=[{'label': country, 'value': country} for country in countries],
                        value=['United States']
                    ),
                    style={'height': '300px', 'overflow-y': 'scroll', 'border': '1px solid #ddd', 'padding': '10px',
                           'border-radius': '8px'}  # Rounded edges
                )
            ], style={'margin-top': '10px'}),

            # Filters
            html.Div([
                html.Label("Metric", style={'font-weight': 'bold', 'color': '#495057'}),  # Styled label
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'CFR', 'value': 'cfr'},
                        {'label': 'Weekly/Biweekly Growth', 'value': 'weekly_biweekly_growth'},
                        {'label': 'Cases/Deaths per Million', 'value': 'cases_deaths_per_million'},
                        {'label': 'Policy Impact', 'value': 'policy_impact'},
                        {'label': 'Reproduction Rate Trends', 'value': 'reproduction_rate_trends'},
                        {'label': 'Testing vs. Case Detection', 'value': 'testing_vs_case_detection'},
                        {'label': 'Case Trends', 'value': 'case_trends'},
                        {'label': 'Death Trends', 'value': 'death_trends'},
                        {'label': 'CFR by Country', 'value': 'cfr_by_country'},
                        {'label': 'Vaccination Rate', 'value': 'vaccination_rates_over_time'},
                        {'label': 'Vaccination Attitudes', 'value': 'vaccination_attitudes'},
                        {'label': 'Vaccination by age-group', 'value': 'vaccination_by_age_group'},
                        {'label': 'Vaccination Manufacturer', 'value': 'vaccination_by_manufacturer'},
                        {'label': 'Vaccination vs CFR', 'value': 'vaccination_vs_cfr'},
                        {'label': 'Vaccination vs Reproduction rate', 'value': 'vaccination_vs_reproduction_rate'},
                        {'label': 'Vaccination vs mortality', 'value': 'vaccination_vs_excess_mortality'},
                        {'label': 'Vaccination Trends', 'value': 'us_vaccination_trends'},
                        {'label': 'Policy Stringency', 'value': 'policy_stringency_over_time'},
                        {'label': 'Policy Impact on Cases & Deaths', 'value': 'policy_impact_on_cases_deaths'},
                        {'label': 'Policy Impact on Mobility', 'value': 'policy_impact_on_mobility'},
                        {'label': 'Policy Impact on Vaccination', 'value': 'policy_impact_on_vaccination'},
                        {'label': 'Policy Impact on Mortality', 'value': 'policy_impact_on_excess_mortality'},
                        {'label': 'Policy Effectiveness', 'value': 'policy_effectiveness_by_country'},
                        {'label': 'Testing Rates', 'value': 'testing_rates_over_time'},
                        {'label': 'Healthcare Capacity', 'value': 'healthcare_capacity_over_time'},
                        {'label': 'Healthcare Capacity vs CFR', 'value': 'healthcare_capacity_vs_cfr'},
                        {'label': 'Healthcare Capacity vs Mortality', 'value': 'healthcare_capacity_vs_excess_mortality'},
                        {'label': 'Testing Healthcare', 'value': 'testing_healthcare_by_country'},
                        {'label': 'Mortality Over Time', 'value': 'excess_mortality_over_time'},
                        {'label': 'Age Specific Mortality', 'value': 'age_specific_excess_mortality'},
                        {'label': 'Cumulative Mortality', 'value': 'cumulative_excess_mortality'},
                        {'label': 'Mortality by Country', 'value': 'excess_mortality_by_country'},
                        {'label': 'Mortality vs Vaccination', 'value': 'excess_mortality_vs_vaccination'},
                        {'label': 'Mortality vs Policies', 'value': 'excess_mortality_vs_policies'},
                        {'label': 'Mortality vs Healthcare', 'value': 'excess_mortality_vs_healthcare'},
                        {'label': 'Mobility Trend', 'value': 'mobility_trends_over_time'},
                        {'label': 'Mobility Trend by Country', 'value': 'mobility_trends_by_country'},
                        {'label': 'Mobility vs Cases', 'value': 'mobility_vs_case_growth'},
                        {'label': 'Mobility vs Policies', 'value': 'mobility_vs_policies'},
                        {'label': 'Mobility vs Vaccination', 'value': 'mobility_vs_vaccination'},
                        {'label': 'Mobility vs Mortality', 'value': 'mobility_vs_excess_mortality'}
                    ],
                    value='cfr',  # Default value
                    placeholder="Select a metric",
                    style={'width': '100%', 'min-width': '250px'}  # Increase width
                ),

                # Interval Dropdown
                html.Label("Interval", style={'font-weight': 'bold', 'color': '#495057', 'margin-top': '10px'}),
                # Styled label
                dcc.Dropdown(
                    id='interval-dropdown',
                    options=[
                        {'label': 'Daily', 'value': 'daily'},
                        {'label': 'Weekly', 'value': 'weekly'},
                        {'label': 'Monthly', 'value': 'monthly'}
                    ],
                    value='daily',  # Default value
                    style={'width': '100%'}
                ),

                # Relative to Population Dropdown
                html.Label("Relative to population",
                           style={'font-weight': 'bold', 'color': '#495057', 'margin-top': '10px'}),  # Styled label
                dcc.Dropdown(
                    id='population-dropdown',
                    options=[
                        {'label': 'Per million', 'value': 'per_million'},
                        {'label': 'Total', 'value': 'total'}
                    ],
                    value='per_million',  # Default value
                    style={'width': '100%'}
                )
            ], style={'margin-top': '20px'})
        ], width=3, style={
            'padding': '10px',
            'background-color': '#f0f4f8',
            'border-right': '1px solid #ddd',
            'border-radius': '8px',
            'margin-right': '10px'  # Add gap between left and right
        }),

        # Right Side: Visualizations
        dbc.Col([
            # Visualization Tabs (smaller and organized)
            dcc.Tabs(id='visualization-tabs', value='chart', children=[
                dcc.Tab(
                    label='Chart',
                    value='chart',
                    style={'padding': '5px', 'font-size': '14px'},
                    selected_style={'padding': '5px', 'font-size': '14px', 'background-color': '#2c3e50',
                                    'color': 'white'}  # Active tab style
                ),
                dcc.Tab(
                    label='Map',
                    value='map',
                    style={'padding': '5px', 'font-size': '14px'},
                    selected_style={'padding': '5px', 'font-size': '14px', 'background-color': '#2c3e50',
                                    'color': 'white'}  # Active tab style
                ),
                dcc.Tab(
                    label='Table',
                    value='table',
                    style={'padding': '5px', 'font-size': '14px'},
                    selected_style={'padding': '5px', 'font-size': '14px', 'background-color': '#2c3e50',
                                    'color': 'white'}  # Active tab style
                )
            ], style={'height': '30px', 'margin-bottom': '10px'}),

            # Visualization Display
            html.Div(id='visualization-display', style={
                'height': '500px',  # Fixed height
                'overflow': 'auto',  # Enable both vertical and horizontal scrolling
                'border': '1px solid #ddd',  # Add a border
                'padding': '10px',  # Add padding
                'border-radius': '8px',  # Rounded edges
                'background-color': '#f0f4f8',  # Light blue background
                'width': '100%'  # Ensure it takes the full width of the right column
            })
        ], width='auto', style={
            'padding': '10px',
            'background-color': '#f0f4f8',
            'border-radius': '8px',
            'margin-left': '10px',  # Adjust margin to align with the left column
            'flex': '1'  # Allow the right column to stretch
        })
    ])
], style={
    'margin': '0',
    'padding': '20px',  # Added padding to the outer div
    'font-family': 'Arial, sans-serif',
    'background-color': '#ffffff'  # White background for the entire page
})


# Callback to reorder countries based on search input
@app.callback(
    Output('search-bar', 'options'),
    Input('search-bar', 'search_value')
)
def update_dropdown_options(search_value):
    """
    Reorder the dropdown so that matching countries appear at the top while maintaining the original order.
    """
    if not search_value:
        return [{'label': country, 'value': country} for country in countries]  # Default order

    search_value = search_value.lower()
    matching_countries = [c for c in countries if search_value in c.lower()]
    non_matching_countries = [c for c in countries if c not in matching_countries]

    reordered_countries = matching_countries + non_matching_countries
    return [{'label': country, 'value': country} for country in reordered_countries]


# Callback to update selected country checklist
@app.callback(
    Output('country-checklist', 'value'),
    Input('search-bar', 'value')
)
def update_checklist(selected_countries):
    """
    Update the checklist based on the selected countries from the dropdown.
    """
    if not selected_countries:
        return ['United States']  # Default selection
    return selected_countries


# Mapping of metrics to functions
metric_to_function = {
    'cfr': {
        'function': cases_death_analysis.plot_cfr,
        'requires_country': False  # Does not take 'country' parameter
    },
    'weekly_biweekly_growth': {
        'function': cases_death_analysis.plot_weekly_biweekly_growth,
        'requires_country': True  # Takes 'country' parameter
    },
    'cases_deaths_per_million': {
        'function': cases_death_analysis.plot_cases_deaths_per_million,
        'requires_country': False
    },
    'policy_impact': {
        'function': cases_death_analysis.plot_policy_impact,
        'requires_country': True
    },
    'reproduction_rate_trends': {
        'function': cases_death_analysis.plot_reproduction_rate_trends,
        'requires_country': True
    },
    'testing_vs_case_detection': {
        'function': cases_death_analysis.plot_testing_vs_case_detection,
        'requires_country': True
    },
    'case_trends': {
        'function': cases_death_analysis.plot_case_trends,
        'requires_country': True
    },
    'death_trends': {
        'function': cases_death_analysis.plot_death_trends,
        'requires_country': True
    },
    'cfr_by_country': {
        'function': cases_death_analysis.plot_cfr_by_country,
        'requires_country': True
    },
    'vaccination_rates_over_time': {
        'function': vaccination_analysis.plot_vaccination_rates_over_time,
        'requires_country': True
    },
    'vaccination_attitudes': {
        'function': vaccination_analysis.plot_vaccination_attitudes,
        'requires_country': True
    },
    'vaccination_by_age_group': {
        'function': vaccination_analysis.plot_vaccination_by_age_group,
        'requires_country': True
    },
    'vaccination_by_manufacturer': {
        'function': vaccination_analysis.plot_vaccination_by_manufacturer,
        'requires_country': True
    },
    'vaccination_vs_cfr': {
        'function': vaccination_analysis.plot_vaccination_vs_cfr,
        'requires_country': True
    },
    'vaccination_vs_reproduction_rate': {
        'function': vaccination_analysis.plot_vaccination_vs_reproduction_rate,
        'requires_country': True
    },
    'vaccination_vs_excess_mortality': {
        'function': vaccination_analysis.plot_vaccination_vs_excess_mortality,
        'requires_country': True
    },
    'us_vaccination_trends': {
        'function': vaccination_analysis.plot_us_vaccination_trends,
        'requires_country': False
    },
    'policy_stringency_over_time': {
        'function': policy_analysis.plot_policy_stringency_over_time,
        'requires_country': True
    },
    'policy_impact_on_cases_deaths': {
        'function': policy_analysis.plot_policy_impact_on_cases_deaths,
        'requires_country': True
    },
    'policy_impact_on_mobility': {
        'function': policy_analysis.plot_policy_impact_on_mobility,
        'requires_country': True
    },
    'policy_impact_on_vaccination': {
        'function': policy_analysis.plot_policy_impact_on_vaccination,
        'requires_country': True
    },
    'policy_impact_on_excess_mortality': {
        'function': policy_analysis.plot_policy_impact_on_excess_mortality,
        'requires_country': True
    },
    'policy_effectiveness_by_country': {
        'function': policy_analysis.plot_policy_effectiveness_by_country,
        'requires_country': False
    },
    'testing_rates_over_time': {
        'function': testing_healthcare_analysis.plot_testing_rates_over_time,
        'requires_country': True
    },
    'healthcare_capacity_over_time': {
        'function': testing_healthcare_analysis.plot_healthcare_capacity_over_time,
        'requires_country': True
    },
    'healthcare_capacity_vs_cfr': {
        'function': testing_healthcare_analysis.plot_healthcare_capacity_vs_cfr,
        'requires_country': True
    },
    'healthcare_capacity_vs_excess_mortality': {
        'function': testing_healthcare_analysis.plot_healthcare_capacity_vs_excess_mortality,
        'requires_country': True
    },
    'testing_healthcare_by_country': {
        'function': testing_healthcare_analysis.plot_testing_healthcare_by_country,
        'requires_country': False
    },
    'excess_mortality_over_time': {
        'function': excess_mortality_analysis.plot_excess_mortality_over_time,
        'requires_country': True
    },
    'age_specific_excess_mortality': {
        'function': excess_mortality_analysis.plot_age_specific_excess_mortality,
        'requires_country': True
    },
    'cumulative_excess_mortality': {
        'function': excess_mortality_analysis.plot_cumulative_excess_mortality,
        'requires_country': True
    },
    'excess_mortality_by_country': {
        'function': excess_mortality_analysis.plot_excess_mortality_by_country,
        'requires_country': False
    },
    'excess_mortality_vs_vaccination': {
        'function': excess_mortality_analysis.plot_excess_mortality_vs_vaccination,
        'requires_country': True
    },
    'excess_mortality_vs_policies': {
        'function': excess_mortality_analysis.plot_excess_mortality_vs_policies,
        'requires_country': True
    },
    'excess_mortality_vs_healthcare': {
        'function': excess_mortality_analysis.plot_excess_mortality_vs_healthcare,
        'requires_country': True
    },
    'mobility_trends_over_time': {
        'function': mobility_analysis.plot_mobility_trends_over_time,
        'requires_country': True
    },
    'mobility_trends_by_country': {
        'function': mobility_analysis.plot_mobility_trends_by_country,
        'requires_country': False
    },
    'mobility_vs_case_growth': {
        'function': mobility_analysis.plot_mobility_vs_case_growth,
        'requires_country': True
    },
    'mobility_vs_policies': {
        'function': mobility_analysis.plot_mobility_vs_policies,
        'requires_country': True
    },
    'mobility_vs_vaccination': {
        'function': mobility_analysis.plot_mobility_vs_vaccination,
        'requires_country': True
    },
    'mobility_vs_excess_mortality': {
        'function': mobility_analysis.plot_mobility_vs_excess_mortality,
        'requires_country': True
    }
}


# Callback to update visualizations
@app.callback(
    Output('visualization-display', 'children'),
    [Input('metric-dropdown', 'value'),
     Input('country-checklist', 'value'),
     Input('visualization-tabs', 'value')]
)
def update_visualization(selected_metric, selected_countries, visualization_type):
    if not selected_metric or not selected_countries:
        return "Please select a metric and at least one country."

    # Get the function and its requirements from the dictionary
    metric_info = metric_to_function.get(selected_metric)
    if not metric_info:
        return "Invalid metric selected."

    analysis_function = metric_info['function']
    requires_country = metric_info['requires_country']

    # Generate visualizations
    visualizations = []
    for country in selected_countries:
        try:
            if requires_country:
                # Call the function with 'country' parameter
                visualization = analysis_function(country=country, visualization_type=visualization_type)
            else:
                # Call the function without 'country' parameter
                visualization = analysis_function(visualization_type=visualization_type)

            # Add the visualization to the list
            visualizations.append(visualization)
        except Exception as e:
            # Log the error and continue
            print(f"Error generating visualization for {country}: {e}")
            continue

    # Determine the width of each visualization based on the number of visualizations
    if len(visualizations) == 1:
        # Single visualization takes full width
        rows = [dbc.Row(dbc.Col(visualizations[0], width=12))]
    else:
        # Multiple visualizations: 2 per row
        rows = []
        for i in range(0, len(visualizations), 2):
            # Create a row with up to 2 visualizations
            row_visualizations = visualizations[i:i + 2]
            cols = [dbc.Col(viz, width=6) for viz in
                    row_visualizations]  # Each visualization takes 6 columns (50% width)
            rows.append(dbc.Row(cols))

    return rows


# Run the app
if __name__ == "__main__":
    app.run(debug=True)

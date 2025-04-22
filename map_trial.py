import plotly.express as px
import geopandas as gpd
import pandas as pd
from dash import Dash, dcc, html, Output, Input, callback

cities = pd.read_csv('languageCities.csv', encoding = 'utf-8')

cities_geo = gpd.GeoDataFrame(cities, geometry = gpd.points_from_xy(cities['latitude'], cities['longitude']))

latin_to_rom = pd.read_csv('all_consonants_data.csv')


app = Dash()

app.layout = html.Div(children=[
    html.H1(children='QDFH'),

    html.Div(children='''
        A visual presentation of Latin consonants across the Romance languages
    '''),

    html.Div(children = [
        html.Label('Treatment'),
        dcc.Dropdown(latin_to_rom['treatment'].unique().tolist(),
                     value = '-R-',
                     id = 'select_treatment')
        ]),

    html.Div(children = [
        html.Label('Environment'),
        dcc.Dropdown(value = 'V_V', 
                     id = 'select_environment')
    ]),

    html.Div(children = [
             html.Label('Version'),
             dcc.Dropdown(value = 1,
                          id = 'select_version')
    ]),    

    dcc.Graph(
        id='map'
    )
])

@callback(
    Output('select_environment', 'options'),
    Input('select_treatment', 'value')
)
def update_environments(treatment):
    environ_list = latin_to_rom[latin_to_rom['treatment'] == treatment]['environment'].unique().tolist()
    return environ_list

@callback(
    Output('select_version', 'options'),
    Input('select_treatment', 'value'),
    Input('select_environment', 'value')
)
def update_versions(treatment, environment):
    versions_list = latin_to_rom[(latin_to_rom['treatment'] == treatment) & (latin_to_rom['environment'] == environment)]['version'].unique().tolist()
    return versions_list


@callback(
    Output('map', 'figure'),
    Input('select_treatment', 'value'),
    Input('select_environment', 'value'),
    Input('select_version', 'value'))
def update_map(selected_treatment, selected_environment, selected_version):
    latin_to_rom_sub = latin_to_rom[(latin_to_rom['treatment'] == selected_treatment) &
                                     (latin_to_rom['environment'] == selected_environment)]
    
    grouped = latin_to_rom_sub.groupby('Languages')

    version_tables = []
    for language, df in grouped:
        if selected_version in df['version'].unique().tolist():
            select_version = selected_version
        else:
            select_version = 1
        
        lang_table = df[df['version'] == select_version]
        version_tables.append(lang_table)

    if version_tables:
        version_sub = pd.concat(version_tables, axis=0)
    else:
        version_sub = pd.DataFrame(columns=latin_to_rom.columns)

    city_context = pd.merge(cities_geo, version_sub, left_on = 'Language', right_on = 'Languages').dropna(subset = 'IPA')
    

    fig = px.scatter_geo(city_context,
                    lat=city_context.geometry.x,
                    lon=city_context.geometry.y, 
                    hover_name = 'Language Variety', 
                    text = 'IPA')

    fig.update_layout(geo = dict(projection_scale = 8,
                                 center = dict(lat = 45.76, lon = 4.84)))
    fig.update_traces(textfont = dict(family = 'Arial',
                                    size = 16,
                                    color = 'black'),
                        marker = dict(size = 30,
                                      opacity = 0.5))
    fig.update_geos(showcountries = True)
    return fig


if __name__ == '__main__':
    app.run(debug=True)

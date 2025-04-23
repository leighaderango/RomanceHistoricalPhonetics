import plotly.express as px
import geopandas as gpd
import pandas as pd
from dash import Dash, dcc, html, Output, Input, callback

cities = pd.read_csv('languageCities.csv', encoding = 'utf-8')

cities_geo = gpd.GeoDataFrame(cities, geometry = gpd.points_from_xy(cities['latitude'], cities['longitude']))

display_data = pd.read_csv('display_data.csv')
#latin_to_rom = pd.read_csv('all_consonants_data.csv')


display_data['sonority_scaled'] = (display_data['sonority_avg'] - display_data['sonority_avg'].min()) / (display_data['sonority_avg'].max() - display_data['sonority_avg'].min())
display_data['place_scaled'] = (display_data['place_avg'] - display_data['place_avg'].min()) / (display_data['place_avg'].max() - display_data['place_avg'].min())


def blend_colors(r, b):
    return f'rgb({int(r * 255)}, 0, {int(b * 255)})'

display_data['color'] = [blend_colors(r, b) for r, b in zip(display_data['sonority_scaled'], display_data['place_scaled'])]

app = Dash()

app.layout = html.Div(children=[
    html.H1(children='QDFH'),

    html.Div(children='''
        A visual presentation of Latin consonants across the Romance languages
    '''),

    html.Div(children = [
        html.Label('Treatment'),
        dcc.Dropdown(display_data['treatment'].unique().tolist(),
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
    environ_list = display_data[display_data['treatment'] == treatment]['environment'].unique().tolist()
    return environ_list

@callback(
    Output('select_version', 'options'),
    Input('select_treatment', 'value'),
    Input('select_environment', 'value')
)
def update_versions(treatment, environment):
    versions_list = display_data[(display_data['treatment'] == treatment) & (display_data['environment'] == environment)]['version'].unique().tolist()
    return versions_list


@callback(
    Output('map', 'figure'),
    Input('select_treatment', 'value'),
    Input('select_environment', 'value'),
    Input('select_version', 'value'))
def update_map(selected_treatment, selected_environment, selected_version):
    latin_to_rom_sub = display_data[(display_data['treatment'] == selected_treatment) &
                                     (display_data['environment'] == selected_environment)]
    
    grouped = latin_to_rom_sub.groupby('language')

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
        version_sub = pd.DataFrame(columns=display_data.columns)

    city_context = pd.merge(cities_geo, version_sub, left_on = 'Language', right_on = 'language').dropna(subset = 'display')
    


    fig = px.scatter_geo(city_context,
                    lat=city_context.geometry.x,
                    lon=city_context.geometry.y, 
                    text = 'display',
                    color = city_context['color'],
                    color_discrete_map = 'identity')

    fig.update_layout(geo = dict(projection_scale = 8,
                                 center = dict(lat = 45.76, lon = 4.84)))
    fig.update_traces(textfont = dict(family = 'Arial',
                                    size = 16,
                                    color = 'black'),
                        marker = dict(size = 30,
                                      opacity = 0.5),
                        hovertemplate='<b>%{hovertext}</b><extra></extra>',
                        hovertext=city_context['Language Variety'])
    fig.update_geos(showcountries = True)
    return fig


if __name__ == '__main__':
    app.run(debug=True)

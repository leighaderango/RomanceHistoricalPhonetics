import plotly.express as px
import geopandas as gpd
import pandas as pd
from dash import Dash, dcc, html

cities = pd.read_csv('languageCities.csv', encoding = 'utf-8')

cities_geo = gpd.GeoDataFrame(cities, geometry = gpd.points_from_xy(cities['latitude'], cities['longitude']))

latin_to_rom = pd.read_csv('single_consonants_data.csv')
latin_to_rom_sub = latin_to_rom[(latin_to_rom['treatment'] == 'C-') & (latin_to_rom['environment'] == '#_a')]


city_context = pd.merge(cities_geo, latin_to_rom_sub, left_on = 'Language', right_on = 'Languages')


app = Dash()


fig = px.scatter_geo(city_context,
                    lat=city_context.geometry.x,
                    lon=city_context.geometry.y, 
                    hover_name = 'Language Variety', 
                    center = dict(lat = 45.76, lon = 4.84), 
                    text = 'IPA')
fig.update_layout(geo = dict(projection_scale = 8))
fig.update_traces(textfont = dict(family = 'Arial',
                                  size = 16,
                                  color = 'black'))



app.layout = html.Div(children=[
    html.H1(children='QDFH'),

    html.Div(children='''
        A visual presentation of Latin consonants across the Romance languages
    '''),

    html.Div(children = [
        html.Label('Treatment'),
        dcc.Dropdown(latin_to_rom['treatment'].unique().tolist())
        ]),

    dcc.Graph(
        id='map',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from dash import Input, Output, State, Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd
import plotly.express as px



# map_osm = folium.Map(location=[35.166804, 129.083479], zoom_start=12)

server = Flask(__name__)
app = Dash(__name__,
            prevent_initial_callbacks=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server
           )

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig_1 = px.pie(df, values='Amount', names='Fruit')

fig.update_layout({
    'paper_bgcolor': '#E9EEF6',
})
fig_1.update_layout({
    'paper_bgcolor': '#E9EEF6',
})

navbar = dbc.NavbarSimple(
    brand="GVCS",
    brand_style={"color": "black"},
    brand_href="#",
    color="beige",
    dark=True,
)

chart = html.Div(
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='1',
                        figure=fig_1,
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='2',
                        figure=fig_1,
                        style={'background-color': '#E9EEF6'}
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12)
            ]),
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='3',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='4',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12)
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='5',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='6',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12)
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='7',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='8',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12)
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='9',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='10',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12)
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='11',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='12',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12)
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
    ], id='row'),
)

# map=

app.layout = dbc.Container(className='main', children=[
    dbc.Row([
        dbc.Col(navbar),
    ]),
    dbc.Row([
        dbc.Col(chart),
    ]),
    dbc.Row([
        dbc.Col(dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")],
           id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),),
    ])

])


@app.callback(
    Output("layer", "children"), [Input("map", "click_lat_lng")],)
def map_click(click_lat_lng):
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]


# @app.callback(
#     Output("navbar-collapse", "is_open"),
#     # [Input("navbar-toggler", "n_clicks")],
#     [State("navbar-collapse", "is_open")],
# )
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


if __name__ == '__main__':
    app.run_server(debug=True)

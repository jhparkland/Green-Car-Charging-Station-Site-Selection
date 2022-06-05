from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_leaflet as dl

server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
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

app.layout = html.Div(className='main', children=[
    html.H1(children='Dash에서 h1부분'),

    html.Div(children='''
        걍 잡것 씨부리기.
    '''),

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
                        figure=fig_1
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
    ], className="chart"),
    html.Br(),
    html.Div(children=[
        dl.Map(dl.TileLayer(), className='map')
    ], className='map'),
    html.Br()
])

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8050, debug=True)
    app.run_server(debug=True)
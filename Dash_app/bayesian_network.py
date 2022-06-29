from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
df_economy = pd.DataFrame({
    "경제적": ["True", "False"],
    "적합확률": [80, 20],
    "경제적 요소": ["True", "False"]
})
df_society = pd.DataFrame({
    "사회적": ["True", "False"],
    "적합확률": [70, 30],
    "사회적 요소": ["True", "False"]
})
df_environment = pd.DataFrame({
    "환경적": ["True", "False"],
    "적합확률": [80, 20],
    "환경적 요소": ["True", "False"]
})
df_technique = pd.DataFrame({
    "기술적": ["True", "False"],
    "적합확률": [75, 35],
    "기술적 요소": ["True", "False"]
})





fig1 = px.bar(df_economy, x="경제적", y="적합확률", color="경제적 요소")
fig2 = px.bar(df_society, x="사회적",y="적합확률", color="사회적 요소")
fig3 = px.bar(df_environment, x="환경적", y="적합확률", color="환경적 요소")
fig4 = px.bar(df_technique, x="기술적", y="적합확률", color="기술적 요소")



fig1.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15, legend_title_text="",)
fig2.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15,legend_title_text="")
fig3.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15,legend_title_text="")
fig4.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15,legend_title_text="")





environment_chart = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='1',
                figure=fig3,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='2',
                figure=fig2,
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='3',
                figure=fig4,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='4',
                figure=fig1,
            )
        ]),
    ])

])
economy_chart = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='5',
                figure=fig2,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='6',
                figure=fig1,
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='7',
                figure=fig4,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='8',
                figure=fig3,
            )
        ]),
    ])

])
technique_chart = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='9',
                figure=fig2,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='10',
                figure=fig1,
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='11',
                figure=fig4,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='12',
                figure=fig3,
            )
        ]),
    ])

])
society_chart = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='13',
                figure=fig3,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='14',
                figure=fig2,
            )
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='15',
                figure=fig4,
            )
        ]),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='16',
                figure=fig1,
            )
        ]),
    ])

])


app.layout = html.Div(className='main', children=[
    dbc.Row([
        dbc.Col([
            environment_chart
        ]),
        dbc.Col([
            economy_chart
        ])
    ]),
    dbc.Row([
        dcc.Graph(
            className="standard_1",
            figure=fig2,
        )
    ]),
    dbc.Row([
        dbc.Col([
            society_chart
        ]),
        dbc.Col([
            technique_chart
        ])
    ])
])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
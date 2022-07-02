from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Module import Environment as en

server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )

df = pd.DataFrame({
    "경제적": ["True", "False"],
    "확률": [80, 20],
    "요소": ["True", "False"]
})

standard_df = pd.DataFrame({
    "기준": ["환경적", "경제적", "기술적", "사회적"],
    "Amount": [4, 1, 2, 3]
})


fig = px.bar(df, x="경제적", y="확률", color="요소")
fig_1 = px.pie(standard_df, values='Amount', names='기준')

ozone = en.Ozone()
df_ozone = pd.read_csv(ozone.file_path, encoding='cp949')
df_ozone = ozone.pretreatment(df_ozone)
df_ozone = ozone.advanced_replace(df_ozone, df_ozone.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
df_ozone = ozone.ChangeType(df_ozone, '2021.07')
ozone_describe = ozone.describe(df_ozone)
busan_ozone = df_ozone[df_ozone['구분(2)'] == '부산광역시'].loc[2, '2021.07']

fig_ozone = ozone.cal_norm(df_ozone.iloc[:, 2].mean(),
                            df_ozone.iloc[:, 2].std(),
                            df_ozone.iloc[:, 2].min(),
                            df_ozone.iloc[:, 2].max(),
                            busan_ozone
                            )
#========================================================================================================
so2 = en.So2()
df_so2 = pd.read_csv(so2.file_path, encoding='cp949')
df_so2 = so2.pretreatment(df_so2)
df_so2 = so2.advanced_replace(df_so2, df_so2.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
df_so2 = so2.ChangeType(df_so2, '2021.07')
so2_describe = so2.describe(df_so2)
busan_so2 = df_so2[df_so2['구분(2)'] == '부산광역시'].loc[2, '2021.07']
fig_so2 = so2.cal_norm(df_so2.iloc[:, 2].mean(),
                            df_so2.iloc[:, 2].std(),
                            df_so2.iloc[:, 2].min(),
                            df_so2.iloc[:, 2].max(),
                            busan_so2
                            )

fig.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15)

fig_1.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.61, legend_x=0.25, legend_orientation="h")

fig_ozone.update_layout({
   'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15)

fig_so2.update_layout({
   'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15)

app.layout = html.Div(className='main', children=[
    html.H1(children='CHARLO-WA'),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="standard",
                        id='1',
                        figure=fig_1,
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="standard",
                        id='2',
                        figure=fig_1
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'})
            ]),
        ], xs=12, sm=12, md=12, lg=2, xl=2),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='3',
                        figure=fig_ozone
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='4',
                        figure=fig_so2
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
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
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='6',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
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
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='8',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
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
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='10',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
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
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='12',
                        figure=fig
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2),
    ], className="chart"),
    html.Br(),
    # html.Div(children=[
    #     dl.Map(dl.TileLayer(), className='map')
    # ], className='map'),

    html.Iframe(
        src="assets/route_graph.html",
        style={"height": "500px", "width": "95%"},
    ),
    html.P(),
])

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8050, debug=True)
    app.run_server(debug=False)
from flask import Flask
from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import os, sys
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
df_ozone = ozone.ChangeType(df_ozone, '2021.07',  'float')
ozone_describe = ozone.describe(df_ozone)
busan_ozone = df_ozone[df_ozone['구분(2)'] == '부산광역시'].loc[2, '2021.07']

fig_ozone = ozone.cal_norm(df_ozone.iloc[:, 2].mean(),
                            df_ozone.iloc[:, 2].std(),
                            df_ozone.iloc[:, 2].min(),
                            df_ozone.iloc[:, 2].max(),
                            busan_ozone
                            )
fig_ozone.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin=dict(l=10, r=10, t=10, b=10), legend_title_text="오존",)

#========================================================================================================
so2 = en.So2()
df_so2 = pd.read_csv(so2.file_path, encoding='cp949')
df_so2 = so2.pretreatment(df_so2)
df_so2 = so2.advanced_replace(df_so2, df_so2.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
df_so2 = so2.ChangeType(df_so2, '2021.07', 'float')
so2_describe = so2.describe(df_so2)
busan_so2 = df_so2[df_so2['구분(2)'] == '부산광역시'].loc[2, '2021.07']
fig_so2 = so2.cal_norm(df_so2.iloc[:, 2].mean(),
                            df_so2.iloc[:, 2].std(),
                            df_so2.iloc[:, 2].min(),
                            df_so2.iloc[:, 2].max(),
                            busan_so2
                            )
fig_so2.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin=dict(l=10, r=10, t=10, b=10), legend_title_text="SO2",)
#========================================================================================================

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

elec_standard_df = pd.DataFrame({ #전기차
    "기준": ["환경적", "경제적", "기술적", "사회적"],
    "Amount": [4, 1, 2, 3]
})
hydro_standard_df = pd.DataFrame({ #수소차
    "기준": ["환경적", "경제적", "기술적", "사회적"],
    "Amount": [5, 1, 1, 2]
})

fig1 = px.bar(df_economy, x="경제적", y="적합확률", color="경제적 요소")
fig2 = px.bar(df_society, x="사회적",y="적합확률", color="사회적 요소")
fig3 = px.bar(df_environment, x="환경적", y="적합확률", color="환경적 요소")
fig4 = px.bar(df_technique, x="기술적", y="적합확률", color="기술적 요소")

fig_1 = px.pie(elec_standard_df, values='Amount', names='기준')
fig_2 = px.pie(hydro_standard_df, values='Amount', names='기준')

fig1.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15, legend={'title_text': ''})
fig2.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15, legend={'title_text': ''})
fig3.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15, legend={'title_text': ''})
fig4.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15, legend={'title_text': ''})

fig_1.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, title_text='전기차', title_y=0.7,
    margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.61, legend_x=0.25, legend_orientation="h")
fig_2.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, title_text='수소차', title_y=0.7,
    margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.61, legend_x=0.25, legend_orientation="h")


navbar = dbc.Navbar(
    dbc.Row(
        [
            dbc.Col(
                html.A(
                    html.Img(src="assets/logo.png", height="60px"),
                    href="http://127.0.0.1:8050/",
                    className="logoImg"
                ),
            ),
            dbc.Col(
                html.A(
                    dbc.Button("전체 확률 네트워크 보기 ->", outline=True,
                               color="secondary", className="button"),
                    href="http://127.0.0.1:9999/"
                )
            )
        ]
    )
)

chart = html.Div(
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
                        figure=fig_2
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'})
            ]),
        ], xs=12, sm=12, md=12, lg=4, xl=2.4, className="pie_chart"),
        html.Div(
            className="line",
        ),
        html.Div(
            className="mobile_line1",
        ),
        #상위요소
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='3',
                        figure=fig1
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),

                html.Div(
                    className="desktop_line1",
                ),

                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='4',
                        figure=fig2
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2.4),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='5',
                        figure=fig3
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='6',
                        figure=fig4
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2.4, className="chart_bar_1"),

        html.Div(
            className="desktop_line2",
        ),
        html.Div(
            className="mobile_line2",
        ),

        #하위요소소
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='7',
                        figure=fig_ozone
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='8',
                        figure=fig_so2
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2.4),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='9',
                        figure=fig_ozone
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='10',
                        figure=fig1
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2.4),
    ], className="chart")
)

app.layout = html.Div(className='main', children=[
    navbar,
    chart,
    html.Br(),

    html.Iframe(
        src="assets/route_graph.html",
        style={"height": "500px", "width": "95%"},
        className="map_"
    ),
    html.P(),
])

# @app.callback(
#     Output(component_id='body-div', component_property='children'),
#     Input(component_id='button', component_property='n_clicks')
# )
# def goto_baysian(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         return href=""

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8050, debug=True)
    app.run_server(debug=False)
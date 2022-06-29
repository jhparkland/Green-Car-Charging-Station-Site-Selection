from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import ang

server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
ozone_file_path = "assets/오존_월별_도시별_대기오염도.csv"
df_ozone = pd.read_csv(ozone_file_path, encoding='cp949')
ozen_col = df_ozone.iloc[:, 2:-1].columns.tolist()
df_ozone.drop(columns=ozen_col, inplace=True)

# 해당 컬럼 float 타입으로 변경
ang.advanced_replace(df_ozone, df_ozone.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
df_ozone['2021.07'] = df_ozone['2021.07'].astype(float)

ang.show_norm(df_ozone.iloc[:, 2].mean(), df_ozone.iloc[:, 2].std(), df_ozone.iloc[:, 2].min(), df_ozone.iloc[:, 2].max())
### 부산광역시 오존의 누적확률 구하기

busan_oz = df_ozone[df_ozone['구분(2)']=='부산광역시'].loc[2,'2021.07']
fig_ozone = ang.cal_norm(df_ozone.iloc[:, 2].mean(), df_ozone.iloc[:, 2].std(), df_ozone.iloc[:, 2].min(), df_ozone.iloc[:, 2].max(), busan_oz)

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
elec_standard_df = pd.DataFrame({
    "기준": ["환경적", "경제적", "기술적", "사회적"],
    "Amount": [4, 1, 2, 3]
})
hydro_standard_df = pd.DataFrame({
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
}, title_text='수소차', title_y=0.7,
    margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.61, legend_x=0.25, legend_orientation="h")
fig_2.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, title_text='수소차', title_y=0.7,
    margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.61, legend_x=0.25, legend_orientation="h")
fig_ozone.update_layout({
    'paper_bgcolor': '#E9EEF6',
}, margin_l=10, margin_r=10, legend_y=1.5, legend_x=0.15)

navbar = dbc.Navbar(
    dbc.Row(
        [
            dbc.Col(
                html.A(
                    html.Img(src="assets/logo.png", height="60px"),
                    href="",
                    className="logoImg"
                ),
            ),
            dbc.Col(
                dbc.Button("전체 확률 네트워크 보기 ->", outline=True, color="secondary", className="me-1",)
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
                        figure=fig_ozone
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

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8050, debug=True)
    app.run_server(debug=True)
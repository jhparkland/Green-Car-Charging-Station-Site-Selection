from flask import Flask
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
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
                html.H3("Baysian Network"),
                className="bay"
            )
        ]
    )
)


environment_chart = html.Div([
    # 환경적 하위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='1',
                figure=fig_ozone,
            )
        ], xs=3, sm=3, md=3, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='2',
                figure=fig_so2,
            )
        ], xs=3, sm=3, md=3, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    dbc.Row(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='3',
                figure=fig4,
            )
        ], xs=3, sm=3, md=3, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='4',
                figure=fig1,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    #환경적 상위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                figure=fig3,
            )
        ], xs=6, sm=6, md=12, lg=12, xl=12, style={'padding': '12px'})
    ])

])
economy_chart = html.Div([
    #경제적 하위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='5',
                figure=fig2,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='6',
                figure=fig1,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='7',
                figure=fig4,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='8',
                figure=fig3,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    dbc.Row([ #경제적 상위요소
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                figure=fig1,
            )
        ], xs=6, sm=6, md=12, lg=12, xl=12, style={'padding': '12px'})
    ])
])
technique_chart = html.Div([
    
    # 기술적 상위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                figure=fig4,
            )
        ], xs=6, sm=6, md=12, lg=12, xl=12, style={'padding': '12px'})
    ]),

    #기술적 하위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='9',
                figure=fig2,
            )
        ],xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='10',
                figure=fig1,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='11',
                figure=fig4,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='12',
                figure=fig3,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ])

])
society_chart = html.Div([
    
    # 사회적 상위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                figure=fig2,
            )
        ], xs=6, sm=6, md=12, lg=12, xl=12, style={'padding': '12px'})

    ]),
    
    #사회적 하위요소
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='13',
                figure=fig3,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='14',
                figure=fig2,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='15',
                figure=fig4,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
        dbc.Col([
            dcc.Graph(
                className="standard_1",
                id='16',
                figure=fig1,
            )
        ], xs=3, sm=3, md=6, lg=6, xl=6, style={'padding': '12px'}),
    ])

])


app.layout = html.Div(className='main', children=[
    navbar,
    dbc.Row([
        dbc.Col([
            html.H1("환경적"),
            environment_chart
        ], className="B_chart"),
        dbc.Col([
            html.H1("경제적"),
            economy_chart
        ], className="B_chart")
    ]),

    #최종확률
   dbc.Row([
       dbc.Col([
           html.H1("최종확률"),
           dcc.Graph(
                className="standard_1",
                figure=fig2,
           )
       ], style={'padding': '12px'})

    ], className="B_chart"),

    dbc.Row([
        dbc.Col([
            html.H1("사회적"),
            society_chart
        ], className="B_chart"),
        dbc.Col([
            html.H1("기술적"),
            technique_chart
        ], className="B_chart")
    ])
])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)
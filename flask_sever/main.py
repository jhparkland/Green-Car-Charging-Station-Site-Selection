from flask import Flask
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import matplotlib.font_manager as font_manager
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Module import Environment as en

#서버연결
server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
app.title = "애코 차징 플레이스"
app._favicon ="logo_icon.ico"

font_dir = ['/assets/NanumSquare']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

#========================================================================================================

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
fig_ozone.update_layout({   #환경적 하위요소-대기질(OZONE)
    'paper_bgcolor': '#E9EEF6',
}, margin=dict(l=10, r=10, t=10, b=10), legend_title_text="오존", font_family='NanumSquare')

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
fig_so2.update_layout({     #환경적 하위요소-대기질(SO2)
    'paper_bgcolor': '#E9EEF6',
}, margin=dict(l=10, r=10, t=10, b=10), legend_title_text="SO2", font_family='NanumSquare')
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

fig_1 = px.pie(elec_standard_df, values='Amount', names='기준') #전기차
fig_2 = px.pie(hydro_standard_df, values='Amount', names='기준') #수소차

#막대차트 배경색 설정 및 레이아웃 설정 변경
fig1.update_layout({'paper_bgcolor': '#E9EEF6'}, font_family='NanumSquare') #경제적
fig2.update_layout({'paper_bgcolor': '#E9EEF6'}, font_family='NanumSquare') #사회적
fig3.update_layout({'paper_bgcolor': '#E9EEF6'}, font_family='NanumSquare') #환경적
fig4.update_layout({'paper_bgcolor': '#E9EEF6'}, font_family='NanumSquare') #기술적


fig_1.update_layout({   #전기차 충전소 파이차트
    'paper_bgcolor': '#E9EEF6', #파이차트 배경색
}, title_text='전기차 충전소', title_y=0.8, title_font_size=22, #제목설정
    margin=dict(l=0, r=0, t=40, b=20),  #좌우위아래 여유공간
    legend_y=1.3, legend_x=0.25, legend_orientation="h", legend_font_size=9.8, font_family='NanumSquare') #범례 설정

fig_2.update_layout({   #수소차 충전소 파이차트
    'paper_bgcolor': '#E9EEF6', #파이차트 배경색
}, title_text='수소차 충전소', title_y=0.8, title_font_size=22, #제목설정
    margin=dict(l=0, r=0, t=40, b=20),  #좌우위아래 여유공간
    legend_y=1.3, legend_x=0.25, legend_orientation="h", legend_font_size=9.8, font_family='NanumSquare') #범례 설정

#상단 메뉴바(header-로고,베이지안 네트워크버튼)
header = dbc.Navbar(
    #하나의 행 사용
    dbc.Row(
        [
            dbc.Col(
                html.A(     #왼편에 로고 표시하고 누르면 페이지 리셋(새로고침)
                    html.Img(src="assets/logo.png", height="60px"), #파일경로, 높이
                    href="",
                    target="_black",
                    className="logoImg"
                ),
            ),
            dbc.Col(    #베이지안 네트워크 페이지로 연결
                html.Form(
                    dbc.Button("전체 확률 네트워크 보기 ->", outline=True, color="secondary",
                               className="me-1", href="/bayesian", external_link=True, target="_blank"),
                ),
            )
        ]
    )
)

#차트
chart = html.Div(className='def_chart', children=[
    
    #desktop_제목
    dbc.Row([
        dbc.Col([
            html.H4("상위요인 중요도", className="d-none d-lg-block d-xl-none", id="c_name_1"),
            html.H4("상위요인 중요도", className="d-none d-xl-block", id="c_name_2")
        ]),
        dbc.Col([
            html.H4("상위요인 적합성", className="d-none d-lg-block d-xl-none", id="c_name_3"),
            html.H4("상위요인 적합성", className="d-none d-xl-block", id="c_name_4")
        ]),
        dbc.Col([
            html.H4("하위 변수 정규 분포", className="d-none d-lg-block d-xl-none", id="c_name_5"),
            html.H4("하위 변수 정규 분포", className="d-none d-xl-block", id="c_name_6")
        ]),
    ]),

    dbc.Row([
        #상위요인 중요도_name
        html.H4("상위요인 중요도", className="d-block d-sm-none", id="m_c_name_1"), #xs
        html.H4("상위요인 중요도", className="d-none d-sm-block d-md-none", id="m_c_name_1-2"),#sm
        html.H4("상위요인 중요도", className="d-none d-md-block d-lg-none", id="m_c_name_1-3"),#md
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(  #전기차_파이차트
                        className="standard",
                        id='1',
                        figure=fig_1,
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(  #수소차_파이차트
                        className="standard",
                        id='2',
                        figure=fig_2
                    ),
                ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'})
            ]),
        ], xs=12, sm=12, md=12, lg=4, xl=2.4, className="pie_chart"),

        #라인
        html.Div(   #전기차, 수소차 영역 구분 선(데스크톱:가로, 모바일:세로)
            className="line",
        ),
        html.Div(   #파이차트, 확률차트 영역 구분 -> 모바일에만 적용
            className="mobile_line1",
        ),
        #상위요인 적합성_name
        html.H4("상위요인 적합성", className="d-block d-sm-none", id="m_c_name_2"), #xs
        html.H4("상위요인 적합성", className="d-none d-sm-block d-md-none", id="m_c_name_2-2"),#sm
        html.H4("상위요인 적합성", className="d-none d-md-block d-lg-none", id="m_c_name_2-3"),#md
        #상위요소
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(  #경제적
                        className="image",
                        id='3',
                        figure=fig1
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),

                #라인-파이차트. 확률 구분 선 -> desktop만 적용
                html.Div(
                    className="desktop_line1",
                ),

                dbc.Col([
                    dcc.Graph(  #사회적
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
                    dcc.Graph(  #환경적
                        className="image",
                        id='5',
                        figure=fig3
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                dbc.Col([
                    dcc.Graph(  #기술적
                        className="image",
                        id='6',
                        figure=fig4
                    ),
                ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
            ])
        ], xs=12, sm=12, md=12, lg=2, xl=2.4, className="chart_bar_1"),

        #라인
        html.Div(
           className="desktop_line2",
        ),
        html.Div(
            className="mobile_line2",
        ),
        #하위변수 정규분포_name
        html.H4("하위 변수 정규 분포", className="d-block d-sm-none", id="m_c_name_3"), #xs
        html.H4("하위 변수 정규 분포", className="d-none d-sm-block d-md-none", id="m_c_name_3-2"),#sm
        html.H4("하위 변수 정규 분포", className="d-none d-md-block d-lg-none", id="m_c_name_3-3"),#md
        #하위요소
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        className="image",
                        id='7',
                        figure=fig_ozone    #대기질->오존
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
])

#메인화면
main_layout = [
    header,
    chart,
    html.Br(),
    html.Iframe(    #하단부(지도)
        src="assets/route_graph.html",
        style={"height": "500px", "width": "95%"},
        className="map_"
    ),
    html.P(),
]

#베이지안 네트워크 화면
bayesian_layout = html.Div("hello")

#최종 출력
app.layout = html.Div(className='main', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

#========================================================================================================

@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/bayesian':
        return bayesian_layout
    else:
        return main_layout



saveE = {}
saveH = {}
saveEcon = {}
saveSoci = {}
saveEnvi = {}
saveTech = {}


@app.callback(  #수소차 파이차트 클릭데이터 초기화
    Output("2", "clickData"),
    Input("1", "clickData")
)
def clear_hydro(elec):
    global saveE, saveH
    if elec is not None:
        saveE = elec
        return None
    else:
        return saveH

@app.callback(  #전기차 파이차트 클릭데이터 초기화
    Output("1", "clickData"),
    Input("2", "clickData")
)
def clear_elec(hydro):
    global saveE, saveH
    if hydro is not None:
        saveH = hydro
        return None
    else:
        return saveE

@app.callback(  #파이차트 -> 확률차트 이벤트 연결
    Output("3", "figure"),
    Output("4", "figure"),
    Output("5", "figure"),
    Output("6", "figure"),
    Input("1", "clickData"),
    Input("2", "clickData"),
)
def update(elec, hydro):
    if elec is not None:
        return fig1, fig2, fig3, fig4
    else:
        return fig1, fig2, fig3, fig4

@app.callback(  #사회적 확률 차트 클릭데이터 초기화
    Output("4", "clickData"),
    Input("3", "clickData"),
)
def clear_econ(econ):
    global saveEcon, saveSoci, saveEnvi, saveTech
    if econ is not None:
        saveEcon = econ
        saveSoci = None
        saveEnvi = None
        saveTech = None
        return None
    else:
        return saveSoci

@app.callback(  #환경적 확률 차트 클릭데이터 초기화
    Output("5", "clickData"),
    Input("4", "clickData"),
)
def clear_econ(soci):
    global saveEcon, saveSoci, saveEnvi, saveTech
    if soci is not None:
        saveEcon = None
        saveSoci = soci
        saveEnvi = None
        saveTech = None
        return None
    else:
        return saveEnvi

@app.callback(  #기술적 확률 차트 클릭데이터 초기화
    Output("6", "clickData"),
    Input("5", "clickData"),
)
def clear_econ(envi):
    global saveEcon, saveSoci, saveEnvi, saveTech
    if envi is not None:
        saveEcon = None
        saveSoci = None
        saveEnvi = envi
        saveTech = None
        return None
    else:
        return saveTech

@app.callback(  #경제적 확률 차트 클릭데이터 초기화
    Output("3", "clickData"),
    Input("6", "clickData"),
)
def clear_econ(tech):
    global saveEcon, saveSoci, saveEnvi, saveTech
    if tech is not None:
        saveEcon = None
        saveSoci = None
        saveEnvi = None
        saveTech = tech
        return None
    else:
        return saveEcon

@app.callback(  #확률차트 -> 정규분포 이벤트 설정
    Output("7", "figure"),
    Output("8", "figure"),
    Output("9", "figure"),
    Input("3", "clickData"),
    Input("4", "clickData"),
    Input("5", "clickData"),
    Input("6", "clickData")
)
def update(econ, soci, envi, tech):
    if econ is not None:
        return fig_ozone, fig_ozone, fig_ozone
    elif soci is not None:
        return fig_so2, fig_so2, fig_so2
    elif envi is not None:
        return fig_ozone, fig_ozone, fig_ozone
    else:
        return fig_so2, fig_so2, fig_so2


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)
    app.run_server(debug=False)
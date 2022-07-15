# 전기차 베이지안
from flask_sever.component import Bayesian
from Module import Environment
from Module import Social
from Module import Economical
from Module import Technical
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os, sys
import matplotlib.font_manager as font_manager
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


# 서버연결
# server = Flask(__name__)
app = Dash(__name__,
           title='에코 차징 플레이스',
           update_title='데이터를 불러오는 중 입니다.',
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
server = app.server

font_dir = ['/assets/NanumSquare']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# 데이터 불러오는 영역
# ========================================================================================================
'''
환경적-수소, 경제 동일함
'''
ozone = Environment.Ozone()  # 오존 데이터
so2 = Environment.So2()  # 아황산가스 데이터
no2 = Environment.No2()  # 이산화질소 데이터
co = Environment.Co()  # 일산화탄소 데이터
pm25 = Environment.FineDust_pm25()  # 미세먼지 pm2.5
pm10 = Environment.FineDust_pm10()  # 미세먼저 pm10
total_air_quality = Environment.Total_air_quality()  # 통합 대기환경

'''
사회적
E : 고정인구, 유동인구, 전기차 수(ecc.elec_fig/elec_ecc),전기차 충전소 수, 고속도로 여부,교차로 [6]
H : 고정인구, 유동인구, lpg 충전소 수, 수소차 수(ecc.hydro_fig/hydro_ecc), 수소차 충전소 수, 고속도로 여부, 교차로 [8]
'''
population = Social.Population()    #고정 인구
f_population = Social.FloatingPopulation()  #유동인구
ecc = Social.Eco_friendly_car_registration()    #전기차 수
lpg = Social.LPG_charging_station()   #lpg 충전소 수
evcs = Social.EVCS()    #전기차 충전소 수
hvcs = Social.HVCS()  #수소차 충전소 수
intersection = Social.Intersection()   #교차로
# highway = Social.Highway()  #고속도로 여부(정성적)

'''
경제적
E : 주차 구획수, 전기차 충전소 설치 비용
H : lpg 충전소 토지 비용, 수소차 충전소 설치 비용
'''
elec_charger_cost = Economical.electricity_charger_cost()  # 전기차 충전소 설치 비용
hydro_charger_cost = Economical.Hydrogen_charger_cost()  # 수소차 충전소 설치 비용
lpg_land_cost = Economical.Lpg_land_costs()     # LPG 토지 비용
parkinglot = Economical.Parkinglot()   # 주차 구획수
'''
기술적
E : 급속/완속 적합성
H : 복합 충전소 여부
'''
# ccs = Technical.Complex_charging_station() #복합 충전소 여부
# charging_time = Technical.Charging_time()  #급속/완속 적합성
'''
각 요소의 fig는 객체.fig 하면 됨
ex) ozone.fig => 오존 fig
'''
# ========================================================================================================

# 경제적 확률차트 데이터프레임
df_economy = pd.DataFrame({
    "경제적": ["적합", "부적합"],  # x축 라벨
    "적합확률": [80, 20],  # 확률
    "경제적 요소": ["적합 : 80", "부적합 : 20"]  # 색 구분 위해 넣음
})
# 사회적 확률차트 데이터프레임
df_society = pd.DataFrame({
    "사회적": ["적합", "부적합"],  # x축 라벨
    "적합확률": [70, 30],  # 확률
    "사회적 요소": ["적합 : 70", "부적합 : 30"]  # 색 구분 위해 넣음
})
# 환경적 확률차트 데이터프레임
df_environment = pd.DataFrame({
    "환경적": ["적합", "부적합"],  # x축 라벨
    "적합확률": [80, 20],  # 확률
    "환경적 요소": ["적합 : 80", "부적합 : 20"]  # 색 구분 위해 넣음
})
# 기술적 확률차트 데이터프레임
df_technique = pd.DataFrame({
    "기술적": ["적합", "부적합"],  # x축 라벨
    "적합확률": [75, 25],  # 확률
    "기술적 요소": ["적합 : 75", "부적합 : 25"]  # 색 구분 위해 넣음
})
# 수소차 - 경제적 확률차트 데이터프레임
df_hy_economy = pd.DataFrame({
    "경제적": ["적합", "부적합"],
    "적합확률": [47, 53],
    "경제적 요소": ["적합 : 47", "부적합 : 53"]
})
# 수소차 - 사회적 확률차트 데이터프레임
df_hy_society = pd.DataFrame({
    "사회적": ["적합", "부적합"],
    "적합확률": [84, 16],
    "사회적 요소": ["적합 : 84", "부적합 : 16"]
})
# 수소차 - 환경적 확률차트 데이터프레임
df_hy_environment = pd.DataFrame({
    "환경적": ["적합", "부적합"],
    "적합확률": [58, 42],
    "환경적 요소": ["적합 : 58", "부적합 : 42"]
})
# 수소차 - 기술적 확률차트 데이터프레임
df_hy_technique = pd.DataFrame({
    "기술적": ["적합", "부적합"],
    "적합확률": [74, 26],
    "기술적 요소": ["적합 : 74", "부적합 : 26"]
})
# =========================================================================================================
fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4 \
    = Bayesian.bay_bar_layout(**{
                                   "경제적": df_economy,
                                   "사회적": df_society,
                                   "환경적": df_environment,
                                   "기술적": df_technique,
                                   "수소_경제적": df_hy_economy,
                                   "수소_사회적": df_hy_society,
                                   "수소_환경적": df_hy_environment,
                                   "수소_기술적": df_hy_technique
                                   })
fig_list = {
            "fig1": fig1,
            "fig2": fig2,
            "fig3": fig3,
            "fig4": fig4,

            "hy_fig1": hy_fig1,
            "hy_fig2": hy_fig2,
            "hy_fig3": hy_fig3,
            "hy_fig4": hy_fig4,

            "ozone": ozone.fig,
            "so2": so2.fig,
            "no2": no2.fig,
            "co": co.fig,
            "pm25": pm25.fig,
            "pm10": pm10.fig,
            "total_air_quality": total_air_quality.fig,

            "population": population.fig,
            "f_population": f_population.fig,
            "elec_ecc": ecc.elec_fig,
            "hydro_ecc": ecc.hydro_fig,
            "lpg": lpg.fig,
            "evcs": evcs.fig,
            "hvcs": hvcs.fig,
            "intersection": intersection.fig,
            # "highway": highway.fig,

            # "elec_charger_cost": elec_charger_cost.fig,
            "hydro_charger_cost": hydro_charger_cost.fig,
            "lpg_land_cost": lpg_land_cost.fig,
            "parkinglot": parkinglot.fig,

            # "ccs": ccs.fig,
            # "charging_time": charging_time.fig,
            }
# 막대차트 및 파이차트 배경색 설정 및 레이아웃 설정 변경 및
Bayesian.bay_layout(**fig_list)  # 언팩 인자로 전달 필수!.
bayesian_elec_chart = Bayesian.bayesian_network_elec(**fig_list)
bayesian_hydro_chart = Bayesian.bayesian_network_hydro(**fig_list)
app.layout = html.Div(bayesian_elec_chart)
# fig1 = px.bar(df_economy, x="경제적", y="적합확률", color="경제적 요소", text="경제적 요소")
# fig1.update_yaxes(visible=False), fig1.update_xaxes(visible=False)
# fig2 = px.bar(df_society, x="사회적", y="적합확률", color="사회적 요소", text="사회적 요소")
# fig2.update_yaxes(visible=False), fig2.update_xaxes(visible=False, )
# fig3 = px.bar(df_environment, x="환경적", y="적합확률", color="환경적 요소", text="환경적 요소")
# fig3.update_yaxes(visible=False), fig3.update_xaxes(visible=False)
# fig4 = px.bar(df_technique, x="기술적", y="적합확률", color="기술적 요소", text="기술적 요소")
# fig4.update_yaxes(visible=False), fig4.update_xaxes(visible=False)
#
# fig1.update_layout({
#     'paper_bgcolor': '#E9EEF6',  # 배경색
#     }, title_text="경제적", title_font_size=22, margin_l=10, margin_r=10,
#     font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
# fig2.update_layout({
#     'paper_bgcolor': '#E9EEF6',  # 배경색
#     }, title_text="사회적", title_font_size=22, margin_l=10, margin_r=10,
#     font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
# fig3.update_layout({
#     'paper_bgcolor': '#E9EEF6',  # 배경색
#     }, title_text="환경적", title_font_size=22, margin_l=10, margin_r=10,
#     font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
# fig4.update_layout({
#     'paper_bgcolor': '#E9EEF6',  # 배경색
#     }, title_text="기술적", title_font_size=22, margin_l=10, margin_r=10,
#     font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
# # =========================================================================================================
#
# ##################환경적####################
# ozone.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="오존", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# so2.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="아황산가스", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# no2.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="이산화질소", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# co.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="일산화탄소", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# pm25.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="pm25", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# pm10.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="pm10", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
#
# ########################사회적####################
# population.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="고정인구", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# f_population.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="유동인구", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# elec_ecc.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="전기차 수", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# hydro_ecc.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="수소차 수", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# lpg.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="lpg 충전소 수", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# evcs.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="전기차 충전소 수", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# hvcs.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="수소차 충전소 수", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# intersection.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="교차로", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
#
# ###################경제적#################
# parkinglot.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="주차 구획수 ", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# hydro_charger_cost.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="수소차 충전소 설치 비용", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# lpg_land_cost.update_layout({
#     'paper_bgcolor': '#E9EEF6',
# }, title_text="lpg 토지 비용", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
#
# #################기술적#################
# # css.update_layout({
# #     'paper_bgcolor': '#E9EEF6',
# # }, title_text="복합 충전소 여부", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
# # charging_time.update_layout({
# #     'paper_bgcolor': '#E9EEF6',
# # }, title_text="급속/완속 적합성", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
#
# # =========================================================================================================


# app.layout = html.Div(className='bay', children=[
#     html.Img(src="assets/logo.png", id="logo"),
#     html.Div(id="env", children=[
#         html.H1("환경적"),
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=ozone,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=so2,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=no2,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=co,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=pm25
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=pm10,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=total_air_quality,
#                 )
#             ], xs=3, sm=3, md=3, lg=3, xl=3),
#         ], style={'margin-top': '2%'}),
#         dbc.Row([
#             dbc.Col([
#                 dcc.Graph(
#                     className="standard_1",
#                     figure=fig3,
#                 )
#             ], xs=12, sm=12, md=12, lg=12, xl=12, style={'margin-top': '2%'})
#         ]),
#         html.Div(id="soc", children=[
#             html.H1("사회적"),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig4,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig1,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig3,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig4,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#             ]),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig2,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig4,
#                     )
#                 ], xs=3, sm=3, md=3, lg=3, xl=3),
#             ], style={'margin-top': '2%'}),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig2,
#                     )
#                 ], xs=12, sm=12, md=12, lg=12, xl=12, style={'margin-top': '2%'})
#             ]),
#         ]),
#         html.Div(id="eco", children=[
#             html.H1("경제적"),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig1,
#                     )
#                 ], xs=12, sm=12, md=12, lg=12, xl=12)
#             ]),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig2,
#                     )
#                 ], xs=6, sm=6, md=6, lg=6, xl=6),
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig4,
#                     )
#                 ], xs=6, sm=6, md=6, lg=6, xl=6),
#             ], style={'margin-top': '2%'}),
#         ]),
#         html.Div(id="tec", children=[
#             html.H1("기술적"),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig4,
#                     )
#                 ]),
#             ]),
#             dbc.Row([
#                 dbc.Col([
#                     dcc.Graph(
#                         className="standard_1",
#                         figure=fig3,
#                     )
#                 ], style={'margin-top': '2%'})
#             ]),
#         ]),
#         html.Div(id="cen", children=[
#             html.H1("최종 확률"),
#             dbc.Row([
#                 dbc.Col(
#                     dcc.Graph(
#                         figure=fig4, id="ch_cen"
#                     )
#                 )
#             ])
#         ]
#                  )
#     ]),
#
# ])
#
# layout = app.layout
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)

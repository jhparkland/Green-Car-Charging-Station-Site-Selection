from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os, sys
import matplotlib.font_manager as font_manager
import time

from flask_sever import bayesian_network

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_sever.component import Main_Component, Bayesian, CallBack
from Module import Environment
from Module import Social
from Module import Economical
from Module import Technical

# from Module import Bayesian as Ba

cwd = os.getcwd()  # 현재 경로
# 서버연걸
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

# app._favicon = f"{cwd}/assets/logo_icon.ico"
# print(f"{cwd}/assets/logo_icon.ico")

font_dir = [f'{cwd}/assets/NanumSquare.woff']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# 데이터 불러오는 영역
# =====================================================================================================================
'''
환경적 - 오존, 아황산가스, 이산화질소, 미세먼지 =>수소, 전기 동일함
'''
ozone = Environment.Ozone()  # 오존 대기 오염도
so2 = Environment.So2()  # 아황산가스 대기 오염도
no2 = Environment.No2()  # 이산화질소 대기 오염도
pm25 = Environment.FineDust_pm25()  # 미세먼지 pm2.5
pm10 = Environment.FineDust_pm10()  # 미세먼저 pm10

'''
사회적 - 고정인구, 월 평균 유동인구, 충전소당 친환경 차량수(ecc.hydro_fig/hydro_ecc), 도로 보급률
'''
population = Social.Population()  # 고정인구 인구밀도
f_population = Social.FloatingPopulation()  # 월 평균 유동인구 인구밀도
ecc = Social.Eco_friendly_car_registration()  # 충전소당 친환경(전기차, 수소차) 차량수
intersection = Social.Intersection()  # 도로 보급률

'''
경제적 - 수소: 수소 충전소 기대수익, 충전기 구축 비용, 후보지 평균 소득
        전기: 충전기 구축 비용, 후보지 평균 소득
'''
hydro_expected_income = Environment.Total_air_quality()  # 수소 충전소 기대수익
hydro_charger_cost = Economical.Hydrogen_charger_cost()  # 수소차 구축 비용
elec_charger_cost = Social.Highway()  # 전기차 구축 비용
land_cost = Economical.Lpg_land_costs()     # 후보지 평균 소득

'''
기술적 - 수소: 수소 연료 공급 방식, ,충전소당 공급 가능 차량 수
        전기: 전기 충전기 용량
'''
elec_capacity = Social.LPG_charging_station()  # 전기 충전기 용량
hydro_supply_fuel = Social.HVCS()   # 수소 연료 공급 방식
hydro_supply_car = Social.FloatingPopulation() #수소차 충전소 당 공급 가능 차량수

'''
각 요소의 fig는 객체.fig 하면 됨
ex) ozone.fig => 오존 fig
'''
# 전기차 파이차트 데이터프레임
elec_standard_df = pd.DataFrame({
    "기준": ["환경적", "경제적", "기술적", "사회적"],  # 영역명
    "Amount": [4, 1, 2, 3],  # 비율
})
# 수소차 파이차트 데이터프레임
hydro_standard_df = pd.DataFrame({
    "기준": ["환경적", "경제적", "기술적", "사회적"],  # 영역명
    "Amount": [5, 1, 1, 2],  # 비율
})
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

# 최종 부지선정 임시 데이터 프레임
df_e_final_site_selection = pd.DataFrame({
    "최종 부지선정": ["적합", "부적합"],
    "적합확률": [62, 38],
    "최종 부지선정 요소": ["적합 : 67", "부적합 : 33"]
})

df_h_final_site_selection = pd.DataFrame({
    "최종 부지선정": ["적합", "부적합"],
    "적합확률": [62, 38],
    "최종 부지선정 요소": ["적합 : 62", "부적합 : 38"]
})
# =========================================================================================================
# 파이차트 및 확률 차트 생성
fig_1, fig_2, fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4, e_final_fig, h_final_fig \
    = Main_Component.mark_chart(**{"전기차": elec_standard_df,
                                   "수소차": hydro_standard_df,
                                   "경제적": df_economy,
                                   "사회적": df_society,
                                   "환경적": df_environment,
                                   "기술적": df_technique,
                                   "수소_경제적": df_hy_economy,
                                   "수소_사회적": df_hy_society,
                                   "수소_환경적": df_hy_environment,
                                   "수소_기술적": df_hy_technique,
                                   "전기차 최종 부지선정": df_e_final_site_selection,
                                   "수소차 최종 부지선정": df_h_final_site_selection
                                   })
# 전기 파이, 수소 파이, 경제 막대, 환경 막대, 기술 막대, 정규분포 1, 정규분포 2, 정규분포 3, 최종입지
# 나중에 그래프 모두 나오면 그때 수정 부탁함.
# 나중에 그래프 모두 나오면 그때 수정 부탁함.
fig_list = {
    # 전기차 상위요소 차트 - 경제적, 사회적, 환경적, 기술적
    "fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4,
    # 수소차 상위요소 차트 - 경제적, 사회적, 환경적, 기술적
    "hy_fig1": hy_fig1, "hy_fig2": hy_fig2, "hy_fig3": hy_fig3, "hy_fig4": hy_fig4,
    # 파이차트 - 전기, 수소
    "fig_1": fig_1, "fig_2": fig_2,
    # 최종확률차트 - 전기, 수소
    "e_final_fig": e_final_fig, "h_final_fig": h_final_fig,

    # 환경적 - 오존, 일산화탄소, 이산화 질소, 미세먼지
    "ozone": ozone.fig, "so2": so2.fig, "no2": no2.fig, "pm25": pm25.fig, "pm10": pm10.fig,

    # 사회적 - 고정인구, 월 평균 유동인구, 충전소당 친환경 차량수, 도로 보급률
    "population": population.fig,   #고정인구
    "f_population": f_population.fig,   #월 평균 유동인구
    "eleFig": ecc.elec_fig,     # 충전소당 전기차 차랑수,
    "hydFig": ecc.hydro_fig,    # 충전소당 수소차 차량수
    "intersection": intersection.fig,   # 도로 보급률

    # 경제적 - 수소: 수소 충전소 기대 수익, 충전기 구축 비용, 후보지 평균 소득
    #         전기: 충전기 구축 비용, 후보지 평균 소득
    "elec_charger_cost": elec_charger_cost.fig,     # 전기차 충전기 구축 비용
    "hydro_charger_cost": hydro_charger_cost.fig,   # 수소차 충전기 구축 비용
    "land_cost": land_cost.fig,     # 후보지 평균 소득
    "hydro_expected_income": hydro_expected_income.fig,     # 수소 충전소 기대 수익

    # 기술적 - 수소: 수소 연료 공급 방식, 충전소 당 공급 가능 차량 수
    #         전기: 전기 충전기 용량
    "elec_capacity": elec_capacity.fig,  # 전기 충전기 용량
    "hydro_supply_car": hydro_supply_car.fig,   # 수소차 충전소 당 공급 가능 차량 수
    "hydro_supply_fuel": hydro_supply_fuel.fig,     # 수소차 연료 공급 방식
}
# 막대차트 및 파이차트 배경색 설정 및 레이아웃 설정 변경 및
Main_Component.chart_layout(**fig_list)  # 언팩 인자로 전달 필수!.

# cwd = os.getcwd()  # 현재 경로
# final_fig.write_html(cwd + "/assets/final_fig.html")


# 상단 메뉴바(로고표시, 베이지안 네트워크 경로)
navbar = Main_Component.navbar()

# 차트 배치
chart = Main_Component.drawing_chart(**fig_list)  # 언팩 인자로 전달 필수!.

# 그래프 배치
graph = Main_Component.drawing_graph()

# 메인화면
main_layout = Main_Component.main_layout(navbar, graph, chart)

# 베이지안 네트워크 화면
bayesian_layout = bayesian_network.bayesian_chart
# 총 출력
app.layout = Bayesian.layout()

CallBack.page_transitions(bayesian_layout, main_layout)


class Stat:
    state = False

    @staticmethod
    def set_state(state):
        '''
        상태 값 설정
        '''
        Stat.state = state

@app.callback(
    Output("1", "figure"),
    Output("3", "figure"),
    Output("4", "figure"),
    Output("5", "figure"),
    Output("6", "figure"),
    Output("elec_popup", "children"),
    Output("hydro_popup", "children"),
    Output("hydro-selected", "value"),
    Output("elec-prev", "value"),
    Output("hydro-prev", "value"),
    Output("elec_geojson", "click_feature"),
    Output("hydro_geojson", "click_feature"),
    Input("elec_geojson", "click_feature"),
    Input("hydro_geojson", "click_feature"),
    State("elec-prev", "value"),
    State("hydro-prev", "value"),
)
def update(elec, hydro, elec_prev, hydro_prev):
    if id(elec) == id(hydro):
        # print(elec_prev)
        return fig_1, fig1, fig2, fig3, fig4, None, None, 'False', elec_prev, hydro_prev, None, None
    elif hydro is not None:
        Stat.set_state(True)
        Main_Component.hydro_value_update(hydro['properties']['name'], **fig_list)
        if elec_prev is None:
            return fig_2, hy_fig1, hy_fig2, hy_fig3, hy_fig4, None, \
                   Main_Component.hydro_map_chart(hydro['properties']['name'], **fig_list), 'True', \
                   elec_prev, hydro['properties']['name'], None, None
        return fig_2, hy_fig1, hy_fig2, hy_fig3, hy_fig4, Main_Component.elec_map_chart(elec_prev, **fig_list), \
               Main_Component.hydro_map_chart(hydro['properties']['name'], **fig_list), 'True', \
               elec_prev, hydro['properties']['name'], None, None
    else:
        Stat.set_state(False)
        Main_Component.elec_value_update(elec['properties']['name'], **fig_list)
        if hydro_prev is None:
            return fig_1, fig1, fig2, fig3, fig4, Main_Component.elec_map_chart(elec['properties']['name'], **fig_list), \
                   None, 'False', elec['properties']['name'], hydro_prev, None, None
        return fig_1, fig1, fig2, fig3, fig4, Main_Component.elec_map_chart(elec['properties']['name'], **fig_list), \
               Main_Component.hydro_map_chart(hydro_prev, **fig_list), 'False', \
               elec['properties']['name'], hydro_prev, None, None


@app.callback(
    Output("7", "figure"),
    Output("8", "figure"),
    Output("9", "figure"),
    Output("10", "figure"),
    Output("loading1", "style"),
    Output("loading2", "style"),
    Output("loading3", "style"),
    Output("1", "style"),
    Output("3", "style"),
    Output("4", "style"),
    Output("5", "style"),
    Output("6", "style"),
    Output("7", "style"),
    Output("8", "style"),
    Output("9", "style"),
    Output("10", "style"),
    Output("3", "clickData"),
    Output("4", "clickData"),
    Output("5", "clickData"),
    Output("6", "clickData"),
    Output("elec-prev-second", "value"),
    Output("hydro-prev-second", "value"),
    Input("elec_geojson", "click_feature"),
    Input("hydro_geojson", "click_feature"),
    Input("3", "clickData"),
    Input("4", "clickData"),
    Input("5", "clickData"),
    Input("6", "clickData"),
    State("hydro-selected", "value"),
    State("elec-prev", "value"),
    State("hydro-prev", "value"),
    State("elec-prev-second", "value"),
    State("hydro-prev-second", "value"),
)
def update(elec, hydro, econ, soci, envi, tech, hydro_selected, elec_prev, hydro_prev, elec_prev2, hydro_prev2):
    if id(elec) == id(hydro) == id(econ) == id(soci) == id(envi) == id(tech) == id(elec_prev) == id(
            hydro_prev):  # 모두 None일 경우(제일 처음 로드된 경우)
        return ozone.fig, so2.fig, no2.fig, pm10.fig, \
               {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'display': 'none', "position": "relative", "z-index": "2"}, \
               {'visibility': 'hidden', "position": "relative", "z-index": "2"}, \
               {'display': 'none', "position": "relative", "z-index": "2"}, \
               None, None, None, None, elec_prev, hydro_prev
    elif hydro_prev != hydro_prev2:     # 전기차
        return no2.fig, ozone.fig, pm25.fig, so2.fig, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               None, None, None, None, elec_prev, hydro_prev
    elif elec_prev != elec_prev2:   # 수소차
        return ozone.fig, so2.fig, pm25.fig, pm10.fig, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               {'display': 'block', "position": "relative", "z-index": "2"}, \
               None, None, None, None, elec_prev, hydro_prev

    elif econ is not None:  # 경제적
        if hydro_selected == 'False':   # 전기차 - 충전기 구축 비용, 후보지 평균 소득
            return elec_charger_cost.fig, land_cost.fig, ozone.fig, ozone.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev
        else:   # 수소차 - 수소차 충전기 구축 비용, 후보지 평균 소득, 수소 충전소 기대수익
            return hydro_charger_cost.fig, land_cost.fig, hydro_expected_income.fig, ozone.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev

    elif soci is not None:  # 사회
        if hydro_selected == 'False':   # 전기차 - 고정인구, 월 평균 유동인구, 충전소 당 전기차 차량 수, 도로 보급률
            return population.fig, f_population.fig, ecc.elec_fig, intersection.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev
        else:   # 수소차 - 도로 보급률, 월 평균 유동인구, 충전소 당 수소차 차량 수 , 고정인구
            return intersection.fig, f_population.fig, ecc.hydro_fig, population.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev

    elif tech is not None:  # 기술
        if hydro_selected == 'False':   # 전기차 - 전기 충전기 용량
            return elec_capacity.fig, ozone.fig, no2.fig, so2.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev
        else:   # 수소차 - 수소 연료 공급 방식, 수소차 충전소 당 공급 가능 차량 수
            return hydro_supply_fuel.fig, hydro_supply_car.fig, so2.fig, so2.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   {'display': 'none', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev

    elif envi is not None:  # 환경
        if hydro_selected == 'False':   # 전기차 - 오존, 아황산가스, 미세먼먼 pm2.5, 미세먼지 pm10
            return ozone.fig, so2.fig, pm25.fig, pm10.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev
        else:   #수소차 - 이산화질소, 오존, pm2.5, pm1.0
            return no2.fig, ozone.fig, pm25.fig, so2.fig, \
                   {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   {'display': 'block', "position": "relative", "z-index": "2"}, \
                   None, None, None, None, elec_prev, hydro_prev


@app.callback(
    # 출력- 상위요소, 최종확률
    Output("bay_env", "figure"),
    Output("bay_soc", "figure"),
    Output("bay_eco", "figure"),
    Output("bay_tec", "figure"),
    Output("final_fig", "figure"),
    # 하위요소
    Output("elec_hydro_Fig", "figure"),
    Output("charger_cost", "figure"),   # 경제적 - 충전기 구축 비용(elec_charger_cost, hydro_charger_cost)
    Output("hydro_expected_income", "figure"),     # 수소 충전소 기대 수익
    Output("capacity_insatll", "figure"),   # 전기 : 전기 충전기 용량 - elec_capacity / 수소 : 수소차 충전소 당 공급 가능 차량 수 - hydro_supply_car
    Output("supply_fuel", "figure"),    # 기술적 - 수소차 연료 공급 방식

    Output("hydro_expected_income", "style"),
    Output("supply_fuel", "style"),
    # 입력
    Input("bay_env", "clickData"),
    Input("bay_soc", "clickData"),
    Input("bay_eco", "clickData"),
    Input("bay_tec", "clickData"),
)
def bayseian(bay_env, bay_soc, bay_eco, bay_tec, ):
    if Stat.state:      # 수소차
        return hy_fig3, hy_fig2, hy_fig1, hy_fig4, h_final_fig, \
               ecc.hydro_fig, hydro_charger_cost.fig, hydro_expected_income.fig, hydro_supply_car.fig, \
               hydro_supply_fuel.fig, \
               {'display': 'block', "position": "relative", "z-index": "2"},\
               {'display': 'block', "position": "relative", "z-index": "2"}


    else:   # 전기차
        return fig3, fig2, fig1, fig4, e_final_fig, \
               ecc.elec_fig, elec_charger_cost.fig, hydro_expected_income.fig, elec_capacity.fig, \
               hydro_supply_fuel.fig, \
               {'display': 'none', "position": "relative", "z-index": "2"},\
               {'display': 'none', "position": "relative", "z-index": "2"}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=False)
from dash import Dash, html
import dash_bootstrap_components as dbc
import pandas as pd
import os, sys
import matplotlib.font_manager as font_manager

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask_sever.component import Bayesian
from Module import Environment
from Module import Social
from Module import Economical
from Module import Technical

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
###################데이터 불러오는 영역####################3
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
경제적 - 수소: 수로 충전소 기대수익, 충전기 구축 비용, 후보지 평균 소득
        전기: 충전기 구축 비용, 후보지 평균 소득
'''
hydro_expexted_income = Environment.Total_air_quality()  # 수소 충전소 기대수익
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
fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4, e_final_fig, h_final_fig \
    = Bayesian.bay_bar_layout(**{
                                   #상위- 막대차트
                                   "경제적": df_economy,      # 전기 경제적
                                   "사회적": df_society,   # 전기 환경적
                                   "환경적": df_environment,   # 전기 경제적
                                   "기술적": df_technique,     # 전기 기술적
                                   "수소_경제적": df_hy_economy,     # 수소 경제적
                                   "수소_사회적": df_hy_society,     # 수소 사회적
                                   "수소_환경적": df_hy_environment,     # 수소 환경적
                                   "수소_기술적": df_hy_technique,      # 수소 기술적적
                                  #최종부지선정 - 막대차트
                                   "전기차 최종 부지선정": df_e_final_site_selection,    # 전기차 최종 부지
                                   "수소차 최종 부지선정": df_h_final_site_selection     # 수소차 최종 부지선정
                                   })

# 전기 파이, 수소 파이, 경제 막대, 환경 막대, 기술 막대, 정규분포 1, 정규분포 2, 정규분포 3, 최종입지
fig_list = {
    # 전기차 상위요소 차트 - 경제적, 사회적, 환경적, 기술적
    "fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4,
    # 수소차 상위요소 차트 - 경제적, 사회적, 환경적, 기술적
    "hy_fig1": hy_fig1, "hy_fig2": hy_fig2, "hy_fig3": hy_fig3, "hy_fig4": hy_fig4,
    # 최종확률차트 -
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
    "hydro_expected_income": hydro_expexted_income.fig,

    # 기술적 - 수소: 수소 연료 공급 방식, 충전소당 공급 가능 차량 수
    #         전기: 전기 충전기 용량
    "elec_capacity": elec_capacity.fig,  # 전기 충전기 용량
    "hydro_supply_car": hydro_supply_car.fig,   # 수소차 충전소 당 공급 가능 차량
    "hydro_supply_fuel": hydro_supply_fuel.fig,     # 수소차 연료 공급 방식
}

# 막대차트 및 파이차트 배경색 설정 및 레이아웃 설정 변경 및
Bayesian.bay_layout(**fig_list)  # 언팩 인자로 전달 필수!.
#베이지안 배치
bayesian_chart = Bayesian.bayesian_network(**fig_list)

app.layout = html.Div(bayesian_chart)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)
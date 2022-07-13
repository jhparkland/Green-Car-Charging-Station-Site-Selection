from flask import Flask
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly
import pandas as pd
import os, sys
import matplotlib.font_manager as font_manager
from component import Main_Component, Bayesian, CallBack
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Module import Environment
from Module import Social
import time


# 서버연걸
#server = Flask(__name__)
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
ozone = Environment.Ozone()  # 오존 데이터
print(f"적합: {ozone.t_pro}, 부적합: {ozone.f_pro}")  # 오존 확률
ozone.fig.write_html("ozone.html")

so2 = Environment.So2()  # 아황산가스 데이터
print(f"적합: {so2.t_pro}, 부적합: {so2.f_pro}")  # 아황산가스 확률

pm25 = Environment.FineDust_pm25()  # 미세먼지 pm2.5
print(f"적합: {pm25.t_pro}, 부적합: {pm25.f_pro}")  # 미세먼지 pm2.5 확률

pm10 = Environment.FineDust_pm10()  # 미세먼저 pm10
print(f"적합: {pm10.t_pro}, 부적합: {pm10.f_pro}")  # 미세먼지 pm10 확률
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
# =========================================================================================================
# 파이차트 및 확률 차트 생성
fig_1, fig_2, fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4\
    = Main_Component.mark_chart(**{"전기차": elec_standard_df,
                                    "수소차": hydro_standard_df,
                                    "경제적": df_economy,
                                    "사회적": df_society,
                                    "환경적": df_environment,
                                    "기술적": df_technique,
                                    "수소_경제적": df_hy_economy,
                                    "수소_사회적": df_hy_society,
                                    "수소_환경적": df_hy_environment,
                                    "수소_기술적": df_hy_technique
                                    })

# 전기 파이, 수소 파이, 경제 막대, 환경 막대, 기술 막대, 정규분포 1, 정규분포 2, 정규분포 3, 최종입지
# 나중에 그래프 모두 나오면 그때 수정 부탁함.
fig_list = {"fig1": fig1,
            "fig2": fig2,
            "fig3": fig3,
            "fig4": fig4,
            "hy_fig1": hy_fig1,
            "hy_fig2": hy_fig2,
            "hy_fig3": hy_fig3,
            "hy_fig4": hy_fig4,
            "fig_1": fig_1,
            "fig_2": fig_2,
            "ozone": ozone.fig,
            "so2": so2.fig,
            "pm25": pm25.fig,
            "pm10": pm10.fig
            }

# 막대차트 및 파이차트 배경색 설정 및 레이아웃 설정 변경 및
Main_Component.chart_layout(**fig_list)  # 언팩 인자로 전달 필수!.

# os.chdir('../')
# cwd = os.getcwd()  # 현재 경로
# fig4.write_html(cwd +"\\flask_sever\\assets\\fig4.html")

# 상단 메뉴바(로고표시, 베이지안 네트워크 경로)
navbar = Main_Component.navbar()

# 차트 배치
chart = Main_Component.drawing_chart(**fig_list)  # 언팩 인자로 전달 필수!.

# 메인화면
main_layout = Main_Component.main_layout(navbar, chart)

# 베이지안 네트워크 화면
bayesian_layout = Bayesian.print_hello()

# 총 출력
app.layout = Bayesian.layout()


CallBack.page_transitions(bayesian_layout, main_layout)

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
        return hy_fig1, hy_fig2, hy_fig3, hy_fig4

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
    Output("10", "figure"),
    Input("3", "clickData"),
    Input("4", "clickData"),
    Input("5", "clickData"),
    Input("6", "clickData")
)
def update(econ, soci, envi, tech):
    if econ is not None:
        return ozone.fig, ozone.fig, ozone.fig, ozone.fig
    elif soci is not None:
        return so2.fig, so2.fig, so2.fig, so2.fig
    elif envi is not None:
        return ozone.fig, so2.fig, pm25.fig, pm10.fig,
    else:
        return so2.fig, so2.fig, so2.fig, so2.fig

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=False)
from flask import Flask
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import os, sys
import matplotlib.font_manager as font_manager
from component import Main_Component, Bayesian, CallBack
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Module import Environment
from Module import Social

# from Module import Bayesian as Ba


# 서버연걸
server = Flask(__name__)
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True,
           server=server,
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )

app.title = "에코 차징 플레이스"
app._favicon = "logo_icon.ico"

font_dir = ['/assets/NanumSquare']
for font in font_manager.findSystemFonts(font_dir):
    font_manager.fontManager.addfont(font)

# 데이터 불러오는 영역
# ========================================================================================================
ozone = Environment.Ozone()  # 오존 데이터
print(f"적합: {ozone.t_pro}, 부적합: {ozone.f_pro}")  # 오존 확률

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
    "경제적": ["True", "False"],  # x축 라벨
    "적합확률": [80, 20],  # 확률
    "경제적 요소": ["True", "False"]  # 색 구분 위해 넣음
})
# 사회적 확률차트 데이터프레임
df_society = pd.DataFrame({
    "사회적": ["True", "False"],  # x축 라벨
    "적합확률": [70, 30],  # 확률
    "사회적 요소": ["True", "False"]  # 색 구분 위해 넣음
})
# 환경적 확률차트 데이터프레임
df_environment = pd.DataFrame({
    "환경적": ["True", "False"],  # x축 라벨
    "적합확률": [80, 20],  # 확률
    "환경적 요소": ["True", "False"]  # 색 구분 위해 넣음
})
# 기술적 확률차트 데이터프레임
df_technique = pd.DataFrame({
    "기술적": ["True", "False"],  # x축 라벨
    "적합확률": [75, 35],  # 확률
    "기술적 요소": ["True", "False"]  # 색 구분 위해 넣음
})
# =========================================================================================================
# 파이차트 및 확률 차트 생성
fig_1, fig_2, fig1, fig2, fig3, fig4 = Main_Component.mark_chart(**{"전기차": elec_standard_df,
                                                                    "수소차": hydro_standard_df,
                                                                    "경제적": df_economy,
                                                                    "사회적": df_society,
                                                                    "환경적": df_environment,
                                                                    "기술적": df_technique
                                                                    })

# 전기 파이, 수소 파이, 경제 막대, 환경 막대, 기술 막대, 정규분포 1, 정규분포 2, 정규분포 3, 최종입지
# 나중에 그래프 모두 나오면 그때 수정 부탁함.
fig_list = {"fig1": fig1,
            "fig2": fig2,
            "fig3": fig3,
            "fig4": fig4,
            "fig_1": fig_1,
            "fig_2": fig_2,
            "ozone": ozone.fig,
            "so2": so2.fig
            }

# 막대차트 및 파이차트 배경색 설정 및 레이아웃 설정 변경 및
Main_Component.chart_layout(**fig_list)  # 언팩 인자로 전달 필수!.

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

save_hydro = save_elec =save_econ = save_soci = save_envi = save_tech = {}

CallBack.elec_piechart_click(save_elec, save_hydro)
CallBack.hydro_piechart_click(save_elec, save_hydro)
CallBack.soci_chart_click(save_econ, save_soci, save_envi, save_tech)
CallBack.envi_chart_click(save_econ, save_soci, save_envi, save_tech)
CallBack.tech_chart_click(save_econ, save_soci, save_envi, save_tech)
CallBack.econ_chart_click(save_econ, save_soci, save_envi, save_tech)

@callback(  # 파이차트 -> 확률차트 이벤트 연결 (이새끼는 구조를 모르겠다 bro)
    Output("3", "figure"),
    Output("4", "figure"),
    Output("5", "figure"),
    Output("6", "figure"),
    Input("1", "clickData"),
    Input("2", "clickData"),
)
def update(elec, hydro):
    if elec is not None:
        return fig_1, fig_1, fig_1, fig_1
    else:
        return fig_2, fig_2, fig_2, fig_2

@callback(  # 확률차트 -> 정규분포 이벤트 설정
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
        return ozone.fig, so2.fig, fig1
    elif soci is not None:
        return fig2, so2.fig, fig2
    elif envi is not None:
        return fig3, so2.fig, ozone.fig
    else:
        return so2.fig, so2.fig, so2.fig


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9000, debug=True)

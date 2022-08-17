import pandas as pd
import plotly.express as px
from Module import init as dir
from Module.Social import Social, Population, FloatingPopulation


class Technical:
    """
    기술적 요소 모델링
    """

    @staticmethod
    def check_location(location, x, y):
        '''
        LPG 충전소 여부 판단.
        '''
        if (x, y) in location:
            complex_cs_pro = 1.0
        else:
            complex_cs_pro = 0.0

        return complex_cs_pro, 1 - complex_cs_pro

    @staticmethod
    def charge_type(foottraffic_pro, busan_people_pro):
        '''
        foottraffic_pro : 유동인구 적합도
        busan_people_pro : 고정인구 적합도
        charger_pro : 설정하고자 하는 충전기 타입의 적합도 비율 초기값(0~1)
        '''

        # 급속 충전기 초기 확률:0.38
        charger_pro = 0.38

        if foottraffic_pro >= busan_people_pro:
            charger_type = 'Fast Charge'
        else:
            charger_type = 'Standard Charge'

        # 유동인구와 기존인구와 차이가 나는 만큼 더 많은 확률 부여
        if foottraffic_pro >= busan_people_pro:
            charger_type = '급속 충전'
            diff = foottraffic_pro - busan_people_pro
            charger_pro += diff
            if charger_pro > 1:
                charger_pro = 1.0
        elif foottraffic_pro < busan_people_pro:
            charger_type = '완속 충전'
            diff = busan_people_pro - foottraffic_pro
            charger_pro -= diff
            if charger_pro < 0:
                charger_pro = 0.0

        return charger_type, charger_pro, 1 - charger_pro

    @staticmethod
    def bar_chart(t_pro, f_pro, t_text, f_text, variable_name):
        dataframe = pd.DataFrame({
            "급속/완속": [t_text, f_text],
            "충전시간": [t_pro, f_pro],
            variable_name: [f"{t_text} : {t_pro}", f"{f_text} : {f_pro}"]
        })
        fig = px.bar(dataframe, x="급속/완속", y="충전시간", color=variable_name, text=variable_name)
        # fig.update_yaxes(visible=False)
        # fig.update_xaxes(visible=False)
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, title_font_size=18, margin_l=10, margin_r=10, margin_b=20,
                          font_family='NanumSquare', showlegend=False)
        # fig.show()
        return fig


class Complex_charging_station(Technical):
    '''
    복합 충전소 적합도
    '''

    def __init__(self):
        self.file_path = dir.getdir("부산 LPG 충전소 현황(한국가스안전공사).csv")  # 데이터 경로
        self.df_lpg = pd.read_csv(self.file_path, encoding='cp949')
        self.df_lpg = self.df_lpg[self.df_lpg['면적'] >= 1500].reset_index(drop=True)
        self.location = list(zip(self.df_lpg['위도'].tolist(), self.df_lpg['경도'].tolist()))
        self.t_pro, self.f_pro = Technical.check_location(self.location, 35.18601331, 129.0559741)
        self.fig = Technical.bar_chart(self.t_pro * 100, self.f_pro * 100, "적합", "부적합", "복합 충전소 적합도")


class Charging_time(Technical):
    '''
    기술적 요소 - 충전시간에 따른 충전방식
    '''

    def __init__(self):
        self.population = Population()
        self.population_pro = self.population.t_pro
        self.fpopulation = FloatingPopulation()
        self.fpopulation_pro = self.fpopulation.t_pro
        self.charger_type, self.t_pro, self.f_pro = Technical.charge_type(self.fpopulation_pro, self.population_pro)
        self.fig = Technical.bar_chart(round(self.t_pro, 3) * 100, round(self.f_pro, 3) * 100, "급속", "완속",
                                       self.charger_type)

# if __name__ == '__main__':
#     ccs = Complex_charging_station()
#     charging_time = Charging_time()
#
#     ccs.fig.show()
#     charging_time.fig.show()
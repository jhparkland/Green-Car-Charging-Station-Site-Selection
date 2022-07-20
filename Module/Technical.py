import pandas as pd
import plotly.express as px
import init as dir
import numpy as np
from scipy.stats import norm
from Social import Social, Population, FloatingPopulation


class Technical:
    """
    기술적 요소 모델링
    """
    @staticmethod
    def cal_norm(mean, std, min, max, value, affect):
        '''
        정규분포에서 value에 대한 누적확률 구하기
        mean: 평균값
        std: 표준편차
        min: 관측된 데이터의 최솟값
        max: 관측된 데이터의 최댓값
        value: 누적확률을 구하고자 하는 데이터의 측정값
        affect: 입지에 긍정/부정적인 영향(True/False)
        '''

        min = min - std

        # 확률 값을 구할 특정 구간의 범위 설정
        cum_a = np.linspace(min, value, 100)
        cum_b = np.linspace(value, max, 100)

        pro = norm(mean, std).cdf(value) - norm(mean, std).cdf(min).round(3)
        if affect == False:
            pro = 1 - pro

        # 최종 누적확률 반환
        return pro, 1 - pro


    @staticmethod
    def check_location(location, x, y):
        '''
        LPG 충전소 여부 판단.
        '''
        if (x, y) in location:
            complex_cs_pro = 1.0
        else:
            complex_cs_pro = 0.0

        return complex_cs_pro, 1-complex_cs_pro

    @staticmethod
    def charge_type(people,floating):
        '''
        busan_people : 고정인구 수
        foottraffic : 유동인구 수
        charger_pro : 설정하고자 하는 충전기 타입의 적합도 비율 초기값(0~1)
        '''

        # 급속 충전기 초기 확률:0.38
        charger_pro = 0.38
        people_file_path = dir.getdir('행정구역 인구 데이터.csv')
        floating_file_path = dir.getdir('부산 유동인구 데이터.csv')
        df_busan_people = pd.read_csv(people_file_path, encoding='cp949')
        df_foottraffic = pd.read_csv(floating_file_path, encoding='cp949')
        people_pro,a = Technical.cal_norm(df_busan_people['총인구수 (명)'].mean(),df_busan_people['총인구수 (명)'].std(),df_busan_people['총인구수 (명)'].min(),df_busan_people['총인구수 (명)'].max(),people,True)
        foottraffic_pro,b = Technical.cal_norm(df_foottraffic['월 평균'].mean(),df_foottraffic['월 평균'].std(),df_foottraffic['월 평균'].min(),df_foottraffic['월 평균'].max(),floating,True)
        # 유동인구와 기존인구와 차이가 나는 만큼 더 많은 확률 부여
        if foottraffic_pro >= people_pro:
            diff = foottraffic_pro - people_pro
            charger_pro += diff
            if charger_pro > 1:
                charger_pro = 1.0
        elif foottraffic_pro < people_pro:
            diff = people_pro - foottraffic_pro
            charger_pro -= diff
            if charger_pro < 0:
                charger_pro = 0.0

        return  charger_pro, 1 - charger_pro

    @staticmethod
    def bar_chart(t_pro, f_pro, t_text, f_text, variable_name):
        dataframe = pd.DataFrame({
            "기술적":[t_text,f_text],
            "적합확률":[t_pro,f_pro],
            variable_name:[f"{t_text} : {t_pro}",f"{f_text} : {f_pro}"]
            })
        fig = px.bar(dataframe, x="기술적", y="적합확률", color=variable_name, text = variable_name)
        fig.show()
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
        self.fig = Technical.bar_chart(self.t_pro*100,self.f_pro*100,"적합","부적합","복합 충전소 적합도")


class Charging_time(Technical):
    '''
    기술적 요소 - 충전시간에 따른 충전방식
    '''

    def __init__(self):
        self.population = Population()
        self.population_pro = self.population.t_pro
        self.fpopulation = FloatingPopulation()
        self.fpopulation_pro = self.fpopulation.t_pro
        self.t_pro, self.f_pro = Technical.charge_type(self.population_pro, self.fpopulation)
        self.fig = Technical.bar_chart(round(self.t_pro,3)*100,round(self.f_pro,3)*100,"급속","완속","급속충전 적합도")

if __name__ == '__main__':
    ccs = Complex_charging_station()
    charging_time = Charging_time()

    ccs.fig.show()
    charging_time.fig.show()

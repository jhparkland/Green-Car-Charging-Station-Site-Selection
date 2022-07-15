import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
from Module import init as dir


class Social:
    '''
    사회적 요소 모델링
    '''

    @staticmethod
    def ChangeType(df, col_name, type):
        '''
        데이터 프레임 특정 컬럼 타입 변경
        :param df: 대상 DataFrame
        :param col_name: 컬럼 이름
        :return:
        '''
        df[col_name] = df[col_name].astype(type)
        return df

    @staticmethod
    def pretreatment(df, start, stop):
        '''
        데이터 프레임 특정 열 삭제
        :param df: 대상 데이터 프레임
        :param start: 컬럼 시작
        :param stop: 컬럼 끝
        :return: 삭제 처리된 데이터 프레임
        '''
        col = df.iloc[:, start:stop].columns.tolist()
        df.drop(columns=col, inplace=True)
        # return df

    @staticmethod
    def advanced_replace(df, col, str, regex):
        '''
        DataFrame 특정 열의 특수문자 제거
        :param df: 대상 DataFrame
        :param col: column
        :param str: 제거할 특수 문자.
        :param regex: 적용할 정규표현식
        :return:
        '''
        df[col] = df[col].replace(str, 0)
        df[col] = df[col].replace(to_replace=regex, value=r'', regex=True)
        return df

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
        red = 'rgb(239,85,59)'
        blue = 'rgb(100,110,250)'
        fig = go.Figure()

        # 확률 값을 구할 특정 구간의 범위 설정
        cum_a = np.linspace(min, value, 100)
        cum_b = np.linspace(value, max, 100)

        pro = norm(mean, std).cdf(value) - norm(mean, std).cdf(min).round(3)
        if affect == True:
            # 구간 사이에 색을 채움
            fig.add_trace(
                go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='적합', line=dict(color=blue)))
            fig.add_trace(
                go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='부적합', line=dict(color=red)))
            fig.update_yaxes(visible=False)
            annotations = []
            annotations.append(
                dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=blue), xshift=-40, yshift=-100, bordercolor=blue, borderwidth=2))
            annotations.append(
                dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=red), xshift=40, yshift=-100, bordercolor=red, borderwidth=2))
        else:
            fig.add_trace(
                go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='부적합', line=dict(color=red)))
            fig.add_trace(
                go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='적합', line=dict(color=blue)))
            fig.update_yaxes(visible=False)
            annotations = []
            annotations.append(
                dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=red), xshift=-40, yshift=-100, bordercolor=red, borderwidth=2))
            annotations.append(
                dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=blue), xshift=40, yshift=-100, bordercolor=blue, borderwidth=2))
            pro = 1 - pro
        fig.update_layout(annotations=annotations)

        # 최종 누적확률 반환
        return fig, pro, 1 - pro


class Population(Social):
    '''
    사회적 요소 - 행정구역별 인구
    '''

    def __init__(self):
        self.file_path = dir.getdir("행정구역 인구 데이터.csv")  # 데이터 경로
        self.busan_people_standard = 200000  # 고정인구 판단 기준
        self.df_people = pd.read_csv(self.file_path, encoding='cp949', header=1)
        self.df_busan_people = self.df_people[28:44].sort_values('행정구역(시군구)별')
        self.df_busan_people.set_index('행정구역(시군구)별', inplace=True)  # 부산 추출
        self.df_busan_people['총인구수 (명)'] = self.df_busan_people['총인구수 (명)'].astype(float)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_busan_people['총인구수 (명)'].mean(),
                                                           self.df_busan_people['총인구수 (명)'].std(),
                                                           self.df_busan_people['총인구수 (명)'].min(),
                                                           self.df_busan_people['총인구수 (명)'].max(),
                                                           self.busan_people_standard,
                                                           False
                                                           )


class FloatingPopulation(Social):
    """
    사회적 요소 - 유동인구 데이터
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 유동인구 데이터.csv")  # 데이터 경로
        self.foot_traffic_standard = 400000  # 유동인구 판단기준
        self.df_foot_traffic = pd.read_csv(self.file_path, encoding='cp949')
        Social.pretreatment(self.df_foot_traffic, 1, -1)
        self.df_foot_traffic.set_index('구군', inplace=True)
        self.df_foot_traffic = Social.advanced_replace(self.df_foot_traffic, '월 평균', '-', r'[^0-9.0-9]')
        self.df_foot_traffic['월 평균'] = self.df_foot_traffic['월 평균'].astype(float)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_foot_traffic['월 평균'].mean(),
                                                           self.df_foot_traffic['월 평균'].std(),
                                                           self.df_foot_traffic['월 평균'].min(),
                                                           self.df_foot_traffic['월 평균'].max(),
                                                           self.foot_traffic_standard,
                                                           False
                                                           )


class Eco_friendly_car_registration(Social):
    """
    사회적 요소 - 친환경 자동차 등록수 데이터
    """

    def __init__(self):
        self.file_path = dir.getdir("연료별 자동차 등록 수.csv")  # 데이터 경로
        self.elec_vehicle_standard = 50000  # 전기차 등록 수
        self.hydro_vehicle_standard = 1500  # 수소차 등록 수
        self.df_vehicle = pd.read_csv(self.file_path, encoding='cp949')
        Social.pretreatment(self.df_vehicle, 1, 3)
        # 전국 자동차 수 통계값 구하기 (전기, 수소)
        columns = self.df_vehicle.iloc[:, 1:].columns.tolist()
        for col in columns:
            self.df_vehicle = Social.advanced_replace(self.df_vehicle, col, '-', r'[^0-9.0-9]')
            self.df_vehicle[col] = self.df_vehicle[col].astype(int)

        self.df_elec_vehicle = self.df_vehicle.iloc[3:7, :-1].sum()  # 전기 + 하이브리드
        self.df_elec_vehicle = self.df_elec_vehicle[1:].astype(int)
        self.df_hydro_vehicle = self.df_vehicle.iloc[8, 1:-1].astype(int)

        self.elec_fig, self.elec_t_pro, self.elec_f_pro = Social.cal_norm(self.df_elec_vehicle.mean(),
                                                                          self.df_elec_vehicle.std(),
                                                                          self.df_elec_vehicle.min(),
                                                                          self.df_elec_vehicle.max(),
                                                                          self.elec_vehicle_standard,
                                                                          False
                                                                          )

        self.hydro_fig, self.hydro_t_pro, self.hydro_f_pro = Social.cal_norm(self.df_hydro_vehicle.mean(),
                                                                             self.df_hydro_vehicle.std(),
                                                                             self.df_hydro_vehicle.min(),
                                                                             self.df_hydro_vehicle.max(),
                                                                             self.hydro_vehicle_standard,
                                                                             False
                                                                             )


class LPG_charging_station(Social):
    """
    사회적 요소 - LPG 충전소 현황
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 LPG 충전소 현황.csv")  # 데이터 경로
        self.lpg_standard = 2
        self.df_lpg = pd.read_csv(self.file_path, encoding='cp949')
        self.df_lpg = self.df_lpg[self.df_lpg['면적'] >= 1500].reset_index(
            drop=True)  # 복합충전소 규제로 인해 부지의 크기는 1500m^2 이상 요구.
        self.lpg_group = self.df_lpg.groupby('행정구역').count()
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.lpg_group['업소명'].mean(),
                                                           self.lpg_group['업소명'].std(),
                                                           self.lpg_group['업소명'].min(),
                                                           self.lpg_group['업소명'].max(),
                                                           self.lpg_standard,
                                                           False
                                                           )


class EVCS(Social):
    """
    사회적 요소 - 전기차 충전소 현황
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 전기차 충전소 현황.csv")  # 데이터 경로
        self.evcs_standard = 500
        self.df_evcs = pd.read_csv(self.file_path, encoding='cp949')
        self.evcs_group = self.df_evcs.groupby('시군구').count()
        self.evcs_group['충전소'] = self.evcs_group['충전소'].astype(int)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.evcs_group['충전소'].mean(),
                                                           self.evcs_group['충전소'].std(),
                                                           self.evcs_group['충전소'].min(),
                                                           self.evcs_group['충전소'].max(),
                                                           self.evcs_standard,
                                                           True
                                                           )


class HVCS(Social):
    """
    사회적 요소 - 수소차 충전소 현황
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 수소차 충전소 현황.csv")  # 데이터 경로
        self.HVCS_standard = 15
        self.df_hvcs = pd.read_csv(self.file_path, encoding='cp949')

        self.address_city = []
        self.address_gu = []

        for i in range(self.df_hvcs.shape[0]):
            strings = self.df_hvcs.iloc[i]['주소'].split()
            self.address_city.append(strings.pop(0))
            self.address_gu.append(strings.pop(0))

        self.df_hvcs.insert(2, "시", self.address_city)
        self.df_hvcs.insert(3, "구", self.address_gu)

        self.hvcs_group = self.df_hvcs.groupby('시').count()
        self.df_hvcs = self.df_hvcs[self.df_hvcs['시'] == '부산광역시'].reset_index(drop=True)
        self.hvcs_group['충전소'] = self.hvcs_group['충전소'].astype(int)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.hvcs_group['충전소'].mean(),
                                                           self.hvcs_group['충전소'].std(),
                                                           self.hvcs_group['충전소'].min(),
                                                           self.hvcs_group['충전소'].max(),
                                                           self.HVCS_standard,
                                                           True
                                                           )


class Intersection(Social):
    """
    사회적 요소 - 교통편의성(교차로) 정보
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 주차장 현황(교차로).csv")  # 데이터 경로
        self.intersection_standard = 100
        self.df_parking_intersection = pd.read_csv(self.file_path, encoding='cp949')
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_parking_intersection['교차로'].mean(),
                                                           self.df_parking_intersection['교차로'].std(),
                                                           self.df_parking_intersection['교차로'].min(),
                                                           self.df_parking_intersection['교차로'].max(),
                                                           self.intersection_standard,
                                                           False
                                                           )


class Highway(Social):
    """
    사회적 요소 - 고속도로 여부(정성적)
    """

    def __init__(self):
        self.parking_file_path = '부산 주차장 현황(교차로).csv'
        self.df_parking = pd.read_csv(self.parking_file_path, encoding='cp949')
        self.highway_standard = 1000
        self.df_parking_highway = self.df_parking[self.df_parking['주변고속도로까지 최단거리']!='-'].reset_index(drop=True)
        self.df_parking_highway['주변고속도로까지 최단거리'] = self.df_parking_highway['주변고속도로까지 최단거리'].astype(float)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm( self.df_parking_highway['주변고속도로까지 최단거리'].mean(),
                                                            self.df_parking_highway['주변고속도로까지 최단거리'].std(),
                                                            self.df_parking_highway['주변고속도로까지 최단거리'].min(),
                                                            self.df_parking_highway['주변고속도로까지 최단거리'].max(),
                                                            self.highway_standard,
                                                            True
                                                            )

if __name__ == '__main__':
    population = Population()
    f_population = FloatingPopulation()
    ecc = Eco_friendly_car_registration()
    lpg = LPG_charging_station()
    evcs = EVCS()
    hvcs = HVCS()
    intersection = Intersection()
    highway = Highway()  # 정성적

    population.fig.show()  # 고정 인구
    f_population.fig.show()  # 유동 인구
    ecc.elec_fig.show()  # 전기차
    ecc.hydro_fig.show()  # 수소차
    lpg.fig.show()  # lpg 충전
    evcs.fig.show()  # 전기 충전
    hvcs.fig.show()  # 수소 충전
    intersection.fig.show()  # 교차로
    highway.fig.show()
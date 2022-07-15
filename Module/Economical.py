import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
from Module import init as dir


class Economical:
    """
    경제적 요소 모델링
    """

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


class Electricity_charger_cost(Economical):
    """
    경제적 요소 - 전기차 충전소 설치 비용
    """
    def __init__(self):
        self.t_pro = 0

class Hydrogen_charger_cost(Economical):
    """
    경제적 요소 - 수소차 충전소 설치 지용
    """

    def __init__(self):
        self.file_path = dir.getdir("수소 충전소 종류별 구축 비용.csv")  # 데이터 경로
        self.hvcs_construction_cost_standard = 3_000_000_000  # 수소충전소 구축 비용
        self.df_hvcs_construction_cost = pd.read_csv(self.file_path, encoding='cp949')
        self.df_hvcs_construction_cost = self.df_hvcs_construction_cost.set_index('충전소 종류')
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_hvcs_construction_cost['구축 비용'].mean(),
                                                               self.df_hvcs_construction_cost['구축 비용'].std(),
                                                               self.df_hvcs_construction_cost['구축 비용'].min(),
                                                               self.df_hvcs_construction_cost['구축 비용'].max(),
                                                               self.hvcs_construction_cost_standard,
                                                               True
                                                               )


class Lpg_land_costs(Economical):
    """
    경제적 요소 - LPG 충전소 토지비용
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 LPG 충전소 현황.csv")  # 데이터 경로
        self.lpg_cost_standard = 6_000_000_000  # LPG 충전소 토지비용
        self.df_lpg = pd.read_csv(self.file_path, encoding='cp949')
        self.df_lpg = self.df_lpg[self.df_lpg['면적'] >= 1500].reset_index(
            drop=True)  # 복합충전소 규제로 인해 부지의 크기는 1500m^2 이상 요구.
        self.cost = []
        for i in range(self.df_lpg.shape[0]):
            area = self.df_lpg.iloc[i]['면적']
            price = self.df_lpg.iloc[i]['공시지가']
            self.cost.append(area * price)

        self.df_lpg.insert(8, '토지비용', self.cost)
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_lpg['토지비용'].mean(),
                                                               self.df_lpg['토지비용'].std(),
                                                               self.df_lpg['토지비용'].min(),
                                                               self.df_lpg['토지비용'].max(),
                                                               self.lpg_cost_standard,
                                                               True
                                                               )


class Parkinglot(Economical):
    """
    경제적 요소 - 주차 구획 수
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 주차장 현황(교차로).csv")  # 데이터 경로
        self.parking_area_standard = 100  # 주차구획 수
        self.df_parking = pd.read_csv(self.file_path, encoding='cp949')
        self.df_parking_area = self.df_parking['주차구획수'].astype(int)
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_parking_area.mean(),
                                                               self.df_parking_area.std(),
                                                               self.df_parking_area.min(),
                                                               self.df_parking_area.max(),
                                                               self.parking_area_standard,
                                                               False
                                                               )

if __name__ == '__main__':

    elec_charger_cost = Electricity_charger_cost() # 전기차 충전소 설치 비용
    hydro_charger_cost = Hydrogen_charger_cost() # 수소차 충전소 설치 비용
    lpg_land_cost = Lpg_land_costs() # LPG 토지 비용
    parkinglot = Parkinglot() # 주차 구획수

    #elec_charger_cost.fig.show()
    hydro_charger_cost.fig.show()
    lpg_land_cost.fig.show()
    parkinglot.fig.show()

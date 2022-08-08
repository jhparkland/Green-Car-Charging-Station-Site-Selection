import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from scipy.stats import norm
import init as dir


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
                dict(x=(max+min)/2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=blue), xshift=-30, yshift=40, bordercolor=blue, borderwidth=2))
            annotations.append(
                dict(x=(max+min)/2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=red), xshift=30, yshift=40, bordercolor=red, borderwidth=2))
        else:
            fig.add_trace(
                go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='부적합', line=dict(color=red)))
            fig.add_trace(
                go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='적합', line=dict(color=blue)))
            fig.update_yaxes(visible=False)
            annotations = []
            annotations.append(
                dict(x=(max+min)/2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=red), xshift=-30, yshift=40, bordercolor=red, borderwidth=2))
            annotations.append(
                dict(x=(max+min)/2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=blue), xshift=30, yshift=40, bordercolor=blue, borderwidth=2))
            pro = 1 - pro
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, annotations=annotations, title_font_size=22,
                          margin_l=10, margin_r=10, margin_t=90, margin_b=10, font_family='NanumSquare',
                          legend_orientation="h", legend_x=0.25, legend_y=1.25, title_y=0.95)
        fig.update_xaxes(range=[min, max])

        # 최종 누적확률 반환
        return fig, pro, 1 - pro

    @staticmethod
    def bar_chart(t_pro, f_pro, t_text, f_text, variable_name):
        dataframe = pd.DataFrame({
            "상태": [t_text, f_text],
            "확률": [t_pro, f_pro],
            variable_name: [f"{t_text} : {t_pro}", f"{f_text} : {f_pro}"]
        })
        fig = px.bar(dataframe, x="상태", y="확률", color=variable_name, text=variable_name)
        # fig.update_yaxes(visible=False)
        # fig.update_xaxes(visible=False)
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                          font_family='NanumSquare', showlegend=False)
        # fig.show()
        return fig, t_pro


class Density(Social):
    '''
    사회적 요소 - 후보지 고정인구밀도
    '''

    def __init__(self):
        self.file_path = dir.getdir("행정구역 읍면동 주민등록인구.csv")  # 데이터 경로
        self.density_standard = 20_000  # 고정인구 판단 기준
        self.df_density = pd.read_csv(self.file_path, encoding='cp949')
        self.df_density = self.df_density.sort_values(by=["행정구역(시군구)별","행정구역(동읍면)별"],ascending=True).reset_index(drop=True)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_density['인구밀도(km^2)'].mean(),
                                                           self.df_density['인구밀도(km^2)'].std(),
                                                           self.df_density['인구밀도(km^2)'].min(),
                                                           self.df_density['인구밀도(km^2)'].max(),
                                                           self.density_standard,
                                                           False
                                                           )


class FloatingPopulation(Social):
    """
    사회적 요소 - 후보지 유동인구밀도
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 유동인구 데이터.csv")  # 데이터 경로
        self.density_path = dir.getdir("행정구역 읍면동 주민등록인구.csv")
        self.foot_traffic_standard = 400_000  # 유동인구 판단기준
        self.df_foot_traffic = pd.read_csv(self.file_path, encoding='cp949')
        self.df_density = pd.read_csv(self.density_path,encoding='cp949')
        self.foottraffic_col = self.df_foot_traffic.iloc[:,1:-1].columns.tolist()
        self.df_foot_traffic.drop(columns=self.foottraffic_col)
        self.df_foot_traffic.set_index('구군', inplace=True)
        self.df_foot_traffic = Social.advanced_replace(self.df_foot_traffic, '월 평균', '-', r'[^0-9.0-9]')
        self.df_foot_traffic['월 평균'] = self.df_foot_traffic['월 평균'].astype(float)
        self.density = []
        self.population = self.df_foot_traffic['월 평균'].tolist()
        self.area = self.df_density['면적(km^2)'].tolist()
        self.list_p_a = list(zip(self.population,self.area))
        for x,y in self.list_p_a:
            val = x/y
            self.density.append(val)
        self.df_foot_traffic.insert(1,'유동인구밀도(km2당)',self.density)
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_foot_traffic['유동인구밀도(km2당)'].mean(),
                                                           self.df_foot_traffic['유동인구밀도(km2당)'].std(),
                                                           self.df_foot_traffic['유동인구밀도(km2당)'].min(),
                                                           self.df_foot_traffic['유동인구밀도(km2당)'].max(),
                                                           self.foot_traffic_standard,
                                                           False
                                                           )


class EV_per_charger(Social):
    """
    사회적 요소 - 전기차 충전기당 전기차 수
    """

    def __init__(self):
        self.file_path = dir.getdir("연료별_자동차등록대수.csv")  # 데이터 경로
        self.EV_per_charger_standard = 5.1  # 전기차충전기당 전기차수
        self.df_vehicle = pd.read_csv(self.file_path, encoding='cp949')

        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_vehicle['전기차충전소당 전기차 수'].mean(),
                                                                          self.df_vehicle['전기차충전소당 전기차 수'].std(),
                                                                          self.df_vehicle['전기차충전소당 전기차 수'].min(),
                                                                          self.df_vehicle['전기차충전소당 전기차 수'].max(),
                                                                          self.EV_per_charger_standard,
                                                                          False
                                                                          )


class HV_per_charger(Social):
    """
    사회적 요소 - 수소차 충전소당 수소차 수
    """

    def __init__(self):
        self.HV_per_charger_standard = 346.533
        self.HVCS_file_path = dir.getdir("부산 수소차 충전소 현황.csv")  # 데이터 경로
        self.vehicle_file_path = dir.getdir("연료별_자동차등록대수.csv")
        self.df_HVCS = pd.read_csv(self.HVCS_file_path, encoding='cp949')
        self.df_vehicle = pd.read_csv(self.vehicle_file_path, encoding='cp949')
        self.HV_per_charger = self.df_vehicle['수소'].sum() / self.df_HVCS['충전소'].count()
        if self.HV_per_charger >= self.HV_per_charger_standard:
            self.HV_per_charger_pro = 1.0
            self.HV_per_charger_pro_negative = 0
        else:
            self.HV_per_charger_pro = 0
            self.HV_per_charger_pro_negative = 1.0

        self.fig, self.t_pro = Social.bar_chart(self.HV_per_charger_pro, 
                                                self.HV_per_charger_pro_negative,
                                                '적합',
                                                '부적합',
                                                '수소충전소당 수소차 수')
        


class Street_supply(Social):
    """
    사회적 요소 - 후보지 도로보급률 
    """

    def __init__(self):
        self.file_path = dir.getdir("도로보급률.csv")  # 데이터 경로
        self.street_supply_standard = 2.916917867
        self.df_street_supply = pd.read_csv(self.file_path, encoding='cp949')
        self.fig, self.t_pro, self.f_pro = Social.cal_norm(self.df_street_supply['도로보급률'].mean(),
                                                           self.df_street_supply['도로보급률'].std(),
                                                           self.df_street_supply['도로보급률'].min(),
                                                           self.df_street_supply['도로보급률'].max(),
                                                           self.street_supply_standard,
                                                           False
                                                           )


# if __name__ == '__main__':
#     density = Density()
#     floating = FloatingPopulation()
#     ev_per_charger = EV_per_charger()
#     hv_per_charger = HV_per_charger()
#     street_supply = Street_supply()

#     density.fig.show()  # 고정 인구밀도
#     floating.fig.show()  # 유동 인구밀도
#     ev_per_charger.fig.show()  # 전기차 충전소당 전기차 수
#     hv_per_charger.fig.show()  # 수소차 충전소당 수소차 수
#     street_supply.fig.show()  # 도로보급률
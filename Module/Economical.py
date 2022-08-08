import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import init as dir


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
                dict(x=(max + min) / 2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=blue), xshift=-30, yshift=40, bordercolor=blue, borderwidth=2))
            annotations.append(
                dict(x=(max + min) / 2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=red), xshift=30, yshift=40, bordercolor=red, borderwidth=2))
        else:
            fig.add_trace(
                go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='부적합', line=dict(color=red)))
            fig.add_trace(
                go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='적합', line=dict(color=blue)))
            fig.update_yaxes(visible=False)
            annotations = []
            annotations.append(
                dict(x=(max + min) / 2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                     font=dict(size=15, color=red), xshift=-30, yshift=40, bordercolor=red, borderwidth=2))
            annotations.append(
                dict(x=(max + min) / 2, y=norm.pdf(mean, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                     font=dict(size=15, color=blue), xshift=30, yshift=40, bordercolor=blue, borderwidth=2))
            pro = 1 - pro
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, annotations=annotations, title_font_size=22,
                          margin_l=10, margin_r=10, margin_t=90, margin_b=10, font_family='NanumSquare',
                          legend_orientation="h", legend_x=0.25, legend_y=1.25, title_y=0.95)
        fig.update_xaxes(range=[min, max])

        # 최종 누적확률 반환
        return fig, pro, 1 - pro

    @staticmethod
    def cal_maintenance_cost(station_type, operating_rate):
        # 인건비
        if station_type == '복합':
            labor_cost = 40_000_000
        else:
            labor_cost = 60_000_000
        # 전기세
        # 가동률 1%당 162만원
        elec_cost = operating_rate * 1_620_000
        # 카드수수료
        # 가동률 1%당 54만원
        card_cost = operating_rate * 540_000 
        # 기타(장비 교체비용, 품질검사비, 연간 도로점용료, 물품구입비, 공과금 등)
        etc = 30_000_000 + 4_000_000 + 5_000_000 + 10_000_000
        maintenance_cost = labor_cost + elec_cost + card_cost + etc

        return maintenance_cost   

    @staticmethod
    def cal_revenue(charge_time_average, sale_cost, maintenance_cost):
        # 수소연료 평균 공급단가(1kg당)
        hidrogen_cost = 6_000
        # 수소연료 판매 마진(1kg당)
        revenue_per_kg = sale_cost - hidrogen_cost
        # 수소차 1회 평균 수소연료 충전량(kg)
        charge_amount = 3.736 
        # 일평균 판매수익
        day_revenue = revenue_per_kg * charge_amount * charge_time_average 
        year_revenue = day_revenue * 365
        # 수소연료구입비 보조금
        grant = 0

        # 수소연료구입비 보조금 지원금 반영
        diff = year_revenue - maintenance_cost
        
        if diff < 0:
            diff = -diff
            # 기준단가
            grant_cost_standard = sale_cost - (maintenance_cost / charge_amount * charge_time_average * 365)
            # 지원단가 (수소연료공급단가에 기준단가와 차액의 70%)
            grant_cost = (hidrogen_cost - grant_cost_standard) * 0.7
            # 지원금액
            grant = grant_cost * charge_amount * charge_time_average * 365
            # 최대지원금액은 적자의 80%
            if grant > diff * 0.8:
                grant = diff * 0.8
        # 연간수입 + 보조금
        year_revenue = year_revenue + grant
        # 연간수입에 유지보수비용을 뺀 순수익
        diff = year_revenue - maintenance_cost    

        return diff

# EVCS_cost_standard = 35_000_000             # 급속 충전기 설치비용
# # 17_500_000(정부보조금 최대지원가능금액, 출처 한국에너지공단 '2022년 전기차충전서비스산업육성산업) / 0.5(보조율) = 35_000_000
# HVCS_cost_standard = 3_000_000_000    # 수소충전소 구축 비용
# # 1_500_000_000(정부보조금 최대지원가능금액, 출처 환경부'2022년 수소차 보급 및 충전소 설치사업 보조금 업무처리지침 / 0.5 (일반수소충전소 보조율) = 3_000_000_000(구축비용)
# # 4_200_000_000(정부보조금 최대지원가능금액, 출처 환경부'2022년 수소차 보급 및 충전소 설치사업 보조금 업무처리지침 / 0.7 (특수수소충전소 보조율) = 6_000_000_000(구축비용)
# income_standard = 3_600          # 연 평균소득
# maintenance_cost_standard = 100      # 유지비용
# HVCS_income_standard = 0        # 수소충전소 기대수익

class EVCS_cost(Economical):
    """
    경제적 요소 - 전기차 충전기 설치 비용
    """

    def __init__(self):
        self.EVCS_cost_file_path = dir.getdir('전기차 충전기 가격.csv')
        self.EVCS_cost_standard = 35_000_000
        self.df_EVCS_cost = pd.read_csv(self.EVCS_cost_file_path, encoding='cp949')   
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_EVCS_cost[self.df_EVCS_cost['충전기']=='급속']['충전기가격'].mean(),
                                                                self.df_EVCS_cost[self.df_EVCS_cost['충전기']=='급속']['충전기가격'].std(),
                                                                self.df_EVCS_cost[self.df_EVCS_cost['충전기']=='급속']['충전기가격'].min(),
                                                                self.df_EVCS_cost[self.df_EVCS_cost['충전기']=='급속']['충전기가격'].max(),
                                                                self.EVCS_cost_standard,
                                                                True)    


class HVCS_cost(Economical):
    """
    경제적 요소 - 수소 충전소 구축 비용
    """

    def __init__(self):
        self.file_path = dir.getdir("수소 충전소 종류별 구축 비용.csv")  # 데이터 경로
        self.HVCS_cost_standard = 3_000_000_000  # 수소충전소 구축 비용
        self.df_HVCS_cost = pd.read_csv(self.file_path, encoding='cp949')
        self.df_HVCS_cost = self.df_HVCS_cost.set_index('충전소 종류')
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_HVCS_cost['구축 비용'].mean(),
                                                               self.df_HVCS_cost['구축 비용'].std(),
                                                               self.df_HVCS_cost['구축 비용'].min(),
                                                               self.df_HVCS_cost['구축 비용'].max(),
                                                               self.HVCS_cost_standard,
                                                               True
                                                               )


class Income(Economical):
    """
    경제적 요소 - 후보지 평균소득
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 평균소득.csv")  # 데이터 경로
        self.income_standard = 3_600  # 평균소득 기준
        self.df_income = pd.read_csv(self.file_path, encoding='cp949')
        
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(self.df_income['평균소득금액(만)'].mean(),
                                                               self.df_income['평균소득금액(만)'].std(),
                                                               self.df_income['평균소득금액(만)'].min(),
                                                               self.df_income['평균소득금액(만)'].max(),
                                                               self.income_standard,
                                                               False)


class HVCS_income(Economical):
    """
    경제적 요소 - 수소충전소 기대수익
    """

    def __init__(self):
        self.file_path = dir.getdir("부산 수소차 충전소 현황.csv")  # 데이터 경로
        self.HVCS_income_standard = 0  # 수소충전소 기대수익 기준
        self.df_HVCS = pd.read_csv(self.file_path, encoding='cp949')
        self.revenue = []
        for i in range(self.df_HVCS.shape[0]):
            self.maintenance_cost = Economical.cal_maintenance_cost(self.df_HVCS.iloc[i]['충전소 설치방식'],
                                                                    self.df_HVCS.iloc[i]['평균가동률'])
            rev = Economical.cal_revenue(self.df_HVCS.iloc[i]['하루평균충전횟수'], self.df_HVCS.iloc[i]['충전가격'], self.maintenance_cost)
            self.revenue.append(rev)
        self.df_HVCS.insert(15,'연간기대수익',self.revenue)
        self.fig, self.t_pro, self.f_pro = Economical.cal_norm(-110_000_000,
                                                                100_000_000,
                                                                -300_000_000,
                                                                160_000_000,
                                                                self.HVCS_income_standard,
                                                                False)


# if __name__ == '__main__':
#     evcs_cost = EVCS_cost()  # 전기차 충전소 설치 비용
#     hvcs_cost = HVCS_cost()  # 수소차 충전소 설치 비용
#     income = Income()  # 후보지 평균소득
#     hvcs_income = HVCS_income()  # 수소충전소 기대수익

#     evcs_cost.fig.show()
#     hvcs_cost.fig.show()
#     income.fig.show()
#     hvcs_income.fig.show()

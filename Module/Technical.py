import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import norm
import init as dir
from Social import FloatingPopulation, HV_per_charger


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
            "공급방식": [t_text, f_text],
            "확률": [t_pro, f_pro],
            variable_name: [f"{t_text} : {round(t_pro,6)}", f"{f_text} : {round(f_pro,6)}"]
        })
        fig = px.bar(dataframe, x="공급방식", y="확률", color=variable_name, text=variable_name)
        # fig.update_yaxes(visible=False)
        # fig.update_xaxes(visible=False)
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                          font_family='NanumSquare', showlegend=False)
        # fig.show()
        return fig, t_pro
    
    def bar_chart_multi(pro_list, text_list, variable_name):
        dataframe = pd.DataFrame({
            "충전기용량" : ["50kW단독","100kW단독","100kW멀티","200kW단독","200kW멀티"],
            "확률": pro_list,
            variable_name: [f"{text_list[0]} : {pro_list[0]}", 
                            f"{text_list[1]} : {pro_list[1]}",
                            f"{text_list[2]} : {pro_list[2]}",
                            f"{text_list[3]} : {pro_list[3]}",
                            f"{text_list[4]} : {pro_list[4]}"]
        })
        fig = px.bar(dataframe, x = "충전기용량", y="확률", color=variable_name, text=variable_name)
        # fig.update_yaxes(visible=False)
        # fig.update_xaxes(visible=False)
        fig.update_layout({'paper_bgcolor': '#E9EEF6'}, title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                          font_family='NanumSquare', showlegend=False)
        # fig.show()
        return fig, pro_list


class Charge_capacity(Technical):
    '''
    기술적 요소 - 전기차 충전기 용량
    '''

    def __init__(self):
        self.file_path = dir.getdir("전기차충전소 리스트.csv")  # 데이터 경로
        self.df_EVCS = pd.read_csv(self.file_path, encoding='cp949')
        self.df_EVCS_standard = self.df_EVCS[self.df_EVCS['충전기타입']=='AC완속'].reset_index(drop=True)
        self.df_EVCS_fast = self.df_EVCS[self.df_EVCS['충전기타입']!='AC완속'].reset_index(drop=True)
        self.charge_capacity = self.df_EVCS_fast.groupby('충전용량')

        self.capacity_50only_pro = self.df_EVCS_fast[self.df_EVCS_fast['충전용량']=='50kW단독']['운영기관'].count() / self.df_EVCS_fast['충전용량'].shape[0]
        self.capacity_100only_pro = self.df_EVCS_fast[self.df_EVCS_fast['충전용량']=='100kW단독']['운영기관'].count() / self.df_EVCS_fast['충전용량'].shape[0]
        self.capacity_100multi_pro = self.df_EVCS_fast[self.df_EVCS_fast['충전용량']=='100kW멀티']['운영기관'].count() / self.df_EVCS_fast['충전용량'].shape[0]
        self.capacity_200only_pro = self.df_EVCS_fast[self.df_EVCS_fast['충전용량']=='200kW단독']['운영기관'].count() / self.df_EVCS_fast['충전용량'].shape[0]
        self.capacity_200multi_pro = self.df_EVCS_fast[self.df_EVCS_fast['충전용량']=='200kW멀티']['운영기관'].count() / self.df_EVCS_fast['충전용량'].shape[0]
        self.pro_list = [round(self.capacity_50only_pro,6),
                         round(self.capacity_100only_pro,6),
                         round(self.capacity_100multi_pro,6),
                         round(self.capacity_200only_pro,6),
                         round(self.capacity_200multi_pro,6)]
        self.text_list = ['50kW단독','100kW단독','100kW멀티','200kW단독','200kW멀티']
        self.fig, self.pro = Technical.bar_chart_multi(self.pro_list, self.text_list, '충전기 용량')


class HVCS_type(Technical):
    '''
    기술적 요소 - 수소연료 공급방식
    '''

    def __init__(self):
        self.HVCS = HV_per_charger()
        self.df_HVCS = self.HVCS.df_HVCS
        self.HVCS_type_tube_pro = self.df_HVCS[self.df_HVCS['공급방식']=='튜브트레일러']['충전소'].count() / self.df_HVCS['충전소'].shape[0]
        self.HVCS_type_reformation_pro = self.df_HVCS[self.df_HVCS['공급방식']=='천연가스개질']['충전소'].count() / self.df_HVCS['충전소'].shape[0]
        self.pro_list = [self.HVCS_type_tube_pro, self.HVCS_type_reformation_pro]
        self.fig, self.t_pro = Technical.bar_chart(self.HVCS_type_tube_pro, self.HVCS_type_reformation_pro,"튜브트레일러","천연가스개질",'수소연료 공급방식')

class Maximum_charge(Technical):
    '''
    기술적 요소 - 수소충전소당 공급 가능 차량수
    '''

    def __init__(self):
        self.HVCS = HV_per_charger()
        self.df_HVCS = self.HVCS.df_HVCS
        self.maximum_charge_standard = 45.3
        self.fig, self.t_pro, self.f_pro = Technical.cal_norm(self.df_HVCS['최대 충전 수소차수'].mean(),
                                                              self.df_HVCS['최대 충전 수소차수'].std(),
                                                              self.df_HVCS['최대 충전 수소차수'].mean()-3*self.df_HVCS['최대 충전 수소차수'].std(),
                                                              self.df_HVCS['최대 충전 수소차수'].max()+3*self.df_HVCS['최대 충전 수소차수'].std(),
                                                              self.maximum_charge_standard,
                                                              False)

# if __name__ == '__main__':
#     charge_capacity = Charge_capacity()   # 충전기 용량
#     hvcs_type = HVCS_type()               # 수소연료 공급방식
#     maximum_charge = Maximum_charge()     # 수소충전소당 공급가능 차량수

#     charge_capacity.fig.show()
#     hvcs_type.fig.show()
#     maximum_charge.fig.show()
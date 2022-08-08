import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
import init as dir


class Environment:
    '''
    환경요소 모델링
    '''

    air_pollution_file_path = dir.getdir("대기오염시도별실시간측정정보(환경부).csv")
    df_air_pollution = pd.read_csv(air_pollution_file_path, encoding='cp949').interpolate(method='pad')
    df_air_pollution = df_air_pollution[df_air_pollution['sidoName'] == '부산']
    df_air_pollution.reset_index(drop=True, inplace=True)


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
    def pretreatment(df):
        '''
        데이터 프레임 특정 열 삭제
        :param df: 대상 데이터 프레임
        :return: 삭제 처리된 데이터 프레임
        '''
        col = df.iloc[:, 2:-1].columns.tolist()
        df.drop(columns=col, inplace=True)
        # return df

    @staticmethod
    def cal_norm(mean, std, min, max, value, affect):
        """
        정규분포 출력 메서드
        :param mean: 평균값
        :param std: 표준편차 값
        :param min: 데이터의 최소값
        :param max: 데이터의 최대값
        :param value: 데이터의 측정값
        :return: 정규분포 객체, 참.거짓 확률
        """

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
        # value까지의 누적확률에서 min까지의 누적확률을 뺌

        # 최종 누적확률 반환
        return fig, pro, 1 - pro


class Ozone(Environment):
    """
    환경적 요소 - 오존 대기오염도
    """

    def __init__(self):
        self.o3_standard = 0.003
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            Environment.df_air_pollution['o3Value'].mean(),
            Environment.df_air_pollution['o3Value'].std(),
            Environment.df_air_pollution['o3Value'].min(),
            Environment.df_air_pollution['o3Value'].max(),
            self.o3_standard,
            False
        )


class No2(Environment):
    """
    환경적 요소 - 이산화질소 대기오염도
    """

    def __init__(self):
        self.no2_standard = 0.012
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            Environment.df_air_pollution['no2Value'].mean(),
            Environment.df_air_pollution['no2Value'].std(),
            Environment.df_air_pollution['no2Value'].min(),
            Environment.df_air_pollution['no2Value'].max(),
            self.no2_standard,
            False
        )


class Co(Environment):
    """
    환경적 요소 - 일산화탄소 대기오염도
    """

    def __init__(self):
        self.co_standard = 0.3
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            Environment.df_air_pollution['coValue'].mean(),
            Environment.df_air_pollution['coValue'].std(),
            Environment.df_air_pollution['coValue'].min(),
            Environment.df_air_pollution['coValue'].max(),
            self.co_standard,
            False
        )


class FineDust_pm25(Environment):
    '''
    환경적 요소 - 미세먼지 pm2.5 대기오염도
    '''

    def __init__(self):
        self.pm25_standard = 10
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            Environment.df_air_pollution['pm25Value'].mean(),
            Environment.df_air_pollution['pm25Value'].std(),
            Environment.df_air_pollution['pm25Value'].min(),
            Environment.df_air_pollution['pm25Value'].max(),
            self.pm25_standard,
            False
        )


class FineDust_pm10(Environment):
    '''
     환경적 요소 - 미세먼지 pm10 대기오염도
     '''

    def __init__(self):
        self.pm10_standard = 15
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            Environment.df_air_pollution['pm10Value'].mean(),
            Environment.df_air_pollution['pm10Value'].std(),
            Environment.df_air_pollution['pm10Value'].min(),
            Environment.df_air_pollution['pm10Value'].max(),
            self.pm10_standard,
            False
        )


# if __name__ == '__main__':
#     ozone = Ozone()  # 오존 데이터
#     print(f"적합: {ozone.t_pro}, 부적합: {ozone.f_pro}")  # 오존 확률

#     no2 = No2() # 이산화질소 데이터
#     print(f"적합: {no2.t_pro}, 부적합: {no2.f_pro}")  # 이산화질소 확률

#     co = Co() # 일산화탄소 데이터
#     print(f"적합: {co.t_pro}, 부적합: {co.f_pro}")  # 이산화질소 확률

#     pm25 = FineDust_pm25()  # 미세먼지 pm2.5
#     print(f"적합: {pm25.t_pro}, 부적합: {pm25.f_pro}")  # 미세먼지 pm2.5 확률

#     pm10 = FineDust_pm10()  # 미세먼저 pm10
#     print(f"적합: {pm10.t_pro}, 부적합: {pm10.f_pro}")  # 미세먼지 pm10 확률
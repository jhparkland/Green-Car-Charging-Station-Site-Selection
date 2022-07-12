import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
from Module import init as dir


def pretreatment(df):
    '''
    데이터 프레임 특정 열 삭제
    :param df: 대상 데이터 프레임
    :return: 삭제 처리된 데이터 프레임
    '''
    col = df.iloc[:, 2:-1].columns.tolist()
    df.drop(columns=col, inplace=True)
    # return df


class Environment:
    '''
    환경요소 모델링
    '''

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
    def cal_norm(mean, std, min, max, value):
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
        # 구간 사이에 색을 채움
        fig.add_trace(go.Scatter(x=cum_a, y=norm.pdf(cum_a, mean, std), fill='tozeroy', name='적합', text=pro,
                                 line=dict(color=blue)))
        fig.add_trace(go.Scatter(x=cum_b, y=norm.pdf(cum_b, mean, std), fill='tozeroy', name='부적합', text=pro,
                                 line=dict(color=red)))
        fig.update_yaxes(visible=False)
        annotations = []
        annotations.append(dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(pro, 3),
                                font=dict(size=15, color=blue), xshift=-40, yshift=-100, bordercolor=blue,
                                borderwidth=2))
        annotations.append(
            dict(x=value, y=norm.pdf(value, loc=mean, scale=std), showarrow=False, text=round(1 - pro, 3),
                 font=dict(size=15, color=red), xshift=40, yshift=-100, bordercolor=red, borderwidth=2))
        fig.update_layout(annotations=annotations)
        # value까지의 누적확률에서 min까지의 누적확률을 뺌

        # 최종 누적확률 반환
        return fig, pro, 1 - pro


class Ozone(Environment):
    """
    환경적 요소 - 오존 대기오염도
    """

    def __init__(self):
        self.file_path = dir.getdir("오존 대기오염도.csv")
        self.df_ozone = pd.read_csv(self.file_path, encoding='cp949')
        pretreatment(self.df_ozone)
        Environment.advanced_replace(self.df_ozone, self.df_ozone.iloc[:, 2:].columns.tolist(), '-',
                                     r'[^0-9.0-9]')
        Environment.ChangeType(self.df_ozone, '2021.07', 'float')
        self.busan_ozone = self.df_ozone[self.df_ozone['구분(2)'] == '부산광역시'].loc[2, '2021.07']
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            self.df_ozone.iloc[:, 2].mean(),
            self.df_ozone.iloc[:, 2].std(),
            self.df_ozone.iloc[:, 2].min(),
            self.df_ozone.iloc[:, 2].max(),
            self.busan_ozone
        )


class So2(Environment):
    """
    환경적 요소 - 아황산가스 대기오염도
    """

    def __init__(self):
        self.file_path = dir.getdir('아황산가스 대기오염도.csv')
        self.df_so2 = pd.read_csv(self.file_path, encoding='cp949')
        pretreatment(self.df_so2)
        Environment.advanced_replace(self.df_so2, self.df_so2.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
        Environment.ChangeType(self.df_so2, '2021.07', 'float')
        self.busan_so2 = self.df_so2[self.df_so2['구분(2)'] == '부산광역시'].loc[2, '2021.07']
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            self.df_so2.iloc[:, 2].mean(),
            self.df_so2.iloc[:, 2].std(),
            self.df_so2.iloc[:, 2].min(),
            self.df_so2.iloc[:, 2].max(),
            self.busan_so2
        )


class No2(Environment):
    """
    환경적 요소 - 이산화질소 대기오염도
    """

    def __init__(self):
        self.file_path = dir.getdir('이산화질소 대기오염도.csv')
        self.df_no2 = pd.read_csv(self.file_path, encoding='cp949')
        pretreatment(self.df_no2)
        Environment.advanced_replace(self.df_no2, self.df_no2.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
        Environment.ChangeType(self.df_no2, '2021.07', 'float')
        self.busan_no2 = self.df_no2[self.df_no2['구분(2)'] == '부산광역시'].loc[2, '2021.07']
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            self.df_no2.iloc[:, 2].mean(),
            self.df_no2.iloc[:, 2].std(),
            self.df_no2.iloc[:, 2].min(),
            self.df_no2.iloc[:, 2].max(),
            self.busan_no2
        )


class FineDust_pm25(Environment):
    '''
    환경적 요소 - 미세먼지 pm2.5 대기오염도
    '''

    def __init__(self):
        self.file_path = dir.getdir('미세먼지2.5.csv')
        self.df_pm25 = pd.read_csv(self.file_path, encoding='cp949')
        pretreatment(self.df_pm25)
        Environment.advanced_replace(self.df_pm25, self.df_pm25.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
        Environment.ChangeType(self.df_pm25, '2021.07', 'float')
        self.busan_pm25 = self.df_pm25[self.df_pm25['구분(2)'] == '부산광역시'].loc[2, '2021.07']
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            self.df_pm25.iloc[:, 2].mean(),
            self.df_pm25.iloc[:, 2].std(),
            self.df_pm25.iloc[:, 2].min(),
            self.df_pm25.iloc[:, 2].max(),
            self.busan_pm25
        )


class FineDust_pm10(Environment):
    '''
     환경적 요소 - 미세먼지 pm10 대기오염도
     '''

    def __init__(self):
        self.file_path = dir.getdir('미세먼지10.csv')
        self.df_pm10 = pd.read_csv(self.file_path, encoding='cp949')
        pretreatment(self.df_pm10)
        Environment.advanced_replace(self.df_pm10, self.df_pm10.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
        Environment.ChangeType(self.df_pm10, '2021.07', 'float')
        self.busan_pm10 = self.df_pm10[self.df_pm10['구분(2)'] == '부산광역시'].loc[2, '2021.07']
        self.fig, self.t_pro, self.f_pro = Environment.cal_norm(
            self.df_pm10.iloc[:, 2].mean(),
            self.df_pm10.iloc[:, 2].std(),
            self.df_pm10.iloc[:, 2].min(),
            self.df_pm10.iloc[:, 2].max(),
            self.busan_pm10
        )


if __name__ == '__main__':
    ozone = Ozone()  # 오존 데이터
    print(f"적합: {ozone.t_pro}, 부적합: {ozone.f_pro}")  # 오존 확률

    so2 = So2()  # 아황산가스 데이터
    print(f"적합: {so2.t_pro}, 부적합: {so2.f_pro}")  # 아황산가스 확률

    pm25 = FineDust_pm25()  # 미세먼지 pm2.5
    print(f"적합: {pm25.t_pro}, 부적합: {pm25.f_pro}")  # 미세먼지 pm2.5 확률

    pm10 = FineDust_pm10()  # 미세먼저 pm10
    print(f"적합: {pm10.t_pro}, 부적합: {pm10.f_pro}")  # 미세먼지 pm10 확률

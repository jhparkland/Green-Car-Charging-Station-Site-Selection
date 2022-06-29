import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm
from Module import init as dir

class Environment:
    '''
    환경요소 모델링
    '''
    def __init(self):
        pass

    def advanced_replace(self, df, col, str, regex):
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

    def describe(self, df):
        '''
        데이터 요약 통계 출력
        :param df: 대상 DataFrame
        :return: 통계 DataFrame
        '''
        return df.describe()

    def ChangeType(self,df, col_name, type):
        '''
        데이터 프레임 특정 컬럼 타입 변경
        :param df: 대상 DataFrame
        :param col_name: 컬럼 이름
        :return:
        '''
        df[col_name] = df[col_name].astype(type)
        return  df

    def cal_norm(slef, mean, std, min, max, value):
        '''
        정규분포에서 value에 대한 누적확률 시각화
        mean: 평균값
        std: 표준편차
        min: 관측된 데이터의 최솟값
        max: 관측된 데이터의 최댓값
        value: 누적확률을 구하고자 하는 데이터의 측정값
        '''

        # x축 설정
        x = np.linspace(min, max, 100)
        fig = go.Figure()
        # y축이 확률밀도로 구성된 정규분포
        fig.add_trace(go.Scatter(x=x, y=norm.pdf(x, loc=mean, scale=std), mode='lines+markers'))
        # 확률 값을 구할 특정 구간의 범위 설정
        cum = np.linspace(min, value, 100)
        # 구간 사이에 색을 채움
        fig.add_trace(go.Scatter(x=cum, y=norm.pdf(cum, mean, std), fill='tozeroy'))
        # value까지의 누적확률에서 min까지의 누적확률을 뺌
        pro = norm(mean, std).cdf(value) - norm(mean, std).cdf(min)

        # 최종 누적확률 반환
        return fig

class Ozone(Environment):
    '''
    환경적 요소 - 오존 대기오염도
    '''
    def __init__(self):
        self.file_path = dir.getdir("오존 대기오염도.csv")

    def  pretreatment(self, df):
        col = df.iloc[:, 2:-1].columns.tolist()
        df.drop(columns=col, inplace=True)
        return df

class So2(Environment):
    '''
    환경적 요소 - 아황산가스 대기오염도
    '''
    def __init__(self):
        self.file_path = dir.getdir('아황산가스 대기오염도.csv')

    def pretreatment(self, df):
        col = df.iloc[:, 2:-1].columns.tolist()
        df.drop(columns=col, inplace=True)
        return df

# if __name__ == '__main__':
#     ozone = Ozone()
#     df_ozone = pd.read_csv(ozone.file_path, encoding='cp949')
#     df_ozone = ozone.pretreatment(df_ozone)
#     df_ozone = ozone.advanced_replace(df_ozone, df_ozone.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
#     df_ozone = ozone.ChangeType(df_ozone, '2021.07')
#     ozone_describe = ozone.describe(df_ozone)
#     busan_ozone = df_ozone[df_ozone['구분(2)'] == '부산광역시'].loc[2, '2021.07']

#     fig_ozone = ozone.cal_norm(df_ozone.iloc[:, 2].mean(),
#                                df_ozone.iloc[:, 2].std(),
#                                df_ozone.iloc[:, 2].min(),
#                                df_ozone.iloc[:, 2].max(),
#                                busan_ozone
                            #    )

    #====================================================================================================================
    # so2 = So2()
    # df_so2 = pd.read_csv(so2.file_path, encoding='cp949')
    # df_so2 = so2.pretreatment(df_so2)
    # df_so2 = so2.advanced_replace(df_so2, df_so2.iloc[:, 2:].columns.tolist(), '-', r'[^0-9.0-9]')
    # df_so2 = so2.ChangeType(df_so2, '2021.07')
    # so2_describe = so2.describe(df_so2)
    # busan_so2 = df_so2[df_so2['구분(2)'] == '부산광역시'].loc[2, '2021.07']
    # fig_so2 = so2.cal_norm(df_so2.iloc[:, 2].mean(),
    #                            df_so2.iloc[:, 2].std(),
    #                            df_so2.iloc[:, 2].min(),
    #                            df_so2.iloc[:, 2].max(),
    #                            busan_so2
    #                            )
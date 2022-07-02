import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import osmnx as ox
import numpy as np
import networkx as nx
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go

def temp():
    ozone_file_path = "C:\\Users\\SAMSUNG\\Desktop\\Green-Car-Charging-Station-Site-Selection\\Data\\오존_월별_도시별_대기오염도.csv"
    df_ozone = pd.read_csv(ozone_file_path, encoding='cp949')
    ozen_col =  df_ozone.iloc[:,2:-1].columns.tolist()
    df_ozone.drop(columns=ozen_col, inplace=True)

    return df_ozone, ozen_col



def advanced_replace(df, col, str, regex):
    '''
    DataFrame 특정 열의 특수문자 제거
    :param df: 대상 DataFrame
    :param col: column
    :param str: 제거할 특수 문자.
    :param regex: 적용할 정규표현식
    :return:
    '''
    df[col] = df[col].replace(str,0)
    df[col] = df[col].replace(to_replace=regex, value=r'', regex=True)
    return df

# 프론트 코드



def temp2(df_ozone):
    df_ozone['2021.07'] = df_ozone['2021.07'].astype(float)
    df_ozone.info()

    return df_ozone


def show_norm(mean,std,min,max):
     '''
     정규분포 함수를 matplotlib을 통해 시각화
     mean: 평균값
     std: 표준편차
     min: 관측된 데이터의 최솟값
     max: 관측된 데이터의 최댓값
     '''
     
     # x값 설정(min에서 max까지 unit만큼씩 증가하는 x)
     x = np.linspace(min,max,100)
     # y값은 평균이 mean이고 표준편차가 std인 확률밀도함수
     fig = px.line(x=x,y=norm.pdf(x,loc=mean,scale=std))
     fig.show()



# 프론트 코드



def cal_norm(mean,std,min,max,value):
     '''
     정규분포에서 value에 대한 누적확률 구하기
     mean: 평균값
     std: 표준편차
     min: 관측된 데이터의 최솟값
     max: 관측된 데이터의 최댓값
     value: 누적확률을 구하고자 하는 데이터의 측정값
     '''
   
     # x축 설정
     x = np.linspace(min,max,100)
     fig = go.Figure()
     # y축이 확률밀도로 구성된 정규분포 
     fig.add_trace(go.Scatter(x=x,y=norm.pdf(x,loc=mean,scale=std),mode='lines'))
     # 확률 값을 구할 특정 구간의 범위 설정
     cum = np.linspace(min,value,100)
     # 구간 사이에 색을 채움
     fig.add_trace(go.Scatter(x=cum,y=norm.pdf(cum,mean,std), fill = 'tozeroy'))
     # value까지의 누적확률에서 min까지의 누적확률을 뺌
     pro = norm(mean,std).cdf(value)-norm(mean,std).cdf(min)
     fig.show()

     # 최종 누적확률 반환
     #return pro

# 프론트 코드    

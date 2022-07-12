import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import osmnx as ox
import networkx as nx
import numpy as np
from scipy.stats import norm
import plotly.express as px
import plotly.graph_objects as go

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

def show_norm(mean,std,min,max):
     '''
     정규분포 함수를 matplotlib을 통해 시각화
     mean: 평균값
     std: 표준편차
     min: 관측된 데이터의 최솟값
     max: 관측된 데이터의 최댓값
     '''
     min = min - std
     # x값 설정(min에서 max까지 unit만큼씩 증가하는 x)
     x = np.linspace(min,max,100)
     # y값은 평균이 mean이고 표준편차가 std인 확률밀도함수
     fig = px.line(x=x,y=norm.pdf(x,loc=mean,scale=std))
     
     return fig # 이거 중요함 fig.show()하면 새로운 웹사이트 만들어져서 그냥 fig자체를 리턴해줘야함.
     
def cal_norm(mean,std,min,max,value):
     '''
     정규분포에서 value에 대한 누적확률 구하기
     mean: 평균값
     std: 표준편차
     min: 관측된 데이터의 최솟값
     max: 관측된 데이터의 최댓값
     value: 누적확률을 구하고자 하는 데이터의 측정값
     '''
     min = min - std
     red ='rgb(239,85,59)'
     blue = 'rgb(100,110,250)'
     fig = go.Figure()
     
     # 확률 값을 구할 특정 구간의 범위 설정
     cum_a = np.linspace(min,value,100)
     cum_b = np.linspace(value,max,100)
     
     pro = norm(mean,std).cdf(value)-norm(mean,std).cdf(min).round(3)
     # 구간 사이에 색을 채움
     fig.add_trace(go.Scatter(x=cum_a,y=norm.pdf(cum_a,mean,std), fill = 'tozeroy',name='적합',text=pro,line=dict(color=blue)))
     fig.add_trace(go.Scatter(x=cum_b,y=norm.pdf(cum_b,mean,std), fill = 'tozeroy',name='부적합',text=pro,line=dict(color=red)))
     annotations =[]
     annotations.append(dict(x=value, y=norm.pdf(value,loc=mean,scale=std), showarrow=False, text=round(pro,3), font=dict(size=15,color=blue), xshift=-40, yshift=-100, bordercolor=blue,borderwidth=2))
     annotations.append(dict(x=value, y=norm.pdf(value,loc=mean,scale=std), showarrow=False, text=round(1-pro,3),font=dict(size=15,color=red),xshift=40, yshift=-100, bordercolor=red,borderwidth=2))
     fig.update_layout(annotations=annotations)
     
     return fig # 이거 중요함 fig.show()하면 새로운 웹사이트 만들어져서 그냥 fig자체를 리턴해줘야함.

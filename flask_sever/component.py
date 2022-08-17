from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

import dash_leaflet as dl
import dash_leaflet.express as dlx

elec_marker_data = [
    dict(name="네오스포밑 주차장", lat=35.1538771, lon=129.0575931),
    dict(name="적십자회관 주차장", lat=35.16434005, lon=129.0712629),
    dict(name="평화시장 주차장", lat=35.1464909, lon=129.0602635),
    dict(name="백양순환로 시간제 노상주차장", lat=35.1715941, lon=129.0285127),
    dict(name="테마공원로 시간제 노상주차장", lat=35.15948745, lon=129.021564),
    dict(name="가남공영(주거지전용)주차장", lat=35.14598655, lon=129.034164),
    dict(name="범천4동 소규모공동주차장", lat=35.14895515, lon=129.0491135),
    dict(name="금호천지맨션 뒤 주차장", lat=35.17464865, lon=129.0347596),
    dict(name="서면교회옆 주차장", lat=35.15891935, lon=129.0419288),
    dict(name="부암로타리 주차장", lat=35.16375735, lon=129.0490284),
    dict(name="가야중복도로 공영주차장", lat=35.1454684, lon=129.0263261),
    dict(name="전포동 서전로 주차장", lat=35.1567898, lon=129.0652592),
    dict(name="경남공고 뒤 주차장", lat=35.1543182, lon=129.0711925),
    dict(name="가야중복도로 주차장", lat=35.1508294, lon=129.028627),
    dict(name="가야공원 주차장", lat=35.1492037, lon=129.030028),
    dict(name="주례초등학교공영노외주차장", lat=35.14193405, lon=129.0187571),
    dict(name="부전시장 화물하역 주차구역", lat=35.16452825, lon=129.0590653),
    dict(name="초읍새싹길 주거지전용주차장", lat=35.1791327, lon=129.0489923),
    dict(name="광명3로 주거지전용주차장", lat=35.17289515, lon=129.0756074)
]
elec_geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in elec_marker_data])
elec_list = {"네오스포밑 주차장": [77, 52, 47, 65, 52],
             "적십자회관 주차장": [45, 68, 45, 67, 55],
             "평화시장 주차장": [92, 63, 38, 45, 65],
             "백양순환로 시간제 노상주차장": [51, 63, 74, 43, 67],
             "테마공원로 시간제 노상주차장": [60, 63, 86, 38, 73],
             "가남공영(주거지전용)주차장": [47, 62, 77, 38, 61],
             "범천4동 소규모공동주차장": [64, 46, 59, 82, 48],
             "금호천지맨션 뒤 주차장": [72, 69, 48, 68, 42],
             "서면교회옆 주차장": [47, 68, 78, 49, 51],
             "부암로타리 주차장": [44, 48, 36, 51, 61],
             "가야중복도로 공영주차장": [68, 55, 49, 75, 50],
             "전포동 서전로 주차장": [61, 75, 51, 79, 68],
             "경남공고 뒤 주차장": [68, 55, 34, 41, 53],
             "가야중복도로 주차장": [78, 44, 24, 65, 50],
             "가야공원 주차장": [43, 52, 74, 63, 61],
             "주례초등학교공영노외주차장": [62, 59, 89, 60, 74],
             "부전시장 화물하역 주차구역": [38, 57, 69, 57, 54],
             "초읍새싹길 주거지전용주차장": [85, 38, 41, 72, 60],
             "광명3로 주거지전용주차장": [73, 60, 39, 49, 57]}

hydro_marker_data = [
    dict(name="개인택시신공항충전소", lat=35.19866936, lon=128.9665944),
    dict(name="부산공항LPG충전소", lat=35.14906405, lon=128.951891, ),
    dict(name="신항만에너지", lat=35.11294738, lon=128.8752599),
    dict(name="(주)지원네트웍스 부산강서LPG충전소", lat=35.21250666, lon=128.9625717),
    dict(name="신명지에너지", lat=35.09755417, lon=128.9273511),
    dict(name="르노삼성자동차(주)", lat=35.09540802, lon=128.8832153),
    dict(name="(주)배성에너지 대저충전소", lat=35.20628616, lon=128.9748913),
    dict(name="죽림LPG충전소", lat=35.20073559, lon=128.8934617),
    dict(name="가락충전소", lat=35.20884705, lon=128.8901483)
]
hydro_geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in hydro_marker_data])
hydro_list = {"개인택시신공항충전소": [37, 58, 78, 60, 72],
              "부산공항LPG충전소": [68, 48, 67, 51, 60],
              "신항만에너지": [73, 89, 31, 67, 41],
              "(주)지원네트웍스 부산강서LPG충전소": [64, 38, 50, 41, 49],
              "신명지에너지": [37, 34, 89, 56, 48],
              "르노삼성자동차(주)": [64, 64, 59, 28, 41],
              "(주)배성에너지 대저충전소": [76, 78, 52, 63, 68],
              "죽림LPG충전소": [62, 42, 65, 78, 61],
              "가락충전소": [70, 38, 58, 59, 59]}


class Main_Component:
    @staticmethod
    def mark_chart(**df):
        fig_1 = px.pie(df["전기차"], values='Amount', names='기준')  # 전기차 파이차트(values: 비율, names: 영역명)
        fig_1.update_yaxes(visible=False)
        fig_2 = px.pie(df["수소차"], values='Amount', names='기준')  # 수소차 파이차트
        fig_2.update_yaxes(visible=False)
        # 확률차트 생성
        fig1 = px.bar(df["경제적"], x="경제적", y="적합확률", color="경제적 요소",
                      text="경제적 요소")  # 경제적 확률차트(x: x축 라벨명, y: 값, color: 막대 색)
        fig1.update_yaxes(visible=False)
        fig1.update_xaxes(visible=False)
        fig2 = px.bar(df["사회적"], x="사회적", y="적합확률", color="사회적 요소", text="사회적 요소")  # 사회적 확률차트
        fig2.update_yaxes(visible=False)
        fig2.update_xaxes(visible=False)
        fig3 = px.bar(df["환경적"], x="환경적", y="적합확률", color="환경적 요소", text="환경적 요소")  # 환경적 확률차트
        fig3.update_yaxes(visible=False)
        fig3.update_xaxes(visible=False)
        fig4 = px.bar(df["기술적"], x="기술적", y="적합확률", color="기술적 요소", text="기술적 요소")  # 기술적 확률차트
        fig4.update_yaxes(visible=False)
        fig4.update_xaxes(visible=False)
        hy_fig1 = px.bar(df["수소_경제적"], x="경제적", y="적합확률", color="경제적 요소", text="경제적 요소")
        hy_fig1.update_yaxes(visible=False)
        hy_fig1.update_xaxes(visible=False)
        hy_fig2 = px.bar(df["수소_사회적"], x="사회적", y="적합확률", color="사회적 요소", text="사회적 요소")
        hy_fig2.update_yaxes(visible=False)
        hy_fig2.update_xaxes(visible=False)
        hy_fig3 = px.bar(df["수소_환경적"], x="환경적", y="적합확률", color="환경적 요소", text="환경적 요소")
        hy_fig3.update_yaxes(visible=False)
        hy_fig3.update_xaxes(visible=False)
        hy_fig4 = px.bar(df["수소_기술적"], x="기술적", y="적합확률", color="기술적 요소", text="기술적 요소")
        hy_fig4.update_yaxes(visible=False)
        hy_fig4.update_xaxes(visible=False)
        e_final_fig = px.bar(df['전기차 최종 부지선정'], x='최종 부지선정', y='적합확률', color='최종 부지선정 요소', text='최종 부지선정 요소')
        e_final_fig.update_yaxes(visible=False)
        e_final_fig.update_yaxes(visible=False)
        h_final_fig = px.bar(df['수소차 최종 부지선정'], x='최종 부지선정', y='적합확률', color='최종 부지선정 요소', text='최종 부지선정 요소')
        h_final_fig.update_yaxes(visible=False)
        h_final_fig.update_yaxes(visible=False)

        return fig_1, fig_2, fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4, e_final_fig, h_final_fig

    @staticmethod
    def chart_layout(**figs):
        return [figs["fig1"].update_layout({  # 경제적 차트(임시)
            'paper_bgcolor': '#E9EEF6',  # 배경색
        }, title_text="전기-경제적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
            font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
            figs["fig2"].update_layout({  # 사회적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-사회적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["fig3"].update_layout({  # 환경적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-환경적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["fig4"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-기술적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            figs["hy_fig1"].update_layout({  # 수소 - 경제적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-경제적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig2"].update_layout({  # 수소 - 사회적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-사회적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig3"].update_layout({  # 수소 - 환경적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-환경적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig4"].update_layout({  # 수소 - 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-기술적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            # 파이차트 배경색
            figs["fig_1"].update_layout({  # 전기차 파이차트(임시)
                'paper_bgcolor': '#E9EEF6',  # 배경색
            }, title_text='전기차', title_y=0.8, title_font_size=22,  # 제목 설정
                margin_l=10, margin_r=10, margin_b=20, margin_t=40, legend_y=1.17,  # 좌우위아래 여유공간
                legend_x=0.1, legend_orientation="h", legend_font_size=20, font_family='NanumSquare', font_size=20),
            # 범례 설정
            figs["fig_2"].update_layout({  # 수소차 파이차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text='수소차', title_y=0.8, title_font_size=22,
                margin_l=10, margin_r=10, margin_b=20, margin_t=40, legend_y=1.17,
                legend_x=0.1, legend_orientation="h", legend_font_size=20, font_family='NanumSquare', font_size=20),

            figs["e_final_fig"].update_layout({  # 최종확률
                'paper_bgcolor': '#E9EEF6',
            }, title_text="최종 부지선정", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            figs["h_final_fig"].update_layout({  # 최종확률
                'paper_bgcolor': '#E9EEF6',
            }, title_text="최종 부지선정", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            # 환경적 - 오존, 일산화탄소, 이산화 질소, 미세먼지
            figs["ozone"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="오존 대기오염도"),
            figs["so2"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="아황산가스 대기오염도", title_font_size=18),
            figs["no2"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="이산화질소 대기오염도", title_font_size=18),
            figs["pm25"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="미세먼지-pm25"),
            figs["pm10"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="미세먼지-pm10"),
            # 사회적 - 고정인구, 월 평균 유동인구, 충전소당 친환경 차량수, 도로 보급률
            figs["population"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="고정인구 인구밀도"),
            figs["f_population"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="월 평균 유동인구 인구밀도", title_font_size=16),
            figs["eleFig"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="충전소당 전기차 차량 수", title_font_size=16),
            figs["hydFig"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="충전소당 수소차 차량 수", title_font_size=16),
            figs["intersection"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="도로 보급률"),
            # 경제적 - 수소: 수소 충전소 기대 수익, 충전기 구축 비용, 후보지 평균 소득
            #         전기: 충전기 구축 비용, 후보지 평균 소득
            figs["elec_charger_cost"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="충전기 구축 비용"),
            figs["hydro_charger_cost"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="충전기 구축 비용"),
            figs["land_cost"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="후보지 평균 소득"),
            figs["hydro_expected_income"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="수소 충전소 기대 수익", title_font_size=18),
            # 기술적 - 수소: 수소 연료 공급 방식, 충전소당 공급 가능 차량 수
            #         전기: 전기 충전기 용량
            figs["elec_capacity"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="전기 충전기 용량"),
            figs["hydro_supply_car"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="충전소 당 공급 가능 차량 수",
                                                   title_font_size=14),
            figs["hydro_supply_fuel"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="수소차 연료 공급 방식",
                                                    title_font_size=18),
        ]

    @staticmethod
    def drawing_chart(**figs):
        '''
        대시보드 차트 시각화 메서드
        :param args: fig 객체
        :return: html
        '''
        return html.Div(className='def_chart', children=[
            html.Div(id='hydro-selected', style={'display': 'none'}),
            html.Div(id='hydro-prev', style={'display': 'none'}),
            html.Div(id='elec-prev', style={'display': 'none'}),
            html.Div(id='hydro-prev-second', style={'display': 'none'}),
            html.Div(id='elec-prev-second', style={'display': 'none'}),
            dbc.Row([
                dbc.Col([
                    html.H4("상위요인 중요도", className="d-none d-lg-block d-xl-none c_name_1_2"),
                    html.H4("상위요인 중요도", className="d-none d-xl-block c_name_1_2")
                ]),
                dbc.Col([
                    html.H4("상위요인 적합성", className="d-none d-lg-block d-xl-none c_name_3_4"),
                    html.H4("상위요인 적합성", className="d-none d-xl-block c_name_3_4")
                ]),
                dbc.Col([
                    html.H4("하위 변수 정규 분포", className="d-none d-lg-block d-xl-none c_name_5_6"),
                    html.H4("하위 변수 정규 분포", className="d-none d-xl-block c_name_5_6")
                ]),
            ]),
            dbc.Row([
                # 상위요인 중요도_name
                html.H4("상위요인 중요도", className="d-block d-sm-none", id="m_c_name_1"),  # xs
                html.H4("상위요인 중요도", className="d-none d-sm-block d-md-none m_c_name_1-2_3"),  # sm
                html.H4("상위요인 중요도", className="d-none d-md-block d-lg-none m_c_name_1-2_3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(  # 전기차 파이차트 출력
                                className="pie",
                                id='1',
                            ),
                            html.Div(
                                "위치를 누르면 표현됩니다",
                                className="pie_loading",
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),  # 모바일, 데스크톱 적응형 영역 크기
                    ]),
                ], xs=12, sm=12, md=12, lg=4, xl=2.4, className="pie_chart"),
                html.Div(  # 상위요인 중요도, 상위요인 적합성 구분 선
                    className="line",
                ),
                # 상위요인 적합성_name
                html.H4("상위요인 적합성", className="d-block d-sm-none", id="m_c_name_2"),  # xs
                html.H4("상위요인 적합성", className="d-none d-sm-block d-md-none m_c_name_2-2_3"),  # sm
                html.H4("상위요인 적합성", className="d-none d-md-block d-lg-none m_c_name_2-2_3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 경제적 확률차트 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 경제적 확률차트
                                        className="image",
                                        id='3',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 사회적 확률차트 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 사회적 확률차트
                                        className="image",
                                        id='4',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 환경적 확률차트 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 환경적 확률차트
                                        className="image",
                                        id='5',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 기술적 확률차트 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 기술적 확률차트
                                        className="image",
                                        id='6',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4, className="chart_bar_1"),
                html.Div(  # 확률차트, 정규분포 영역 구분 선(데스크톱에만 적용)
                    className="desktop_line2",
                ),
                # 하위변수 정규분포_name
                html.H4("하위 변수 정규 분포", className="d-block d-sm-none", id="m_c_name_3"),  # xs
                html.H4("하위 변수 정규 분포", className="d-none d-sm-block d-md-none m_c_name_3-2_3"),  # sm
                html.H4("하위 변수 정규 분포", className="d-none d-md-block d-lg-none m_c_name_3-2_3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 정규분포1 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 정규분포1
                                        className="image",
                                        id='7',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 정규분포2 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 정규분포2
                                        className="image",
                                        id='8',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        id="loading1",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 정규분포3 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 정규분포3
                                        className="image",
                                        id='9',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        id="loading2",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 정규분포4 영역
                            dcc.Loading(
                                children=[
                                    dcc.Graph(  # 정규분포4
                                        className="image",
                                        id='10',
                                        style={"position": "relative", "z-index": "2"}
                                    ),
                                    html.Div(
                                        "위치를 누르면 표현됩니다",
                                        id="loading3",
                                        className="loading",
                                    )
                                ],
                                type="circle", style={"margin-top": "270px"}
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
            ], className="chart")
        ])

    @staticmethod
    def drawing_graph():
        return html.Div(className="def_graph", children=[
            dbc.Row([
                dbc.Col([
                    html.H4("전기차 충전소 결과", className="d-none d-lg-block d-xl-none c_name_1_2"),
                    html.H4("전기차 충전소 결과", className="d-none d-xl-block c_name_1_2")
                ]),
                dbc.Col([
                    html.H4("수소차 충전소 결과", className="d-none d-lg-block d-xl-none c_name_3_4"),
                    html.H4("수소차 충전소 결과", className="d-none d-xl-block c_name_3_4")
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.H4("전기차 충전소 결과", className="d-block d-sm-none", id="m_c_name_1"),  # xs
                    html.H4("전기차 충전소 결과", className="d-none d-sm-block d-md-none m_c_name_1-2_3",
                            style={"margin-left": "2.5%"}),  # sm
                    html.H4("전기차 충전소 결과", className="d-none d-md-block d-lg-none m_c_name_1-2_3",
                            style={"margin-left": "2.5%"}),  # md
                    html.Div(
                        dl.Map(center=[35.16434005, 129.0712629], zoom=12.5, zoomControl=True, preferCanvas=False,
                               children=[
                                   dl.TileLayer(),
                                   dl.GeoJSON(data=elec_geojson, id="elec_geojson",
                                              children=[dl.Popup(id="elec_popup")])
                               ], className="map"),
                        className="map_", style={"margin-left": "3%", "margin-right": "8px"}
                    ),
                ], xs=12, sm=12, md=12, lg=6, xl=6),
                dbc.Col([
                    html.H4("수소차 충전소 결과", className="d-block d-sm-none", id="m_c_name_1"),  # xs
                    html.H4("수소차 충전소 결과", className="d-none d-sm-block d-md-none m_c_name_1-2_3",
                            style={"margin-left": "2.5%"}),  # sm
                    html.H4("수소차 충전소 결과", className="d-none d-md-block d-lg-none m_c_name_1-2_3",
                            style={"margin-left": "2.5%"}),  # md
                    html.Div(
                        dl.Map(center=[35.14906405, 128.951891], zoom=11.5, zoomControl=True, preferCanvas=False,
                               children=[
                                   dl.TileLayer(),
                                   dl.GeoJSON(data=hydro_geojson, id="hydro_geojson",
                                              children=[dl.Popup(id="hydro_popup")])
                               ], className="map"),
                        className="map_", style={"margin-right": "3%", "margin-left": "3%"}
                    ),
                ], xs=12, sm=12, md=12, lg=6, xl=6)])
        ])

    @staticmethod
    def main_layout(*args):
        return [
            args[0],
            html.P(),
            args[1],
            html.P(),
            args[2],
            html.P(id='temp', className='temp'),
        ]

    @staticmethod
    def navbar(*args):
        '''
        대시보드 Navbar 영역
        :param args: 대상 객체
        :return:
        '''
        return dbc.Navbar(
            # 하나의 행 사용
            dbc.Row(
                [
                    dbc.Col(
                        html.A(  # 왼편에 로고 표시하고 누르면 페이지 리셋(새로고침)
                            html.Img(src="assets/logo.png", height="120px", id="main_logo"),  # 파일경로, 높이
                            href="",
                            className="logoImg"
                        ),
                        id="img-col"
                    ),
                    dbc.Col(  # 분석 리포트 저장
                        html.Form(
                            dbc.Button("선택한 후보지 전체 영향 관계보기", outline=True, color="secondary", className="me-1",
                                       type="submit"),
                            action="/bayesian",
                            target="_blank",
                        ),
                        id="save"
                    )
                ], className="nav"
            ), className="nav bg-transparent"
        )

    @staticmethod
    def elec_map_chart(name, **figs):
        return [
            dcc.Graph(
                className="map-popup",
                figure=figs['e_final_fig'],
            )
        ]

    @staticmethod
    def hydro_map_chart(name, **figs):
        return [
            dcc.Graph(
                className="map-popup",
                figure=figs['h_final_fig'],
            )
        ]

    @staticmethod
    def elec_value_update(name, **figs):
        for i in range(4):
            figs['fig{}'.format(i + 1)].data[0].y = [elec_list[name][i]]
            figs['fig{}'.format(i + 1)].data[0].text = ['적합 : {}'.format(elec_list[name][i])]
            figs['fig{}'.format(i + 1)].data[1].y = [100 - elec_list[name][i]]
            figs['fig{}'.format(i + 1)].data[1].text = ['부적합 : {}'.format(100 - elec_list[name][i])]
        figs['e_final_fig'].data[0].y = [elec_list[name][4]]
        figs['e_final_fig'].data[0].text = ['적합 : {}'.format(elec_list[name][4])]
        figs['e_final_fig'].data[1].y = [100 - elec_list[name][4]]
        figs['e_final_fig'].data[1].text = ['부적합 : {}'.format(100 - elec_list[name][4])]
        figs['e_final_fig'].update_layout(title_text=name)

    @staticmethod
    def hydro_value_update(name, **figs):
        for i in range(4):
            figs['hy_fig{}'.format(i + 1)].data[0].y = [hydro_list[name][i]]
            figs['hy_fig{}'.format(i + 1)].data[0].text = ['적합 : {}'.format(hydro_list[name][i])]
            figs['hy_fig{}'.format(i + 1)].data[1].y = [100 - hydro_list[name][i]]
            figs['hy_fig{}'.format(i + 1)].data[1].text = ['부적합 : {}'.format(100 - hydro_list[name][i])]
        figs['h_final_fig'].data[0].y = [hydro_list[name][4]]
        figs['h_final_fig'].data[0].text = ['적합 : {}'.format(hydro_list[name][4])]
        figs['h_final_fig'].data[1].y = [100 - hydro_list[name][4]]
        figs['h_final_fig'].data[1].text = ['부적합 : {}'.format(100 - hydro_list[name][4])]
        figs['h_final_fig'].update_layout(title_text=name)


class Bayesian:  # 베이지안 페이지 모델링
    @staticmethod
    def bay_bar_layout(**df):
        # 확률차트 생성
        fig1 = px.bar(df["경제적"], x="경제적", y="적합확률", color="경제적 요소", text="경제적 요소")
        # 경제적 확률차트(x: x축 라벨명, y: 값, color: 막대 색)
        fig1.update_yaxes(visible=False)
        fig1.update_xaxes(visible=False)
        fig2 = px.bar(df["사회적"], x="사회적", y="적합확률", color="사회적 요소", text="사회적 요소")  # 사회적 확률차트
        fig2.update_yaxes(visible=False)
        fig2.update_xaxes(visible=False)
        fig3 = px.bar(df["환경적"], x="환경적", y="적합확률", color="환경적 요소", text="환경적 요소")  # 환경적 확률차트
        fig3.update_yaxes(visible=False)
        fig3.update_xaxes(visible=False)
        fig4 = px.bar(df["기술적"], x="기술적", y="적합확률", color="기술적 요소", text="기술적 요소")  # 기술적 확률차트
        fig4.update_yaxes(visible=False)
        fig4.update_xaxes(visible=False)
        hy_fig1 = px.bar(df["수소_경제적"], x="경제적", y="적합확률", color="경제적 요소", text="경제적 요소")  # 수소 - 경제
        hy_fig1.update_yaxes(visible=False)
        hy_fig1.update_xaxes(visible=False)
        hy_fig2 = px.bar(df["수소_사회적"], x="사회적", y="적합확률", color="사회적 요소", text="사회적 요소")  # 수소 - 사회
        hy_fig2.update_yaxes(visible=False)
        hy_fig2.update_xaxes(visible=False)
        hy_fig3 = px.bar(df["수소_환경적"], x="환경적", y="적합확률", color="환경적 요소", text="환경적 요소")  # 수소 - 환경
        hy_fig3.update_yaxes(visible=False)
        hy_fig3.update_xaxes(visible=False)
        hy_fig4 = px.bar(df["수소_기술적"], x="기술적", y="적합확률", color="기술적 요소", text="기술적 요소")  # 수소 - 기술
        hy_fig4.update_yaxes(visible=False)
        hy_fig4.update_xaxes(visible=False)
        e_final_fig = px.bar(df['전기차 최종 부지선정'], x='최종 부지선정', y='적합확률', color='최종 부지선정 요소', text='최종 부지선정 요소')
        e_final_fig.update_yaxes(visible=False)
        e_final_fig.update_yaxes(visible=False)
        h_final_fig = px.bar(df['수소차 최종 부지선정'], x='최종 부지선정', y='적합확률', color='최종 부지선정 요소', text='최종 부지선정 요소')
        h_final_fig.update_yaxes(visible=False)
        h_final_fig.update_yaxes(visible=False)
        return fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4, e_final_fig, h_final_fig

    @staticmethod
    def bay_layout(**figs):
        return [
            #################### 전기차 상위요소 - 막대그래프 ##################
            figs["fig1"].update_layout({  # 경제적 차트(임시)
                'paper_bgcolor': '#E9EEF6',  # 배경색
            }, title_text="전기-경제적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
            figs["fig2"].update_layout({  # 사회적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-사회적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["fig3"].update_layout({  # 환경적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-환경적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["fig4"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-기술적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            ####################### 수소차 상위요소 - 막대그래프 ##############
            figs["hy_fig1"].update_layout({  # 수소 - 경제적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-경제적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig2"].update_layout({  # 수소 - 사회적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-사회적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig3"].update_layout({  # 수소 - 환경적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-환경적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig4"].update_layout({  # 수소 - 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-기술적", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            figs["e_final_fig"].update_layout({  # 전기차 최종확률
                'paper_bgcolor': '#E9EEF6',
            }, title_text="최종 부지선정", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            figs["h_final_fig"].update_layout({  # 수소차 최종확률
                'paper_bgcolor': '#E9EEF6',
            }, title_text="최종 부지선정", title_font_size=22, margin_l=10, margin_r=10, margin_b=20,
                font_family='NanumSquare', showlegend=False),

            ##################환경적####################
            figs["ozone"].update_layout(paper_bgcolor='#E9EEF6', title_text="오존 대기오염도", margin_t=70, legend_y=1.35),
            figs["so2"].update_layout(paper_bgcolor='#E9EEF6', title_text="아황산가스 대기오염도", margin_t=70, legend_y=1.35,
                                      title_font_size=17),
            figs["no2"].update_layout(paper_bgcolor='#E9EEF6', title_text="이산화질소 대기오염도", margin_t=70, legend_y=1.35,
                                      title_font_size=17),
            figs["pm25"].update_layout(paper_bgcolor='#E9EEF6', title_text="미세먼지-pm25", margin_t=70, legend_y=1.35),
            figs["pm10"].update_layout(paper_bgcolor='#E9EEF6', title_text="미세먼지-pm10", margin_t=70, legend_y=1.35),

            ########################사회적####################
            figs["population"].update_layout(paper_bgcolor='#E9EEF6', title_text="고정인구 인구밀도", margin_t=70,
                                             legend_y=1.35, title_font_size=20),
            figs["f_population"].update_layout(paper_bgcolor='#E9EEF6', title_text="월 평균 유동인구 인구밀도", margin_t=70,
                                               legend_y=1.5, title_font_size=14),
            figs["eleFig"].update_layout(paper_bgcolor='#E9EEF6', title_text="충전소당 전기차 차량 수", margin_t=0, legend_y=0.8,
                                         legend_orientation="h", title_font_size=9),
            figs["hydFig"].update_layout(paper_bgcolor='#E9EEF6', title_text="충전소당 수소차 차량 수", margin_t=0, legend_y=0.5,
                                         legend_orientation="h", title_font_size=10),
            figs["intersection"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="도로 보급률", margin_t=70,
                                               legend_y=1.35),

            ##################경제적#################
            figs["elec_charger_cost"].update_layout(paper_bgcolor='#E9EEF6', title_text="전기차 충전기 구축 비용", margin_t=60,
                                                    legend_y=1.2),
            figs["hydro_charger_cost"].update_layout(paper_bgcolor='#E9EEF6', title_text="수소차 충전기 구축 비용", margin_t=60,
                                                     legend_y=1.2),
            figs["land_cost"].update_layout(paper_bgcolor='#E9EEF6', title_text="후보지 평균 소득", margin_t=70,
                                            legend_y=1.35),
            figs["hydro_expected_income"].update_layout(paper_bgcolor='#E9EEF6', title_text="수소 충전소 기대 수익", margin_t=10,
                                                        legend_y=1.35),

            ################기술적#################
            figs["elec_capacity"].update_layout(paper_bgcolor='#E9EEF6', title_text="전기 충전기 용량", margin_t=70,
                                                legend_y=1.35),
            figs["hydro_supply_car"].update_layout(paper_bgcolor='#E9EEF6', title_text="충전소 당 공급 가능 차량 수", margin_t=70,
                                                   legend_y=1.35, title_font_size=14),
            figs["hydro_supply_fuel"].update_layout({'paper_bgcolor': '#E9EEF6'}, title_text="수소차 연료 공급 방식",
                                                    margin_t=70,
                                                    legend_y=1.35),
        ]

    @staticmethod
    def bayesian_network(**figs):
        '''
        전기차
        베이지안 네트워크
        출력 임시 메서드
        :param args:
        :return:
        '''
        # return html.Div("hello")
        # return bayesian_network_E.layout
        return html.Div(className='bay', children=[
            html.Img(src="assets/logo.png", id="logo"),  # 로고

            html.Div(id="env", children=[  # 환경적 - 오존, 아황산가스, 이산화질소, 미세먼지 =>수소, 전기 동일함
                html.H1("환경적"),
                # 하위요소 - 정규분포
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["ozone"],  # 오존
                            style={"position": "relative", "z-index": "2"},  # loading 위에 그래프를 올리기 위해
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=4, sm=4, md=4, lg=4, xl=4),
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["so2"],  # 아황산가스
                            style={"position": "relative", "z-index": "2"},
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=4, sm=4, md=4, lg=4, xl=4),
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["no2"],  # 이산화질소
                            style={"position": "relative", "z-index": "2"},
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=4, sm=4, md=4, lg=4, xl=4),
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["pm25"],  # 미세먼지 pm25
                            style={"position": "relative", "z-index": "2"}
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=4, sm=4, md=4, lg=4, xl=4),
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["pm10"],  # 미세먼지 pm10
                            style={"position": "relative", "z-index": "2"}
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=4, sm=4, md=4, lg=4, xl=4),
                ], style={'margin-top': '2%'}),  # 행과의 거리 띄우기
                # 상위요소 - 막대그래프
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            className="standard_1",
                            figure=figs["fig3"],  # 환경적 - 상위요소 (막대그래프)
                            id="bay_env",
                            style={"position": "relative", "z-index": "2"}
                        ),
                        html.Div(
                            "Loading...",
                            className="bay_loading",
                        )
                    ], xs=12, sm=12, md=12, lg=12, xl=12, style={'margin-top': '2%'})  # 행과의 거리 띄우기
                ]),
                html.Div(id="soc", children=[
                    # 사회적 - 고정인구, 월 평균 유동인구, 충전소당 친환경 차량수(eleFig, hydFig), 도로 보급률
                    html.H1("사회적"),
                    # 하위요소 - 정규분포
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["population"],  # 고정인구
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["f_population"],  # 월 평균 유동인구
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["eleFig"],  # 충전소당 친환경 차량수
                                id="elec_hydro_Fig",  # 전기차 / 수소차
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["intersection"],  # 도로 보급률
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                    ], style={'margin-top': '2%'}),  # 행과의 거리 띄우기
                    # 상위요소 - 막대그래프
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["fig2"],  # 사회적 - 상위요소 (막대그래프)
                                id="bay_soc",
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'margin-top': '2%'})  # 행과의 거리 띄우기
                    ]),
                ]),
                html.Div(id="eco", children=[
                    # 경제적 - 수소: 수소 충전소 기대수익, 충전기 구축 비용, 후보지 평균 소득
                    #            hydro_expected_income ,hydro_charger_cost, land_cost
                    #         전기: 충전기 구축 비용, 후보지 평균 소득
                    #               elec_charger_cost, land_cost
                    html.H1("경제적"),
                    # 상위요소 - 막대그래프
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["fig1"],  # 경제적 - 상위요소 (막대그래프)
                                id="bay_eco",
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12)
                    ]),
                    # 하위요소 - 정규분포
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["elec_charger_cost"],  # 충전기 구축 비용
                                id="charger_cost",  # 전기차, 수소차
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["land_cost"],  # 후보지 평균 소득
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["hydro_expected_income"],
                                id="hydro_expected_income",  # 수소 충전소 기대 수익
                                style={"position": "relative", "z-index": "2"}
                            ),
                        ], xs=4, sm=4, md=4, lg=4, xl=4),
                    ], style={'margin-top': '2%'}),
                ]),
                html.Div(id="tec", children=[
                    # 기술적 - 수소: 수소 연료 공급 방식, 충전소 당 공급 가능 차량 수
                    #               hydro_supply_fuel, hydro_supply_car
                    #         전기: 전기 충전기 용량
                    #               elec_capacity
                    html.H1("기술적"),
                    # 상위요소 - 막대그래프
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["fig4"],  # 기술적 - 상위요소 (막대그래프)
                                id="bay_tec",
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ]),
                    ]),
                    # 하위요소 - 정규분포
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["elec_capacity"],  # 전기 : 전기 충전기 용량 - elec_capacity
                                id="capacity_insatll",  # 수소 : 수소차 충전소 당 공급 가능 차량 수 - hydro_supply_car
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ], xs=6, sm=6, md=6, lg=6, xl=6),
                        dbc.Col([
                            dcc.Graph(
                                className="standard_1",
                                figure=figs["hydro_supply_fuel"],  # 수소 : 수소차 연료 공급 방식
                                id="supply_fuel",
                                style={"position": "relative", "z-index": "2"}
                            ),
                        ], xs=6, sm=6, md=6, lg=6, xl=6),
                    ], style={'margin-top': '2%'}),
                ]),

                html.Div(id="cen", children=[
                    # 최종 확률 그래프
                    html.H1("최종 확률"),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(
                                className="ch_cen",
                                figure=figs["e_final_fig"],  # 최종 확률 - 막대 그래프
                                id="final_fig",  # 전기차 / 수소차차
                                style={"position": "relative", "z-index": "2"}
                            ),
                            html.Div(
                                "Loading...",
                                className="bay_loading",
                            )
                        ])
                    ])
                ])
            ]),

        ])

    @staticmethod
    def layout(*args):
        '''
        베이지안 네트워크 출력 레이아웃 임시 메서드
        :param args:
        :return:
        '''
        return html.Div(className='main', children=[
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
        ])


class CallBack:  # 콜백함수 모델링
    @staticmethod
    def page_transitions(bayesian_layout, main_layout):
        @callback(
            Output('page-content', 'children'),
            Input('url', 'pathname')
        )
        def display_page(pathname):
            if pathname == '/bayesian':
                return bayesian_layout
            else:
                return main_layout
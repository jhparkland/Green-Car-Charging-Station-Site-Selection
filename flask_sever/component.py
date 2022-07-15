from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from flask_sever import bayesian_network


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
        final_fig = px.bar(df['최종 부지선정'], x='최종 부지선정', y='적합확률', color='최종 부지선정 요소', text='최종 부지선정 요소')
        final_fig.update_yaxes(visible=False)
        final_fig.update_yaxes(visible=False)

        return fig_1, fig_2, fig1, fig2, fig3, fig4, hy_fig1, hy_fig2, hy_fig3, hy_fig4, final_fig

    @staticmethod
    def chart_layout(**figs):
        return [figs["fig1"].update_layout({  # 경제적 차트(임시)
            'paper_bgcolor': '#E9EEF6',  # 배경색
        }, title_text="전기-경제적", title_font_size=22, margin_l=10, margin_r=10,
            font_family='NanumSquare', showlegend=False),  # 좌우 여유공간, 범례 위치조정, 제목 안보이게 하기
            figs["fig2"].update_layout({  # 사회적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-사회적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["fig3"].update_layout({  # 환경적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-환경적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["fig4"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="전기-기술적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig1"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-경제적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig2"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-사회적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig3"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-환경적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["hy_fig4"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="수소-기술적", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            figs["final_fig"].update_layout({  # 기술적 차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text="최종 부지선정", title_font_size=22, margin_l=10, margin_r=10,
                font_family='NanumSquare', showlegend=False),
            # 파이차트 배경색
            figs["fig_1"].update_layout({  # 전기차 파이차트(임시)
                'paper_bgcolor': '#E9EEF6',  # 배경색
            }, title_text='전기차', title_y=0.8, title_font_size=22,  # 제목 설정
                margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.5,  # 좌우위아래 여유공간
                legend_x=0.25, legend_orientation="h", legend_font_size=9, font_family='NanumSquare', font_size=9.6),
            # 범례 설정
            figs["fig_2"].update_layout({  # 수소차 파이차트(임시)
                'paper_bgcolor': '#E9EEF6',
            }, title_text='수소차', title_y=0.8, title_font_size=22,
                margin_l=0, margin_r=0, margin_b=20, margin_t=40, legend_y=1.5,
                legend_x=0.25, legend_orientation="h", legend_font_size=9, font_family='NanumSquare', font_size=9.6),
            figs["ozone"].update_layout({
                'paper_bgcolor': '#E9EEF6',
            }, title_text="오존", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
            figs["so2"].update_layout({
                'paper_bgcolor': '#E9EEF6',
            }, title_text="아황산가스", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
            figs["pm25"].update_layout({
                'paper_bgcolor': '#E9EEF6',
            }, title_text="pm25", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare'),
            figs["pm10"].update_layout({
                'paper_bgcolor': '#E9EEF6',
            }, title_text="pm10", title_font_size=22, margin_l=10, margin_r=10, font_family='NanumSquare')]

    @staticmethod
    def drawing_chart(**figs):
        '''
        대시보드 차트 시각화 메서드
        :param args: fig 객체
        :return: html
        '''
        return html.Div(className='def_chart', children=[
            dbc.Row([
                dbc.Col([
                    html.H4("상위요인 중요도", className="d-none d-lg-block d-xl-none", id="c_name_1"),
                    html.H4("상위요인 중요도", className="d-none d-xl-block", id="c_name_2")
                ]),
                dbc.Col([
                    html.H4("상위요인 적합성", className="d-none d-lg-block d-xl-none", id="c_name_3"),
                    html.H4("상위요인 적합성", className="d-none d-xl-block", id="c_name_4")
                ]),
                dbc.Col([
                    html.H4("하위 변수 정규 분포", className="d-none d-lg-block d-xl-none", id="c_name_5"),
                    html.H4("하위 변수 정규 분포", className="d-none d-xl-block", id="c_name_6")
                ]),
            ]),
            dbc.Row([
                # 상위요인 중요도_name
                html.H4("상위요인 중요도", className="d-block d-sm-none", id="m_c_name_1"),  # xs
                html.H4("상위요인 중요도", className="d-none d-sm-block d-md-none", id="m_c_name_1-2"),  # sm
                html.H4("상위요인 중요도", className="d-none d-md-block d-lg-none", id="m_c_name_1-3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(  # 전기차 파이차트 출력
                                className="standard",
                                id='1',
                                figure=figs["fig_1"],
                            ),
                        ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'}),  # 모바일, 데스크톱 적응형 영역 크기
                        dbc.Col([
                            dcc.Graph(  # 수소차 파이차트 출력
                                className="standard",
                                id='2',
                                figure=figs["fig_2"],
                            ),
                        ], xs=6, sm=6, md=6, lg=12, xl=12, style={'padding': '12px'})
                    ]),
                ], xs=12, sm=12, md=12, lg=4, xl=2.4, className="pie_chart"),
                html.Div(  # 상위요인 중요도, 상위요인 적합성 구분 선
                    className="line",
                ),
                # 상위요인 적합성_name
                html.H4("상위요인 적합성", className="d-block d-sm-none", id="m_c_name_2"),  # xs
                html.H4("상위요인 적합성", className="d-none d-sm-block d-md-none", id="m_c_name_2-2"),  # sm
                html.H4("상위요인 적합성", className="d-none d-md-block d-lg-none", id="m_c_name_2-3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 경제적 확률차트 영역
                            dcc.Graph(  # 경제적 확률차트
                                className="image",
                                id='3',
                                figure=figs["ozone"],
                            ),
                            dcc.Loading(
                                id="ls-loading-2",
                                children=[html.Div([html.Div(id="ls-loading-output-2")])],
                                type="circle",
                            )
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 사회적 확률차트 영역
                            dcc.Graph(  # 사회적 확률차트
                                className="image",
                                id='4',
                                figure=figs["so2"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 환경적 확률차트 영역
                            dcc.Graph(  # 환경적 확률차트
                                className="image",
                                id='5',
                                figure=figs["fig3"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 기술적 확률차트 영역
                            dcc.Graph(  # 기술적 확률차트
                                className="image",
                                id='6',
                                figure=figs["fig4"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4, className="chart_bar_1"),
                html.Div(  # 확률차트, 정규분포 영역 구분 선(데스크톱에만 적용)
                    className="desktop_line2",
                ),
                # 하위변수 정규분포_name
                html.H4("하위 변수 정규 분포", className="d-block d-sm-none", id="m_c_name_3"),  # xs
                html.H4("하위 변수 정규 분포", className="d-none d-sm-block d-md-none", id="m_c_name_3-2"),  # sm
                html.H4("하위 변수 정규 분포", className="d-none d-md-block d-lg-none", id="m_c_name_3-3"),  # md
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 정규분포1 영역
                            dcc.Graph(  # 정규분포1
                                className="image",
                                id='7',
                                figure=figs["ozone"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 정규분포2 영역
                            dcc.Graph(  # 정규분포2
                                className="image",
                                id='8',
                                figure=figs["ozone"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([  # 정규분포3 영역
                            dcc.Graph(  # 정규분포3
                                className="image",
                                id='9',
                                figure=figs["ozone"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'}),
                        dbc.Col([  # 최종결과 영역
                            dcc.Graph(  # 최종결과
                                className="image",
                                id='10',
                                figure=figs["fig1"],
                            ),
                        ], xs=12, sm=12, md=12, lg=12, xl=12, style={'padding': '12px'})
                    ])
                ], xs=12, sm=12, md=12, lg=2, xl=2.4),
            ], className="chart")
        ])

    @staticmethod
    def main_layout(*args):
        return [
            args[0],
            args[1],
            html.Br(),
            html.H4("선정된 최적의 부지", id="map_title"),
            html.Iframe(  # 하단부(지도)
                src="/assets/parkinglot_map.html",
                style={"height": "500px", "width": "95%"},
                className="map_"
            ),
            html.P(),
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
                            html.Img(src="assets/logo.png", height="120px", id="logo"),  # 파일경로, 높이
                            href="",
                            className="logoImg"
                        ),
                        id="img-col"
                    ),
                    dbc.Col(  # 분석 리포트 저장
                        html.Form(
                            dbc.Button("분석 리포트 저장", outline=True, color="secondary", className="me-1",
                                       type="submit"),
                            action="/bayesian",
                            target="_blank",
                        ),
                        id="save"
                    )
                ], className="nav"
            ), className="nav"
        )

class Bayesian:  # 베이지안 페이지 모델링

    @staticmethod
    def print_hello():
        '''
        베이지안 네트워크 출력 임시 메서드
        :param args:
        :return:
        '''
        # return html.Div("hello")
        return bayesian_network.layout

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

    # def __init__(self):
    #     self.save_hydro = self.save_elec = self.save_econ = self.save_soci = self.save_envi = self.save_tech = {}

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

    # @staticmethod
    # def elec_piechart_click(save_elec, save_hydro):
    #     @callback(  # 전기차 파이차트 클릭데이터 초기화
    #         Output("1", "clickData"),
    #         Input("2", "clickData")
    #     )
    #     def clear_elec(hydro):
    #         if hydro is not None:
    #             global save_elec, save_hydro
    #             save_hydro = hydro
    #             return
    #         else:
    #             return save_elec
    #
    # @staticmethod
    # def hydro_piechart_click(save_elec, save_hydro):
    #     @callback(  # 수소차 파이차트 클릭데이터 초기화
    #         Output("2", "clickData"),
    #         Input("1", "clickData")
    #     )
    #     def clear_hydro(elec):
    #         global save_elec, save_hydro
    #         if elec is not None:
    #             save_elec = elec
    #             return None
    #         else:
    #             return save_hydro
    #
    # @staticmethod
    # def soci_chart_click(save_econ, save_soci, save_envi, save_tech):
    #     @callback(  # 사회적 확률 차트 클릭데이터 초기화
    #         Output("4", "clickData"),
    #         Input("3", "clickData"),
    #     )
    #     def clear_econ(econ):
    #         global save_econ, save_soci, save_envi, save_tech
    #         if econ is not None:
    #             save_econ, save_soci, save_envi, save_tech = econ, None, None, None
    #             return
    #         else:
    #             return save_envi
    #
    # @staticmethod
    # def envi_chart_click(save_econ, save_soci, save_envi, save_tech):
    #     @callback(  # 환경적 확률 차트 클릭데이터 초기화
    #         Output("5", "clickData"),
    #         Input("4", "clickData"),
    #     )
    #     def clear_econ(soci):
    #         global save_econ, save_soci, save_envi, save_tech
    #         if soci is not None:
    #             save_econ, save_soci, save_envi, save_tech = None, soci, None, None
    #             return
    #         else:
    #             return save_soci
    #
    # @staticmethod
    # def tech_chart_click(save_econ, save_soci, save_envi, save_tech):
    #     @callback(  # 기술적 확률 차트 클릭데이터 초기화
    #         Output("6", "clickData"),
    #         Input("5", "clickData"),
    #     )
    #     def clear_econ(envi):
    #         global save_econ, save_soci, save_envi, save_tech
    #         if envi is not None:
    #             save_econ, save_envi, save_soci, save_tech = None, envi, None, None
    #             return
    #         else:
    #             return save_tech
    #
    # @staticmethod
    # def econ_chart_click(save_econ, save_soci, save_envi, save_tech):
    #     @callback(  # 경제적 확률 차트 클릭데이터 초기화
    #         Output("3", "clickData"),
    #         Input("6", "clickData"),
    #     )
    #     def clear_econ(tech):
    #         global save_econ, save_soci, save_envi, save_tech
    #         if tech is not None:
    #             save_econ, save_soci, save_envi, save_tech = None, None, None, tech
    #             return
    #         else:
    #             return save_econ

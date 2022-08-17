import Possibility
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete.CPD import TabularCPD

ev_model = BayesianNetwork(
    [
        ###########환경적###########
        ('Ozone', 'Environment'),  # 오존 -> 환경
        ('So2', 'Environment'),  # 아황산 -> 환경
        ('No2', 'Environment'),  # 이산화질소 -> 환경
        ('Co', 'Environment'),  # 일산화탄소 -> 환경
        ('Pm25', 'Environment'),  # 미세먼지 2.5 -> 환경
        ('pm10', 'Environment'),  # 미세먼지 10 -> 환경
        ('Total_air', 'Environment'),  # 통합 대기질 -> 환경
        ###########사회적############
        ('Population', "Social"),  # 고정인구 -> 사회
        ('Floating_population', "Social"),  # 유동인구 -> 사회
        ('Ev_reg', "Social"),  # 전기차 등록 수 -> 사회
        ('Intersection', "Social"),  # 교차로 수 -> 사회
        ('Evcs', 'Social'), # 전기차 충전소 -> 사회
        ('Highway', "Social"),  # 고속도로 여부 -> 사회
        ############경제적##############
        ('parkinglot_n', 'Economical'),  # 주차장 구획 수 -> 경제
        ############기술적#############
        ('Charging_time', 'Technical')  # 충전 시간 -> 기술
    ]
)

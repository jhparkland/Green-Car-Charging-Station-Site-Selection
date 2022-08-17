from Module.Environment import *
from Module.Social import *
from Module.Economical import *
from Module.Technical import *


def get_joint_pro(variable, weight):
    result = 0.0
    variable_weight = list(zip(variable, weight))
    for pro, wei in variable_weight:
        result += pro * wei
    return [round(result, 6), round(1 - result, 6)]


def conditional_pro(weight):
    '''
    weight : 결합할 변수의 가중치 값(list)
    '''
    # 조건부확률테이블의 길이는 2^(하위 변수)의 크기를 가짐
    table_len = 2 ** len(weight)
    # 결과 리스트 초기화
    result_true = [0.0] * table_len

    for i in range(len(weight)):  # 3번
        for j in range(table_len):  # 8번
            # 변수의 T,F 거짓값
            cycle = table_len / (2 ** (i + 1))
            if int(j / cycle) % 2 == 0:
                result_true[j] += weight[i]
                # 부동소수점 오차 제거
                result_true[j] = round(result_true[j], 6)

    result_false = list(reversed(result_true))

    return result_true, result_false


class Probability:

    def __init__(self):
        # E는 전기차, H는 수소차
        self.variable_environment = []  # 환경변수는 전기/수소 동일
        self.variable_social_elec = []
        self.variable_social_hydro = []
        self.variable_economic_elec = []
        self.variable_economic_hydro = []
        self.variable_technical_elec = []
        self.variable_technical_hydro = []
        # 가중치
        self.weight_environment = [0.13, 0.13, 0.13, 0.13, 0.13, 0.13,
                                   0.22]  # co, so2, no2, ozone, pm10, pm25, 통합대기환경지수(khai)
        self.weight_social_elec = [0.1, 0.1, 0.3, 0.2, 0.2, 0.1]  # 고정인구, 유동인구, 전기차 수, 전기차 충전소 수, 교통 편의성, 고속도로 여부
        self.weight_social_hydro = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2,
                                    0.1]  # 고정인구, 유동인구, LPG 충전소 수, 수소차 수, 수소차 충전소 수, 교통 편의성, 고속도로 여부
        self.weight_economic_elec = [1.0]  # 주차 구획수
        self.weight_economic_hydro = [0.5, 0.5]  # LPG 충전소 토지비용, 수소충전소 구축 비용
        self.weight_technical_elec = [1.0]  # 급속/완속 적합성
        self.weight_technical_hydro = [1.0]  # 복합 충전소 여부
        self.weight_primary_factor = [0.15, 0.4, 0.3, 0.15]  # 상위 요소들의 가중치(환경, 사회, 경제, 기술)

        # 상위 요소 결합 확률
        self.environment_joint_pro = 0  # 환경요소 결합 확률

        self.social_joint_pro_elec = 0  # 사회(전기) 결합 확률
        self.social_joint_pro_hydro = 0  # 사회(수소) 결합 확률

        self.economic_joint_pro_elec = 0  # 경제(전기) 결합 확률
        self.economic_joint_pro_hydro = 0  # 경제(수소) 결합 확률

        self.technical_joint_pro_elec = 0  # 기술(전기) 결합 확률
        self.technical_joint_pro_hydro = 0  # 기술(수소) 결합 확률

        # 조건부 확률 변수
        self.environment_pro, environment_pro_negative = 0, 0
        self.social_elec_pro, self.social_elec_pro_negative = 0, 0
        self.social_hydro_pro, self.social_hydro_pro_negative = 0, 0
        self.economic_elec_pro, self.economic_elec_pro_negative = 0, 0
        self.economic_hydro_pro, self.economic_hydro_pro_negative = 0, 0
        self.technical_elec_pro, self.technical_elec_pro_negative = 0, 0
        self.technical_hydro_pro, self.technical_hydro_pro_negative = 0, 0

    def set_env_pro(self):
        '''
        환경적 변수의 적합도 리스트 반환
        '''
        environment_list = [
            Co().t_pro,  # 일산화탄소
            So2().t_pro,  # 아황산가스
            No2().t_pro,  # 이산화질소
            Ozone().t_pro,  # 이산화질소
            FineDust_pm10().t_pro,  # 미세먼지 pm2.5
            FineDust_pm25().t_pro,  # 미세먼지 pm10
            Total_air_quality().t_pro  # 통합 대기환경
        ]
        for env in environment_list:
            self.variable_environment.append(env)

    def set_soc_elec_pro(self):
        '''
        사회적 변수(전기차) 적합도 반환
        '''
        social_elec_list = [
            Population().t_pro,  # 고정인구
            FloatingPopulation().t_pro,  # 유동인구
            Eco_friendly_car_registration().elec_t_pro,  # 전기차
            EVCS().t_pro,  # 전기 충전소
            Intersection().t_pro,  # 교차로
            Highway().t_pro  # 고속도로
        ]
        for soc in social_elec_list:
            self.variable_social_elec.append(soc)

    def set_soc_hydro_pro(self):
        social_hydro_list = [
            Population().t_pro,  # 고정인구
            FloatingPopulation().t_pro,  # 유동인구
            LPG_charging_station().t_pro,  # LPG 충전소
            Eco_friendly_car_registration().hydro_t_pro,  # 수소차
            HVCS().t_pro,  # 수소 충전소
            Intersection().t_pro,  # 교차로
            Highway().t_pro  # 고속도로
        ]
        for soc in social_hydro_list:
            self.variable_social_hydro.append(soc)

    def set_eco_elec_pro(self):
        self.variable_economic_elec.append(Parkinglot().t_pro)  # 주차장 구획 수

    def set_eco_hydro_pro(self):
        economic_hydro_list = [
            Lpg_land_costs().t_pro,  # LPG 충전소 토지 비용
            Hydrogen_charger_cost().t_pro
        ]
        for eco in economic_hydro_list:
            self.variable_economic_hydro.append(eco)

    def set_tech_elec_pro(self):
        self.variable_technical_elec.append(Charging_time().t_pro)

    def set_tech_hydro_pro(self):
        self.variable_technical_hydro.append(Complex_charging_station().complex_cs_pro)

    def print_pro(self):
        Probability.set_env_pro(self)
        Probability.set_soc_elec_pro(self)
        Probability.set_soc_hydro_pro(self)
        Probability.set_eco_elec_pro(self)
        Probability.set_eco_hydro_pro(self)
        Probability.set_tech_elec_pro(self)
        Probability.set_tech_hydro_pro(self)
        print(
            f"{self.variable_environment}\n{self.variable_social_elec}\n{self.variable_social_hydro}\n{self.variable_economic_elec}\n{self.variable_economic_hydro}\n{self.variable_technical_elec}\n{self.variable_technical_hydro}")


# if __name__ == '__main__':
#     pro = Probability()
#     pro.print_pro()
#     pro.environment_joint_pro = get_joint_pro(pro.variable_environment, pro.weight_environment)
#     pro.social_joint_pro_elec = get_joint_pro(pro.variable_social_elec, pro.weight_social_elec)
#     pro.social_joint_pro_hydro = get_joint_pro(pro.variable_social_hydro, pro.weight_social_hydro)
#     pro.economic_joint_pro_elec = get_joint_pro(pro.variable_economic_elec, pro.weight_economic_elec)
#     pro.economic_joint_pro_hydro = get_joint_pro(pro.variable_economic_hydro, pro.weight_economic_hydro)
#     pro.technical_joint_pro_elec = get_joint_pro(pro.variable_technical_elec, pro.weight_technical_elec)
#     pro.technical_joint_pro_hydro = get_joint_pro(pro.variable_technical_hydro, pro.weight_technical_hydro)
#
#     print(f"결합 확률: {pro.environment_joint_pro}")
#     print(f"결합 확률: {pro.social_joint_pro_elec}")
#     print(f"결합 확률: {pro.social_joint_pro_hydro}")
#     print(f"결합 확률: {pro.economic_joint_pro_elec}")
#     print(f"결합 확률: {pro.technical_joint_pro_elec}")
#     print(f"결합 확률: {pro.technical_joint_pro_elec}")
#     print(f"결합 확률: {pro.technical_joint_pro_hydro}")
#
#     pro.environment_pro, pro.environment_pro_negative = conditional_pro(pro.weight_environment)
#     pro.social_elec_pro, pro.social_elec_pro_negative = conditional_pro(pro.weight_social_elec)
#     pro.social_hydro_pro, pro.social_hydro_pro_negative = conditional_pro(pro.weight_social_hydro)
#     pro.economic_elec_pro, pro.economic_elec_pro_negative = conditional_pro(pro.weight_economic_elec)
#     pro.economic_hydro_pro, pro.economic_hydro_pro_negative = conditional_pro(pro.weight_economic_hydro)
#     pro.technical_elec_pro, pro.technical_elec_pro_negative = conditional_pro(pro.weight_technical_elec)
#     pro.technical_hydro_pro, pro.technical_hydro_pro_negative = conditional_pro(pro.weight_technical_hydro)
#
#
#
#     print(pro.environment_pro, pro.environment_pro_negative)
#     print(pro.social_elec_pro, pro.social_elec_pro_negative)
#     print(pro.social_hydro_pro, pro.social_hydro_pro_negative)
#     print(pro.economic_elec_pro, pro.economic_elec_pro_negative)
#     print(pro.economic_hydro_pro, pro.economic_hydro_pro_negative)
#     print(pro.technical_elec_pro, pro.technical_elec_pro_negative)
#     print(pro.technical_hydro_pro, pro.technical_hydro_pro_negative)
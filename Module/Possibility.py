from Environment import *
from Social import *
from Economical import *
from Technical import *



def get_joint_pro(variable, weight):
    result = 0.0
    variable_weight = list(zip(variable,weight))
    for pro, wei in variable_weight:
        # 이중리스트인 경우
        if isinstance(pro,list) and isinstance(wei,list):
            max = 0.0
            value_w = -1
            v_w = list(zip(pro,wei))
            for p,w in v_w:
                if max <= p:
                    max = p
                    value_w = w
            result += max*value_w
            
        else:
            result += pro*wei
    return round(result,6)


# 조건부 확률 구하기
def conditional_pro(weight):
    '''
    weight : 결합할 변수의 가중치 값(list)
    '''
    
    table_len = 1
    for wei in weight:
        weight_len = 0
        if isinstance(wei,list):    # 상태가 3개 이상인 정성적인 변수의 가중치인 경우
            for i in wei:
                weight_len += 1
            # 조건부확률테이블의 길이는 (변수 cardinality들의 곱)의 크기를 가짐
            table_len *= weight_len
        else:
            table_len *= 2
    
    # 결과 리스트 초기화
    result_True = [0.0]*table_len
    result_False = []
    # 변수의 T,F 상태 변화 주기
    cycle = table_len
    for i in range(len(weight)): 
        # cardinality가 3개 이상인 변수의 가중치인 경우(정성적)
        if isinstance(weight[i],list):
            cycle = cycle / len(weight[i])
            pos = 0
            for wei in weight[i]:
                for j in range(table_len):          
                    if int(j/cycle)%len(weight[i]) == pos:
                        result_True[j] += wei
                        result_True[j] = round(result_True[j],6)
                pos += 1
        else:
            cycle = cycle/2
            for j in range(table_len): 
                if int(j/cycle)%2 == 0:
                    result_True[j] += weight[i]
                    result_True[j] = round(result_True[j],6)
    for pro in result_True:
        result_False.append(round(1-pro,6))

    return result_True, result_False


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
        self.weight_environment = [0.3,0.3,0.1,0.15,0.15]  # co, no2, ozone, pm10, pm25
        self.weight_social_elec = [0.35,0.15,0.35,0.15]  # 인구밀도, 유동인구밀도, 충전기당 전기차 수, 도로보급률
        self.weight_social_hydro = [0.35,0.15,0.35,0.15] # 인구밀도, 유동인구밀도, 충전기당 수소차 수, 도로보급률
        self.weight_economic_elec = [0.8,0.2]                    # 전기차충전기 설치비용, 평균소득
        self.weight_economic_hydro = [0.4,0.2,0.4]                       # 수소차충전기 설치비용, 평균소득, 수소차충전소 기대수익
        self.weight_technical_elec = [[0.7,0.7,0.9,0.7,1.0]]            # 충전기용량
        self.weight_technical_hydro = [[0.35,0.7],0.3]                   # 수소연료 공급방식, 최대 충전 가능한 수소차 수
        
        # 최종 확률 결합 가중치
        self.weight_total = [0.1, 0.4, 0.3, 0.2]  # 상위 요소들의 가중치(환경, 사회, 경제, 기술)

        # 상위 요소 결합 확률
        self.environment_joint_pro = 0  # 환경요소 결합 확률

        self.social_joint_pro_elec = 0  # 사회(전기) 결합 확률
        self.social_joint_pro_hydro = 0  # 사회(수소) 결합 확률

        self.economic_joint_pro_elec = 0  # 경제(전기) 결합 확률
        self.economic_joint_pro_hydro = 0  # 경제(수소) 결합 확률

        self.technical_joint_pro_elec = 0  # 기술(전기) 결합 확률
        self.technical_joint_pro_hydro = 0  # 기술(수소) 결합 확률

        # 조건부 확률 변수
        self.environment_pro, self.environment_pro_negative = 0, 0
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
            No2().t_pro,  # 이산화질소
            Ozone().t_pro,  # 이산화질소
            FineDust_pm10().t_pro,  # 미세먼지 pm2.5
            FineDust_pm25().t_pro,  # 미세먼지 pm10
        ]
        for env in environment_list:
            self.variable_environment.append(env)

    def set_soc_elec_pro(self):
        '''
        사회적 변수(전기차) 적합도 반환
        '''
        social_elec_list = [
            Density().t_pro,  # 고정인구밀도
            FloatingPopulation().t_pro,  # 유동인구밀도
            EV_per_charger().t_pro,  # 전기차충전기당 전기차 수
            Street_supply().t_pro,  # 도로보급률
        ]
        for soc in social_elec_list:
            self.variable_social_elec.append(soc)

    def set_soc_hydro_pro(self):
        social_hydro_list = [
            Density().t_pro,  # 고정인구밀도
            FloatingPopulation().t_pro,  # 유동인구밀도
            HV_per_charger().t_pro,  # 수소차충전기당 수소차 수
            Street_supply().t_pro,  # 도로보급률
        ]
        for soc in social_hydro_list:
            self.variable_social_hydro.append(soc)

    def set_eco_elec_pro(self):
        self.variable_economic_elec.append(EVCS_cost().t_pro)   # 전기차충전기 설치 비용
        self.variable_economic_elec.append(Income().t_pro)      # 주차장 구획 수

    def set_eco_hydro_pro(self):
        economic_hydro_list = [
            HVCS_cost().t_pro,  # 수소충전소 구축 비용
            Income().t_pro,     # 평균소득
            HVCS_income().t_pro # 수소충전소 기대수익
        ]
        for eco in economic_hydro_list:
            self.variable_economic_hydro.append(eco)

    def set_tech_elec_pro(self):
        self.variable_technical_elec.append(Charge_capacity().pro_list) # 충전기 용량

    def set_tech_hydro_pro(self):
        self.variable_technical_hydro.append(HVCS_type().pro_list)      # 수소연료 공급방식
        self.variable_technical_hydro.append(Maximum_charge().t_pro)    # 충전소당 공급가능 차량 수

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

class get_pro_elec(Probability):
    '''
    전기 상위요인, 최종확률 읽기
    '''

    def __init__(self):
        self.parking_file_path = dir.getdir('부산 주차장 현황.csv')
        self.df_parking = pd.read_csv(self.parking_file_path,encoing='cp949')
        self.name = []
        self.name = self.df_parking['주차장명'].tolist()
        self.start_dic = {}
        for n in self.name:
            self.result_dic[n] = [self.df_parking[self.df_parking['주차장명']==n]['경제적요인'].values[0],
                                  self.df_parking[self.df_parking['주차장명']==n]['사회적요인'].values[0],
                                  self.df_parking[self.df_parking['주차장명']==n]['환경적요인'].values[0],
                                  self.df_parking[self.df_parking['주차장명']==n]['기술적요인'].values[0],
                                  self.df_parking[self.df_parking['주차장명']==n]['최종확률'].values[0]]

class get_pro_hydro(Probability):
    '''
    수소 상위요인, 최종확률 읽기
    '''

    def __init__(self):
        self.LPG_file_path = dir.getdir('부산 LPG 충전소 현황(한국가스안전공사).csv')
        self.df_LPG = pd.read_csv(self.LPG_file_path,encoing='cp949')
        self.name = []
        self.name = self.df_LPG['업소명'].tolist()
        self.start_dic = {}
        for n in self.name:
            self.result_dic[n] = [self.df_LPG[self.df_LPG['업소명']==n]['경제적요인'].values[0],
                                  self.df_LPG[self.df_LPG['업소명']==n]['사회적요인'].values[0],
                                  self.df_LPG[self.df_LPG['업소명']==n]['환경적요인'].values[0],
                                  self.df_LPG[self.df_LPG['업소명']==n]['기술적요인'].values[0],
                                  self.df_LPG[self.df_LPG['업소명']==n]['최종확률'].values[0]]                             
        

if __name__ == '__main__':
    pro = Probability()
    pro.print_pro()
    pro.environment_joint_pro = get_joint_pro(pro.variable_environment, pro.weight_environment)
    pro.social_joint_pro_elec = get_joint_pro(pro.variable_social_elec, pro.weight_social_elec)
    pro.social_joint_pro_hydro = get_joint_pro(pro.variable_social_hydro, pro.weight_social_hydro)
    pro.economic_joint_pro_elec = get_joint_pro(pro.variable_economic_elec, pro.weight_economic_elec)
    pro.economic_joint_pro_hydro = get_joint_pro(pro.variable_economic_hydro, pro.weight_economic_hydro)
    pro.technical_joint_pro_elec = get_joint_pro(pro.variable_technical_elec, pro.weight_technical_elec)
    pro.technical_joint_pro_hydro = get_joint_pro(pro.variable_technical_hydro, pro.weight_technical_hydro)

    # print(f"결합 확률: {pro.environment_joint_pro}")
    # print(f"결합 확률: {pro.social_joint_pro_elec}")
    # print(f"결합 확률: {pro.social_joint_pro_hydro}")
    # print(f"결합 확률: {pro.economic_joint_pro_elec}")
    # print(f"결합 확률: {pro.technical_joint_pro_elec}")
    # print(f"결합 확률: {pro.technical_joint_pro_elec}")
    # print(f"결합 확률: {pro.technical_joint_pro_hydro}")

    pro.environment_pro, pro.environment_pro_negative = conditional_pro(pro.weight_environment)
    pro.social_elec_pro, pro.social_elec_pro_negative = conditional_pro(pro.weight_social_elec)
    pro.social_hydro_pro, pro.social_hydro_pro_negative = conditional_pro(pro.weight_social_hydro)
    pro.economic_elec_pro, pro.economic_elec_pro_negative = conditional_pro(pro.weight_economic_elec)
    pro.economic_hydro_pro, pro.economic_hydro_pro_negative = conditional_pro(pro.weight_economic_hydro)
    pro.technical_elec_pro, pro.technical_elec_pro_negative = conditional_pro(pro.weight_technical_elec)
    pro.technical_hydro_pro, pro.technical_hydro_pro_negative = conditional_pro(pro.weight_technical_hydro)

    # print(pro.environment_pro, pro.environment_pro_negative)
    # print(pro.social_elec_pro, pro.social_elec_pro_negative)
    # print(pro.social_hydro_pro, pro.social_hydro_pro_negative)
    # print(pro.economic_elec_pro, pro.economic_elec_pro_negative)
    # print(pro.economic_hydro_pro, pro.economic_hydro_pro_negative)
    # print(pro.technical_elec_pro, pro.technical_elec_pro_negative)
    # print(pro.technical_hydro_pro, pro.technical_hydro_pro_negative)
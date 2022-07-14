import pandas as pd
from Module import init as dir
from Module.Social import Social, Population, FloatingPopulation


class Technical:
    """
    기술적 요소 모델링
    """

    @staticmethod
    def check_location(location, x, y):
        '''
        LPG 충전소 여부 판단.
        '''
        if (x, y) in location:
            complex_cs_pro = 1.0
        else:
            complex_cs_pro = 0.0

        return complex_cs_pro

    @staticmethod
    def charge_type(foottraffic_pro, busan_people_pro):
        '''
        foottraffic_pro : 유동인구 적합도
        busan_people_pro : 고정인구 적합도
        charger_pro : 설정하고자 하는 충전기 타입의 적합도 비율 초기값(0~1)
        '''

        # 급속 충전기 초기 확률:0.38
        charger_pro = 0.38

        if foottraffic_pro >= busan_people_pro:
            charger_type = 'Fast Charge'
        else:
            charger_type = 'Standard Charge'

        # 유동인구와 기존인구와 차이가 나는 만큼 더 많은 확률 부여
        if foottraffic_pro >= busan_people_pro:
            charger_type = 'Fast Charge'
            diff = foottraffic_pro - busan_people_pro
            charger_pro += diff
            if charger_pro > 1:
                charger_pro = 1.0
        elif foottraffic_pro < busan_people_pro:
            charger_type = 'Standard Charge'
            diff = busan_people_pro - foottraffic_pro
            charger_pro -= diff
            if charger_pro < 0:
                charger_pro = 0.0

        return charger_type, charger_pro, 1 - charger_pro


class Complex_charging_station(Technical):
    '''
    복합 충전소 여부
    '''

    def __init__(self):
        self.file_path = dir.getdir("부산 LPG 충전소 현황.csv")  # 데이터 경로
        self.df_lpg = pd.read_csv(self.file_path, encoding='cp949')
        self.df_lpg = self.df_lpg[self.df_lpg['면적'] >= 1500].reset_index(drop=True)
        self.location = list(zip(self.df_lpg['위도'].tolist(), self.df_lpg['경도'].tolist()))
        self.complex_cs_pro = Technical.check_location(self.location, 35.18601331, 129.0559741)


class Charging_time(Technical):
    '''
    기술적 요소 - 충전시간에 따른 충전방식
    '''

    def __init__(self):
        self.population = Population()
        self.population_pro = self.population.t_pro
        self.fpopulation = FloatingPopulation()
        self.fpopulation_pro = self.fpopulation.t_pro
        self.charger_type, self.t_pro, self.f_pro = Technical.charge_type(self.fpopulation_pro, self.population_pro)

if __name__ == '_main__':
    ccs = Complex_charging_station()
    charging_time = Charging_time()

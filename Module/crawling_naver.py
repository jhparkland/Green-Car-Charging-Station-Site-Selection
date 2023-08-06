# import pandas as pd
# import numpy as np
# import requests
# import json
# import time

# def get_sido_info():
#     down_url = 'https://new.land.naver.com/api/regions/list?cortarNo=0000000000'
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.1065474,128.9790545,15&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&ad=true",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp=json.loads(r.text)
#     temp=list(pd.DataFrame(temp["regionList"])["cortarNo"])
#     return temp

# def get_gungu_info(sido_code):
#     down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+sido_code
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.104476,128.974763,14&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&ad=true",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp=json.loads(r.text)
#     temp=list(pd.DataFrame(temp['regionList'])["cortarNo"])
#     return temp

# def get_dong_info(gungu_code):
#     down_url = 'https://new.land.naver.com/api/regions/list?cortarNo='+gungu_code
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.104476,128.974763,14&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&ad=true",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp=json.loads(r.text)
#     temp=list(pd.DataFrame(temp['regionList'])["cortarNo"])
#     return temp

# def get_article_info(articleNo):
#     down_url = 'https://new.land.naver.com/api/articles/'+articleNo+'?complexNo='
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.102949,128.976663,16&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&ad=true&articleNo="+articleNo,
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp=json.loads(r.text)
#     return temp

# def get_apt_list(dong_code):
#     down_url = 'https://new.land.naver.com/api/cortars?zoom=16&cortarNo='+dong_code
#     r = requests.get(down_url,data={"sameAddressGroup":"false"},headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.1111,128.9537,16&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp=json.loads(r.text)
#     try:
#         temp=list(pd.DataFrame(temp['articleList'])["articleNo"])
#     except:
#         temp=[]
#     return temp

# def get_school_info(articleNo):
#     down_url = 'https://new.land.naver.com/api/articles/'+articleNo+'/schools'
#     r = requests.get(down_url,headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/articles/"+articleNo+"?ms=37.482968,127.0634,16&a=APT&b=A1&e=RETAIL",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp_school=json.loads(r.text)
#     return temp_school

# ##################가격정보
# def article_price(articleNo):
#     down_url = 'https://new.land.naver.com/api/articles/'+articleNo+'?complexNo='
#     r = requests.get(down_url,headers={
#         "Accept-Encoding": "gzip",
#         "Host": "new.land.naver.com",
#         "Referer": "https://new.land.naver.com/rooms?ms=35.102949,128.976663,16&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&articleNo="+articleNo,
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-origin",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.49"
#     })
#     r.encoding = "utf-8-sig"
#     temp_price=json.loads(r.text)
#     return temp_price

# sido_list=get_sido_info() 

# for m in range(len(sido_list)):
#     gungu_list=get_gungu_info(sido_list[m])
#     gungu_apt_list=[0]*len(gungu_list)
#     for j in range(len(gungu_list)):    #구 마다 하나씩 저장
#         dong_list=get_dong_info(gungu_list[j])
#         dong_apt_list=[0]*len(dong_list)
#         for k in range(len(dong_list)):     #동마다 하나씩 저장
#             article_list=get_apt_list(dong_list[k])
#             article_list_data=[0]*len(article_list)
#             temp_data=pd.DataFrame(index=range(len(article_list)))
#             for i in range(len(article_list)):  #매물마다 하나씩 저장
#                 temp=get_article_info(article_list[i])
#                 print(temp["articleDetail"]["exposureAddress"],temp["complexDetail"]["complexName"])
#                 temp_data.loc[i,"articleId"]=temp['articleDetail']["articleNo"]
#                 temp_data.loc[i,"매물명"]=temp["aricleDetail"]["articleName"]
#                 temp_data.loc[i,"시"]=temp["articleDetail"]["cityName"]
#                 temp_data.loc[i,"구"]=temp["articleDetail"]["divisionName"]
#                 temp_data.loc[i,"동"]=temp["articleDetail"]["sectionName"]
#                 temp_data.loc[i,"법정동주소"]=temp["aricleDetail"]["exposureAddress"]
#                 temp_data.loc[i,"호실"]=temp["articleDetail"]["etcAddress"]
#                 temp_data.loc[i,"latitude"]=temp["aricleDetail"]["latitude"]
#                 temp_data.loc[i,"longitude"]=temp["aricleDetail"]["longitude"]
#                 if temp["aricleDetail"]["detailAddressYn"] == "Y":
#                     temp_data.loc[i,"상세주소"]=temp["aricleDetail"]["detailAddress"]
#                 else:
#                     temp_data.loc[i,"상세주소"]=""
#                 try:
#                     temp_data.loc[i,"용적률"]=temp["aricleDetail"]["batlRatio"]
#                 except KeyError:
#                     temp_data.loc[i,"용적률"]=""
#                 try:
#                     temp_data.loc[i,"건폐율"]=temp["aricleDetail"]["btlRatio"]
#                 except KeyError:
#                     temp_data.loc[i,"건폐율"]=""
#                 try:
#                     temp_data.loc[i,"주차대수"]=temp["aricleDetail"]["parkingPossibleCount"]
#                 except KeyError:
#                     temp_data.loc[i,"주차대수"]=""
#                 try:
#                     temp_data.loc[i,"건설사"]=temp["aricleDetail"]["constructionCompanyName"]
#                 except KeyError:   
#                     temp_data.loc[i,"건설사"]=""
#                 try:
#                     temp_data.loc[i,"난방"]=temp["aricleDetail"]["heatMethodTypeCode"]
#                 except KeyError:   
#                     temp_data.loc[i,"난방"]=""
#                 try:
#                     temp_data.loc[i,"공급면적"]=temp["articleSpace"]["supplySpace"]
#                 except KeyError:   
#                     temp_data.loc[i,"공급면적"]=""
#                 try:
#                     temp_data.loc[i,"전용면적"]=temp["articleSpace"]["exclusiveSpace"]
#                 except KeyError:   
#                     temp_data.loc[i,"전용면적"]=""
#                 try:
#                     temp_data.loc[i,"전용율"]=temp["articleSpace"]["exclusiveRate"]
#                 except KeyError:   
#                     temp_data.loc[i,"전용율"]=""
#                 try:
#                     temp_data.loc[i,"방수"]=temp["aricleDetail"]["roomCount"]
#                 except KeyError:   
#                     temp_data.loc[i,"방수"]=""
#                 try:
#                     temp_data.loc[i,"욕실수"]=temp["aricleDetail"]["bathroomCount"]
#                 except KeyError:   
#                     temp_data.loc[i,"욕실수"]=""
#                 try:
#                     temp_data.loc[i,"거래방식"]=temp["aricleDetail"]["tradeTypeName"]
#                 except KeyError:
#                     temp_data.loc[i,"거래방식"]=""
#                 try:
#                     temp_data.loc[i,"월세"]=temp["articlePrice"]["rentPrice"]
#                 except KeyError:   
#                     temp_data.loc[i,"월세"]=""
#                 try:
#                     temp_data.loc[i,"보증금"]=temp["articlePrice"]["warrantPrice"]
#                 except KeyError:   
#                     temp_data.loc[i,"보증금"]=""
#                 try:
#                     temp_data.loc[i,"전세"]=temp["articlePrice"]["allRentPrice"]
#                 except KeyError:   
#                     temp_data.loc[i,"전세"]=""
#                 try:
#                     temp_data.loc[i,"관리비"]=temp["aricleDetail"]["montlyManagementCost"]
#                 except KeyError:   
#                     temp_data.loc[i,"관리비"]=""
#                 try:
#                     temp_data.loc[i,"건물타입"]=temp['articleDetail']["buildingTypeName"]
#                 except KeyError:   
#                     temp_data.loc[i,"건물타입"]=""
#                 try:
#                     temp_data.loc[i,"복층여부"]=temp['articleDetail']["floorLayerName"]
#                 except KeyError:   
#                     temp_data.loc[i,"복층여부"]=""
#                 try:
#                     temp_data.loc[i,"시설분류"]=temp['articleBuildingRegister']["mainPurpsCdNm"]
#                 except KeyError:   
#                     temp_data.loc[i,"시설분류"]=""    
#                 try:
#                     temp_data.loc[i,"최대층수"]=temp['articleFloor']["totalFloorCount"]
#                 except KeyError:   
#                     temp_data.loc[i,"최대층수"]=""
#                 try:
#                     temp_data.loc[i,"건축시기"]=temp['articleBuildingRegister']["useAprDay"]
#                 except KeyError:   
#                     temp_data.loc[i,"건축시기"]=""
#                 try:
#                     temp_data.loc[i,"방향"]=temp['articleAddition']["direction"]
#                 except KeyError:   
#                     temp_data.loc[i,"방향"]=""
#                 try:
#                     temp_data.loc[i,"주차가능여부"]=temp['aricleDetail']["parkingPossibleYN"]
#                 except KeyError:   
#                     temp_data.loc[i,"주차가능여부"]=""
#                 try:
#                     temp_data.loc[i,"총주차대수"]=temp['aricleDetail']["parkingCount"]
#                 except KeyError:   
#                     temp_data.loc[i,"총주차대수"]=""

#                     time.sleep(1)
#                 article_list_data[i]=temp_data
#             if article_list_data==[]:
#                 dong_apt_list[k]=pd.DataFrame(columns=temp_data.columns)
#             else:
#                 dong_apt_list[k]=pd.concat(article_list_data)
#         gungu_apt_list[j]=pd.concat(dong_apt_list)
#     final_data=pd.concat(gungu_apt_list)
#     final_data.to_csv("crawling_data.csv",encoding="CP949")
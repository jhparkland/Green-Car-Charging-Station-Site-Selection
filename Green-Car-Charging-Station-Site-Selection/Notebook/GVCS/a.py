import b

df_ozone, ozen_col = b.temp() # 프론트 코드


b.advanced_replace(df_ozone, df_ozone.iloc[:,2:].columns.tolist(), '-', r'[^0-9.0-9]')


df_ozone = b.temp2(df_ozone) # 프론트 코드


mean = df_ozone.iloc[:,2].mean()
std = df_ozone.iloc[:,2].std()
min = df_ozone.iloc[:,2].min()
max = df_ozone.iloc[:,2].max()
b.show_norm(mean,std,min,max) 

busan_oz = df_ozone[df_ozone['구분(2)']=='부산광역시'].loc[2,'2021.07']
b.cal_norm(mean,std,min,max,busan_oz)
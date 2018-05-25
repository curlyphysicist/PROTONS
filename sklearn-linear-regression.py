
# --- МОДЕЛЬ ЛИНЕЙНОЙ РЕГРЕССИИ --- #

import numpy as np  
import scipy as sp
import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import sklearn.metrics

import os

# ------------------------------------------------------------- #

print('Введите каналы (10, 30, 50, 100) через пробел')
ch = input()
channels = ch.split(' ')
channels = [int(c) for c in channels]
print('Введите горизонт прогноза (1 - 6) через пробел')
t = input()
time = t.split(' ')
time = [int(h) for h in time]

#JSONparam = "../models/FINAL_EVENTS/LINEAR-REGRESS-Ph15+DST-%sh-%sMeV.json" % (time, channels)       # saving the model
#H5bestparam = "../models/FINAL_EVENTS/LINEAR-REGRESS-Ph15+DST-best-%sh-%sMeV.h5" % (time, channels)  # saving the weights of the BEST model

file = '../прогнозы/FINAL_EVENTS/LINEAR-REGRESS-Ph15+DST-%sMeV-%sh.csv' % (channels, time)      # PPh15 - protons, parameters, hours, 15min.
#info = '../прогнозы/FINAL_EVENTS/LINEAR-REGRESS-Ph15+DST-%sMeV-%sh.txt' % (channels, time)   # Для записи статистики в процессе обучения
                                                                           # Using part of data, change the filename: PPh15, Ph15, PPh, Ph                                                                           
# ------------------------------------------------------------- #

#Selected events
fopen = pd.read_csv("../EVENTS_FINAL_10MEV.csv")      # файл отобранных СПС
train = pd.DataFrame(fopen[1872:14478])       # 1999 - 2006 (вкл 2006)
val = pd.DataFrame(fopen[14771:21662])        # 2010 - 2015 (выкл 2015)
test = pd.DataFrame(fopen[21663:23180])       # 2015 - 2017

#----------------------------------------------------------------------------------------------#
# P + DST      HOURS + 15min            =   126 ВХОДОВ
array = [32, 59, 86, 113, 140, 167]     # массив из номеров столбцов, которые пойдут в массивы обучающих данных
cnt = 0
for cnt in range(35,55):                # без учёта данных за "сейчас"
    array.append(cnt)
for cnt in range(62,82):   
    array.append(cnt)
for cnt in range(89,109):   
    array.append(cnt)             
for cnt in range(116,136):   
    array.append(cnt)
for cnt in range(143,163):   
    array.append(cnt)
for cnt in range(170,190):   
    array.append(cnt)
#----------------------------------------------------------------------------------------------#
k = 0                                         # номера столбцов, которые я прогнозирую (лучше по отдельности, не "мульти-горизонт")
aim = []               
for h  in time:
    if 10 in channels:
        aim.append(28+27*(h-1))
        k+=1
    if 30 in channels:
        aim.append(29+27*(h-1))
        k+=1
    if 50 in channels:
        aim.append(30+27*(h-1))
        k+=1
    if 100 in channels:
        aim.append(31+27*(h-1))
        k+=1
#----------------------------------------------------------------------------------------------#
y_train = np.array(train[aim])           
x_train = np.array(train[array])
y_test = test[aim]         
x_test =  np.array(test[array])
x_val = np.array(val[array])
y_val = np.array(val[aim])

print(array)                                  # Проверка, что столбцы, которые ты прогнозируешь, не появляются в обучающих 
print(aim)
print(train[aim])

scalerX = StandardScaler().fit(x_train)       # Шкалирование данных к виду [0, 1]
scalerY = StandardScaler().fit(y_train)
x_train_scaled = scalerX.transform(x_train)
y_train_scaled = scalerY.transform(y_train)
x_test_scaled = scalerX.transform(x_test)
x_val_scaled = scalerX.transform(x_val)
y_val_scaled = scalerY.transform(y_val)

# ------------------------------------------------------------- #

# Mодель линейной регрессии в sklearn
model = sklearn.linear_model.LinearRegression(fit_intercept=True, normalize=True, copy_X=True, n_jobs=-1)
model.fit(x_train_scaled, y_train_scaled)
params = model.get_params()
print(params)

predicted = pd.DataFrame(model.predict(x_test_scaled))
predicted = pd.DataFrame(scalerY.inverse_transform(predicted)) 

#----------------------------------------------------------------------------------------------#
# Запись в файл: datetime + прогноз + контрольные значения
cols_to_mantain = ['year', 'month', 'day', 'hour_from']
to_csv = test[cols_to_mantain]
to_csv = to_csv.merge(y_test, left_index=True, right_index=True, suffixes=['', ''])
to_csv = to_csv.reset_index(drop=True)
to_csv = to_csv.merge(predicted, how='left', left_index=True, right_index=True, suffixes=['', ''])

pd.DataFrame.to_csv(to_csv, file, index=False)

# ----- ОТРИСОВКА ПРОГНОЗ + КОНТРОЛЬНЫЕ ЗНАЧЕНИЯ ----- #
 
data = pd.read_csv(file, sep=',')
index = data.index
forecast = data.iloc[:, 5]
control = data.iloc[:, 4]
datetimearr = []
'''
for i in range (0, len(data)):
    k = str(int(data.loc[i, 'day'])) + '.' + str(int(data.loc[i, 'month'])) + '.' + str(int(data.loc[i, 'year'])) + ' ' + str(int(data.loc[i, 'hour_from'])) + ':00'
    k = dt.datetime.strptime(k, "%d.%m.%Y %H:%M")
    datetimearr.append(k)

plt.plot(datetimearr, forecast, datetimearr, control) 
plt.grid()
plt.legend(['forecast', 'control'])
plt.xlabel('time')
plt.ylabel('logarifm of proton flux')
plt.title('data: selected (protons+parameters)')
plt.show()
'''
ev_pred = np.ravel(forecast.transpose())
ev_cont = np.ravel(control.transpose())
# Статистика по экзаменационному набору (по расшкалированным данным)
print('LINEAR REGRESS Forecast protons+params',ch, 'MeV, horizon',h,'h')
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(ev_pred, ev_cont)
print('Mean squared error:', round(mse,4))
from sklearn.metrics import mean_absolute_error
mae = mean_absolute_error(ev_pred, ev_cont)
print('Mean absolute error:', round(mae,4))
from sklearn.metrics import r2_score
r2 = r2_score(ev_cont, ev_pred)   
print('R-squared:', round(r2,4))
matrix = data.iloc[:, 4:6]
correl_matrix = round(matrix.corr(),4)
print('Correlation matrix:')
print(correl_matrix)


# --- НЕЙРОННАЯ СЕТЬ (ПРОГНОЗ) --- #

import numpy as np  
import scipy as sp
import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import tensorflow as tf

import keras
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import keras.backend as K
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

from keras.models import model_from_json
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


JSONparam = "../models/params/FINAL_EVENTS/Ph15+DST-%sh-%sMeV.json" % (time, channels)
H5bestparam = "../models/params/FINAL_EVENTS/Ph15+DST-best-%sh-%sMeV.h5" % (time, channels)

file = '../прогнозы/FINAL_EVENTS/Ph15+DST-%sMeV-%sh.csv' % (channels, time)

#figure = ('../картинки/FORECAST/Ph15+DST-%s-MeV-%s-h.png') % (ch, t)           # строим прогноз + контрольные от времени
#scatter = ('../картинки/FORECAST/Ph15+DST-%s-MeV-%s-h(sc).png') % (ch, t)      # строим прогноз от контрольных

# ------------------------------------------------------------- #

#Selected events
fopen = pd.read_csv("../EVENTS_FINAL_10MEV.csv")      # файл отобранных СПС
train = pd.DataFrame(fopen[1872:14478])       # 1999 - 2006 (вкл 2006)
val = pd.DataFrame(fopen[14771:21662])        # 2010 - 2015 (выкл 2015)
test = pd.DataFrame(fopen[21663:23180])       # 2015 - 2017
'''
#Full data
fopen = pd.read_csv("../PROTONS_FINAL_DEEP6.csv")    # данные с фоном
train = pd.DataFrame(fopen[9482:80616])       # 1999 - 2006
val = pd.DataFrame(fopen[106922:150744])      # 2010 - 2015
test = pd.DataFrame(fopen[150746:174660])     # 2015 - 2017
'''
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

y_train = np.array(train[aim])                 # Шкалирование данных          
x_train = np.array(train[array])
y_test = test[aim]         
x_test =  np.array(test[array])

scalerX = StandardScaler().fit(x_train)
scalerY = StandardScaler().fit(y_train)
x_test_scaled = scalerX.transform(x_test)

#----------------------------------------------------------------------------------------------#
# Загружаем обученную сетку

json_file = open(JSONparam, "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(H5bestparam)

loaded_model.compile(loss='mse', optimizer='rmsprop', metrics = ['mse','acc'])

predicted = pd.DataFrame(loaded_model.predict(x_test_scaled))
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
col_c = ('P>%s_future%sh') % (ch, str(int(t)-1))
forecast = data.loc[:, '0']  
control = data.loc[:, col_c]
datetimearr = []

ev_pred = np.ravel(forecast.transpose())
ev_cont = np.ravel(control.transpose())

# Статистика по экзаменационному набору (по расшкалированным данным)
print('Forecast protons+params',ch, 'MeV, horizon',h,'h')
print('Used data:', file)
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

'''

for i in range (0, len(data)):
    k = str(int(data.loc[i, 'day'])) + '.' + str(int(data.loc[i, 'month'])) + '.' + str(int(data.loc[i, 'year'])) + ' ' + str(int(data.loc[i, 'hour_from'])) + ':00'
    k = dt.datetime.strptime(k, "%d.%m.%Y %H:%M")
    datetimearr.append(k)

# Compare forecast with control
plt.plot(datetimearr, forecast, datetimearr, control) 
plt.grid()
plt.legend(['forecast', 'control'])
plt.xlabel('time')
plt.ylabel('logarifm of proton flux')
plt.title(('Protons %s MeV, horizon %sh') % (ch, t))
plt.suptitle('data: selected (protons+param)')
plt.savefig(figure, format='png')
plt.show()

# Scatterplot
plt.plot(forecast,control,'m.')
plt.title('Диаграмма разброса (scatterplot)')
plt.suptitle('data: selected (protons+param)')
plt.xlabel('forecast')
plt.ylabel('control')
plt.grid()
#plt.savefig(scatter, format='png')
plt.show()
'''


# --- НЕЙРОННАЯ СЕТЬ (ОБУЧЕНИЕ) --- #

import numpy as np  
import scipy as sp
import pandas as pd 
import datetime as dt
import matplotlib.pyplot as plt
import tensorflow as tf

import keras
from keras import metrics
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import keras.backend as K
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import sklearn.metrics

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


JSONparam = "../models/params/FINAL_EVENTS/Ph15+DST-%sh-%sMeV.json" % (time, channels)       # saving the model
H5bestparam = "../models/params/FINAL_EVENTS/Ph15+DST-best-%sh-%sMeV.h5" % (time, channels)  # saving the weights of the BEST model

file = '../прогнозы/FINAL_EVENTS/Ph15+DST-%sMeV-%sh.csv' % (channels, time)      # PPh15 - protons, parameters, hours, 15min.
#info = '../прогнозы/FINAL_EVENTS/Ph15+DST-%sMeV-%sh.txt' % (channels, time)   # Для записи статистики в процессе обучения
                                                                           # Using part of data, change the filename: PPh15, Ph15, PPh, Ph                                                                           
# ------------------------------------------------------------- #
# В Keras нет функции расчёта R^2, вводим её авторскую :)
from keras import backend as K

def r2(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    r2 = 1 - SS_res/(SS_tot + K.epsilon())
    return r2
# ------------------------------------------------------------- #

#Selected events
fopen = pd.read_csv("../EVENTS_FINAL_10MEV.csv")      # файл отобранных СПС
train = pd.DataFrame(fopen[1872:14478])       # 1999 - 2006 (вкл 2006)
val = pd.DataFrame(fopen[14771:21662])        # 2010 - 2015 (выкл 2015)
test = pd.DataFrame(fopen[21663:23180])       # 2015 - 2017
'''
#Full data
#fopen = pd.read_csv("../PROTONS_FINAL_DEEP6.csv")    # данные с фоном
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
y_train = np.array(train[aim])           
x_train = np.array(train[array])
y_test = test[aim]         
x_test =  np.array(test[array])
x_val = np.array(val[array])
y_val = np.array(val[aim])

print(array)                                  # Проверь, что столбцы, которые ты прогнозируешь, не появляются в обучающих
print(aim)
print(train[array])
print(train[aim])

scalerX = StandardScaler().fit(x_train)       # Шкалирование данных
scalerY = StandardScaler().fit(y_train)
x_train_scaled = scalerX.transform(x_train)
y_train_scaled = scalerY.transform(y_train)
x_test_scaled = scalerX.transform(x_test)
x_val_scaled = scalerX.transform(x_val)
y_val_scaled = scalerY.transform(y_val)

# ------------------------------------------------------------- #
# Mногослойный персептрон в Keras
model = Sequential()
model.add(Dense(80, input_dim=126, kernel_initializer='normal', activation='sigmoid'))
model.add(Dense(10, kernel_initializer='normal', activation='sigmoid'))
model.add(Dense(k, kernel_initializer='normal', activation='linear'))
model.compile(loss='mse', optimizer='rmsprop', metrics = [r2, metrics.mse, metrics.mae])

SaveTheBest = keras.callbacks.ModelCheckpoint(H5bestparam, monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=True, mode='auto', period=1)

# Если будешь обучать циклами, не комментируй fit на стр.118. Можешь сделать epochs=10, чтобы просто файл модели создался
history = model.fit(x_train_scaled, y_train_scaled, batch_size=80, epochs=1000, validation_data=(x_val_scaled, y_val_scaled), callbacks=[SaveTheBest]) 

model_json = model.to_json()                # Запись модели
with open(JSONparam, "w") as json_file:
        json_file.write(model_json)

'''
#f = open(info, 'w')    # Запись статистики в процессе обучения

#Для построения зависимости MSE от эпох (чтобы понять, правильно ли обучается сеть)
ep = []
for e in range (1,1001):
    ep.append(e)


# Обучение 5 циклами по 200 эпох для того, чтобы раз в 200 эпох выводить трен и валид статистику по расшкалированным данным

cycle = 0   
for cycle in range (1,6):

    json_file = open(JSONparam, "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(H5bestparam)
    loaded_model.compile(loss='mse', optimizer='rmsprop', metrics = [r2, metrics.mse, metrics.mae])

    history = loaded_model.fit(x_train_scaled, y_train_scaled, batch_size=80, epochs=200, validation_data=(x_val_scaled, y_val_scaled), callbacks=[SaveTheBest]) 
    
    # Здесь мы просто берём трен.набор в качестве экз. и прогнозируем его. И считаем статистику.
    pred_tr = pd.DataFrame(loaded_model.predict(x_train_scaled))
    pred_tr = pd.DataFrame(scalerY.inverse_transform(pred_tr))
    f.write('Cycle '); f.write(str(cycle)); f.write('\n')
    f.write('TRAIN\n')
    f.write('Protons '); f.write(str(ch)); f.write('MeV, horizon'); f.write(str(h)); f.write('h\n')
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(pred_tr, y_train)
    f.write('Mean squared error:'); f.write(str(round(mse,4))); f.write('\n')
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(pred_tr, y_train)
    f.write('Mean average error:'); f.write(str(round(mae,4))); f.write('\n')
    from sklearn.metrics import r2_score
    r2 = r2_score(pred_tr, y_train)   
    f.write('R-squared:'); f.write(str(round(r2,4))); f.write('\n')

    # Прогнозируем валидац.набор
    pred_val = pd.DataFrame(loaded_model.predict(x_val_scaled))
    pred_val = pd.DataFrame(scalerY.inverse_transform(pred_val))
    f.write('VAL\n')
    f.write('Protons '); f.write(str(ch)); f.write('MeV, horizon'); f.write(str(h)); f.write('h\n')
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(pred_val, y_val)
    f.write('Mean squared error:'); f.write(str(round(mse,4))); f.write('\n')
    from sklearn.metrics import mean_absolute_error
    mae = mean_absolute_error(pred_val, y_val)
    f.write('Mean average error:'); f.write(str(round(mae,4))); f.write('\n')
    from sklearn.metrics import r2_score
    r2 = r2_score(pred_val, y_val)   
    f.write('R-squared:'); f.write(str(round(r2,4))); f.write('\n\n')
   
f.close()
'''
'''
# Загружаем модель, чтобы сделать прогноз уже экз набора
json_file = open(JSONparam, "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights(H5bestparam)
     
loaded_model.compile(loss='mse', optimizer='rmsprop', metrics = [r2, metrics.mse, metrics.mae])

predicted = pd.DataFrame(loaded_model.predict(x_test_scaled))
predicted = pd.DataFrame(scalerY.inverse_transform(predicted))
'''
predicted = pd.DataFrame(model.predict(x_test_scaled))
predicted = pd.DataFrame(scalerY.inverse_transform(predicted)) 

print('This was the forecast of protons',ch,'MeV, horizon', t,  'h')
print('Used data:', file)
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
# MSE от номера эпохи в процессе тренировки сети
# Правильное поведение коэф-тов: MSE, MAE на трен. наборе убывают с ростом эпохи, на валидац. наборе убывают, а затем начинают расти
plt.plot(ep, history.history['mean_squared_error'])
plt.title('MSEtrain')
plt.grid()
plt.savefig('MSEtrain.png', format='png')
plt.show()
'''

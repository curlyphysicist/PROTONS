
# --- ПОГРУЖЕНИЕ ДАННЫХ (СДВИГ СТОЛБЦОВ ВНИЗ-погружение/ВВЕРХ-прогнозируемые значения) --- #

import pandas as pd

filename = '../PROTONS_FINAL.csv' 
filepath = '../PROTONS_FINAL_DEEP6.csv'
time_delay = 6                                          # глубина погружения
#-----------------------------------------------------------------------------------#
data = pd.read_csv(filename, sep=',')

data.columns = ['year', 'month', 'day', 'hour_from', 'hour_to', 'Dst', 'B_magn', 'B_gsm_z', 'P>10', 'P>10time15', 'P>10time30', 'P>10time45', 'P>10time60', 'P>30', 'P>30time15', 'P>30time30', 'P>30time45', 'P>30time60', 'P>50', 'P>50time15', 'P>50time30', 'P>50time45', 'P>50time60', 'P>100', 'P>100time15', 'P>100time30', 'P>100time45', 'P>100time60']

cols_to_mantain = ['year', 'month', 'day', 'hour_from', 'hour_to']
cols_to_deep = ['Dst', 'B_magn', 'B_gsm_z', 'P>10', 'P>10time15', 'P>10time30', 'P>10time45', 'P>10time60', 'P>30', 'P>30time15', 'P>30time30', 'P>30time45', 'P>30time60', 'P>50', 'P>50time15', 'P>50time30', 'P>50time45', 'P>50time60', 'P>100', 'P>100time15', 'P>100time30', 'P>100time45', 'P>100time60']
cols_to_antideep = ['P>10',	'P>30', 'P>50', 'P>100']
#----------------------------------------------------------------------------------------#

new_data = data[cols_to_mantain]                        # оставляем старые колонки 1 раз

for i in range(time_delay+1):                           # от нуля до нужного числа погружений
    chunk = data[cols_to_deep].shift(i)                 # остальные каждый раз сдвигаем на i
    antichunk = data[cols_to_antideep].shift(-i)        # будущее каждый раз сдвигаем на -i
    chunk.columns = list(map(lambda x: '%s_deep%sh' % (x,i), chunk.columns))
    antichunk.columns = list(map(lambda x: '%s_future%sh' % (x,i), antichunk.columns))
    new_data = new_data.merge(chunk, left_index=True, right_index=True, suffixes=['', ''])
    new_data = new_data.merge(antichunk, left_index=True, right_index=True, suffixes=['', ''])

new_data.to_csv(filepath, index=False)




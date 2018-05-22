
# --- ДОБАВЛЕНИЕ В ФАЙЛ ДАННЫХ СТОЛБЦОВ ТИПА DATETIME / ЛОГАРИФМИРОВАНИЕ ДАННЫХ --- #

import pandas as pd
import math

#----------------------------------------------------------------------------------------------#
filename = '../EVENTS_FINAL_10MEV.csv'
logfile = '../EVENTS_FINAL_10MEV_LOG.csv'
datefile = '../EVENTS_FINAL_10MEV_DATETIME.csv'
#-------------------------------------------------------------------------#
data = pd.read_csv(filename, sep=',')

# ЛОГАРИФМИРОВАНИЕ
cols = ['P>10','P>10time15','P>10time30','P>10time45','P>10time60','P>30','P>30time15','P>30time30','P>30time45','P>30time60','P>50','P>50time15','P>50time30','P>50time45','P>50time60','P>100','P>100time15','P>100time30','P>100time45','P>100time60']
for i in range (0, len(data)):
    for j in cols:
        try:
            data.loc[i, j] = round(math.log(data.loc[i, j]), 4)
        except:
            continue   
data.to_csv(logfile, index=False) 

# DATETIME
i = 0
for i in range (0, len(data)):
    data.loc[i, 'datetime'] = str(data.loc[i, 'day']) + '-' + str(data.loc[i, 'month']) + '-' + str(data.loc[i, 'year']) + ' ' + str(data.loc[i, 'hour_from']) + ':00'
    print(i)

data.to_csv(datefile, index=False)

#----------------------------------------------------------------------------------------------#

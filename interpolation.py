
# --- ЗАПОЛНЕНИЕ ПРОПУСКОВ В ДАННЫХ ЛИНЕЙНОЙ ИНТЕРПОЛЯЦИЕЙ --- #

import pandas as pd
import numpy as np
import math

#----------------------------------------------------------------------------------------------#
filename = '../protons-GOES/filin(log).csv'
filepath = '../filin(log,interpolated).csv'
#--------------------------------------------------#
data = pd.read_csv(filename, sep=',')
cols = ['P>10','P>10time15','P>10time30','P>10time45','P>10time60','P>30','P>30time15','P>30time30','P>30time45','P>30time60','P>50','P>50time15','P>50time30','P>50time45','P>50time60','P>100','P>100time15','P>100time30','P>100time45','P>100time60']
#cols = ['year', 'month', 'day', 'hour', 'Dst', 'Kp*10', 'AE', 'B_rtn_r_MAG', 'B_rtn_t_MAG', 'B_rtn_n_MAG', 'B_gse_x_MAG', 'B_gse_y_MAG', 'B_gse_z_MAG', 'B_gsm_x_MAG', 'B_gsm_y_MAG', 'B_gsm_z_MAG', 'B_magnitude_MAG', 'H_den_SWP', 'He_ratio_SWP', 'SW_spd_SWP', 'Trr_SWP', 'P>10','P>10time15','P>10time30','P>10time45','P>10time60','P>30','P>30time15','P>30time30','P>30time45','P>30time60','P>50','P>50time15','P>50time30','P>50time45','P>50time60','P>100','P>100time15','P>100time30','P>100time45','P>100time60']
#cols = ['P_10', 'P_30', 'P_50', 'P_100']
#--------------------------------------------------#

for j in cols:
    test = pd.Series(data[j])
    test = test.interpolate()
    data[j] = test

data.to_csv(filepath, index=False)
#----------------------------------------------------------------------------------------------#


# --- ФОРМИРОВАНИЕ ВЫБОРКИ ДАННЫХ ПО ПОТОКУ ПРОТОНОВ ИЗ ДАННЫХ В ФОРМАТЕ GOES --- #
# --- ФОРМАТ ДО 1997г --- #

import os
import pandas as pd

directory = '/home/lightning/py3/protons/protons-GOES'
files = os.listdir(directory) 
os.chdir(directory)
filename = 'GOESdatabefore1997.csv'

#-----------------------------------------------------------------------------------------------------------#
GOESdata = {}
key = 0

for name in files:

    fread = open(name)                      # зачитать каждый файл, содрать с него шапку и подклеить к единому
    lines = {}               
    flag = '0'
    i = 0
    for line in fread:
        if (flag=='0' and line!='time_tag,e2_flux_ic,p1_flux,p2_flux,p3_flux,p4_flux,p5_flux,p6_flux,p7_flux,a1_flux,a2_flux,a3_flux,a4_flux,a5_flux,a6_flux,p1_flux_c,p2_flux_c,p3_flux_c,p4_flux_c,p5_flux_c,p6_flux_c,p7_flux_c,p1_flux_ic,p2_flux_ic,p3_flux_ic,p4_flux_ic,p5_flux_ic,p6_flux_ic,p7_flux_ic\n'):
            pass                            # убрала шапку
        else:
            flag = '1'
            lines[i] = line
            i += 1

    if 0 in lines: del lines[0]
    array = []; timedate = []; time = []; date = []; newlines = {}

    for line in lines:
        newarray = []
        array = lines.get(line).split(',')
        timedate = array[0].split(' ')
        date = timedate[0].split('-')
        time = timedate[1].split(':')
        if '\n' in array[28]:
            s = array[28]; s = s[:-1]; array[28] = s  
        #newarray.append(array[4]+','+array[5]+','+array[6]+','+array[7]+','+array[24]+','+array[25]+','+array[26]+','+array[28]) # диф + инт
        newarray.append(array[24]+','+array[25]+','+array[26]+','+array[28])                                                      # инт
        newarray = date + time + newarray
        newlines[key] = newarray
        key+=1

    GOESdata.update(newlines)
    fread.close()
        
GOESdataframe = pd.DataFrame.from_dict(GOESdata, orient='index', dtype=float)
pd.DataFrame.to_csv(GOESdataframe, filename, index=False, index_label=False, decimal=',')



# --- ФОРМИРОВАНИЕ ВЫБОРКИ ДАННЫХ ПО ПОТОКУ ПРОТОНОВ ИЗ ДАННЫХ В ФОРМАТЕ GOES --- #
# --- ФОРМАТ ПОСЛЕ 2011г --- #

import os
import pandas as pd

directory = '/home/lightning/py3/protons/protons-GOES'
files = os.listdir(directory) 
os.chdir(directory)
filename = 'GOESdataafter2011.csv'

#-----------------------------------------------------------------------------------------------------------#
GOESdata = {}
key = 0

for name in files:

    fread = open(name)                      # зачитать каждый файл, содрать с него шапку и подклеить к единому
    lines = {}               
    flag = '0'
    i = 0
    for line in fread:
        if (flag=='0' and line!='time_tag,ZPGT1E_QUAL_FLAG,ZPGT1E,ZPGT5E_QUAL_FLAG,ZPGT5E,ZPGT10E_QUAL_FLAG,ZPGT10E,ZPGT30E_QUAL_FLAG,ZPGT30E,ZPGT50E_QUAL_FLAG,ZPGT50E,ZPGT60E_QUAL_FLAG,ZPGT60E,ZPGT100E_QUAL_FLAG,ZPGT100E,ZPGT1W_QUAL_FLAG,ZPGT1W,ZPGT5W_QUAL_FLAG,ZPGT5W,ZPGT10W_QUAL_FLAG,ZPGT10W,ZPGT30W_QUAL_FLAG,ZPGT30W,ZPGT50W_QUAL_FLAG,ZPGT50W,ZPGT60W_QUAL_FLAG,ZPGT60W,ZPGT100W_QUAL_FLAG,ZPGT100W,ZPEQ5E_QUAL_FLAG,ZPEQ5E,ZPEQ15E_QUAL_FLAG,ZPEQ15E,ZPEQ30E_QUAL_FLAG,ZPEQ30E,ZPEQ50E_QUAL_FLAG,ZPEQ50E,ZPEQ60E_QUAL_FLAG,ZPEQ60E,ZPEQ100E_QUAL_FLAG,ZPEQ100E,ZPEQ5W_QUAL_FLAG,ZPEQ5W,ZPEQ15W_QUAL_FLAG,ZPEQ15W,ZPEQ30W_QUAL_FLAG,ZPEQ30W,ZPEQ50W_QUAL_FLAG,ZPEQ50W,ZPEQ60W_QUAL_FLAG,ZPEQ60W,ZPEQ100W_QUAL_FLAG,ZPEQ100W\n'):
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
        if '\n' in array[52]:
            s = array[52]; s = s[:-1]; array[52] = s     
        newarray.append(array[6]+','+array[8]+','+array[10]+','+array[14]+','+array[20]+','+array[22]+','+array[24]+','+array[28]) # инт с двух детекторов
        newarray = date + time + newarray
        newlines[key] = newarray
        key+=1

    GOESdata.update(newlines)
    fread.close()
        
GOESdataframe = pd.DataFrame.from_dict(GOESdata, orient='index', dtype=float)
pd.DataFrame.to_csv(GOESdataframe, filename, index=False, index_label=False, decimal=',')


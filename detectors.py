
# --- ПОДСЧЁТ СРЕДНЕГО МЕЖДУ 2 ДЕТЕКТОРАМИ (ДАННЫЕ ПОСЛЕ 2011 ГОДА) --- #

import pandas as pd
import os

initfile = '../GOESdataafter2011.csv'
finfile = '../GOESdataafter2011_mid.csv'

#-----------------------------------------------------------------------------------------------------------#

lines = {}
i = 0
fopen = open(initfile)                                                 # файл без названий в первой строке, сразу данные
for line in fopen:
    lines[i] = line.split(',')
    i += 1
fopen.close()

x1 = '-99999.0'; x2 = '-99999.0\n'
key = 0
newlines={}

for key in range (0, len(lines)):

    row = lines[key]
    newrow = []
    newrow[0:5]=row[0:5]
    i = 0

    for i in range (0, 4):
        if ((row[i+5]!=x1) and (row[i+5]!=x2)) and ((row[i+9]!=x1) and (row[i+9]!=x2)):
            newrow.append(round(((float(row[i+5]) + float(row[i+9]))/2),4))
        if ((row[i+5]==x1) or (row[i+5]==x2)) and ((row[i+9]!=x1) and (row[i+9]!=x2)):
            row[i+5] = 0
            newrow.append(round(((float(row[i+5]) + float(row[i+9]))/2),4))
        if ((row[i+5]!=x1) and (row[i+5]!=x2)) and ((row[i+9]==x1) or (row[i+9]==x2)):
            row[i+9] = 0
            newrow.append(round(((float(row[i+5]) + float(row[i+9]))/2),4))
        if ((row[i+5]==x1) or (row[i+5]==x2)) and ((row[i+9]==x1) or (row[i+9]==x2)):
            newrow.append('-99999.0')

    newlines[key] = newrow[0:9]


GOESdatahours = pd.DataFrame.from_dict(newlines, orient='index', dtype=float)
pd.DataFrame.to_csv(GOESdatahours, finfile, index=False, index_label=False)

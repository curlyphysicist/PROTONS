
# --- ПЕРЕСЧЁТ ПЯТИМИНУТНЫХ ЗНАЧЕНИЙ В СРЕДНЕ-15-МИНУТНЫЕ --- #

import pandas as pd
from collections import defaultdict

filename = '../protons-GOES/filin.csv'
filepath = '../protons-GOES/filin15.csv'
#----------------------------------------------------------------------------------------------#
lines = {}
i = 0
fopen = open(filename)                                # файл без названий в первой строке, сразу данные. Уже склеенные в единый файл протоны GOES.
for line in fopen:
    lines[i] = line.split(',')
    i += 1
fopen.close()
#-------------------------------------------------------------------------#

x1 = '-99999.0'; x2 = '-99999.0\n'
col = 0; i = 0; cnt = 0
keynow = 0; keynext = 1
nowrow = lines[keynow]
nextrow = lines[keynext]
newlines = {}
newdata = {}
count = 0
#-------------------------------------------------------------------------#

for keynow in range (0, len(lines)-1, 3):                                    
    nowrow = lines[keynow]                                                            
    col = 0  
    if (nowrow[4]=='0' or nowrow[4]=='0.0'):
        newdata[count] = nowrow[0:4]
        count += 1
    for col in range (0, 4):
        #print('new column', col)
        i = 0
        if (nowrow[col+5] != x1) and (nowrow[col+5]!=x2):
            newlines[cnt] = nowrow[0:4] 
            n = 0
            for i in range (0, 2):                                           
                nextrow = lines[keynext+i]   
                if ((nowrow[0]==nextrow[0]) and (nowrow[1]==nextrow[1]) and (nowrow[2]==nextrow[2]) and (nowrow[3]==nextrow[3])):
                    if (nextrow[col+5]==x1) or (nextrow[col+5]==x2):
                        n += 1
                    else:
                        nowrow[col+5] = float(nowrow[col+5]) + float(nextrow[col+5])
                    #print('I added', nextrow[0:5])
                else:
                    print("what's wrong with your data?")

            nowrow[col+5] = str(round((float(nowrow[col+5])/(3-n)),4))         

        else:
            newlines[cnt] = nowrow[0:4]
            n = 0
            for i in range (0, 2):                                             
                nextrow = lines[keynext+i]   
                if ((nowrow[0]==nextrow[0]) and (nowrow[1]==nextrow[1]) and (nowrow[2]==nextrow[2]) and (nowrow[3]==nextrow[3])):
                    if (nextrow[col+5]==x1) or (nextrow[col+5]==x2):
                        n += 1
                    else:
                        if (nowrow[col+5]==x1) or (nowrow[col+5]==x2):                                   
                            nowrow[col+5] = float(nextrow[col+5])
                        else:
                            nowrow[col+5] = float(nowrow[col+5]) + float(nextrow[col+5])
                else:
                    print("what's wrong with your data? А, удали первую строчку, возможно :)")
            if (nowrow[col+5]!=x1) and (nowrow[col+5]!=x2): 
                nowrow[col+5] = str(round((float(nowrow[col+5])/(3-n)),4))     
            else:
                nowrow[col+5] = '-99999.0'
    nowrow[4] = str(int(float(nowrow[4]) + 15))
    newlines[cnt] = newlines[cnt] + nowrow[4:9]
    #print(newlines[cnt])
    keynext += 3; cnt += 1  

try:
    m = 0; w = 0
    for count in range (0, int(len(newlines)), 1):
        for m in range (0, 4):
            newdata[count] = newdata[count] + newlines[m+w][5:9]
        count += 1; w += 4
except:          
    pass

GOESdatahours = pd.DataFrame.from_dict(newdata, orient='index', dtype=float)
pd.DataFrame.to_csv(GOESdatahours, filepath, index=False, index_label=False)        

#----------------------------------------------------------------------------------------------#

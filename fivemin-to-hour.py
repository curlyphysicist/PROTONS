
# --- ПРЕОБРАЗОВАНИЕ ПЯТИМИНУТНЫХ ДАННЫХ ПО ПРОТОНАМ GOES В СРЕДНЕЧАСОВЫЕ --- #

import pandas as pd

initfile = '../GOESdata1997to2011part2.csv'
finfile = '../GOESdata1997to2011part2-hours.csv'

#-----------------------------------------------------------------------------------------------------------#

lines = {}
i = 0
fopen = open(initfile)                                              # файл без названий в первой строке, сразу данные
for line in fopen:
    lines[i] = line.split(',')
    i += 1
fopen.close()


x1 = '-99999.0'; x2 = '-99999.0\n'
col = 0; i = 0; cnt = 0
keynow = 0; keynext = 1
nowrow = lines[keynow]
nextrow = lines[keynext]
newlines = {}

for keynow in range (0, len(lines)-1, 12):
    nowrow = lines[keynow]                                                              
    col = 0
    for col in range (0, 4):
        i = 0
        if (nowrow[col+5] != x1) and (nowrow[col+5]!=x2):
            newlines[cnt] = nowrow[0:4]
            n = 0
            for i in range (0, 11):
                nextrow = lines[keynext+i]   
                if ((nowrow[0]==nextrow[0]) and (nowrow[1]==nextrow[1]) and (nowrow[2]==nextrow[2]) and (nowrow[3]==nextrow[3])):
                    if (nextrow[col+5]==x1) or (nextrow[col+5]==x2):
                        n += 1
                    else:
                        nowrow[col+5] = float(nowrow[col+5]) + float(nextrow[col+5])
                else:
                    print("what's wrong with your data?")
            nowrow[col+5] = str(round((float(nowrow[col+5])/(12-n)),4))
        else:
            newlines[cnt] = nowrow[0:4]
            n = 0
            for i in range (0, 11):
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
                    print("what's wrong with your data? Возможно, нужно удалить первую строку файла")
            if (nowrow[col+5]!=x1) and (nowrow[col+5]!=x2): 
                nowrow[col+5] = str(round((float(nowrow[col+5])/(12-n)),4))
            else:
                nowrow[col+5] = '-99999.0'
    newlines[cnt] = newlines[cnt] + nowrow[5:9]  
    print(newlines[cnt])
    keynext += 12; cnt += 1

GOESdatahours = pd.DataFrame.from_dict(newlines, orient='index', dtype=float)
pd.DataFrame.to_csv(GOESdatahours, finfile, index=False, index_label=False)        


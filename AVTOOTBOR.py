
# --- АВТОМАТИЧЕСКИЙ ОТБОР СПС ПО ДАННЫМ ПРОТОНОВ GOES --- #

import pandas as pd 

reserve = 10                # Захват плюс-минус с обоих сторон от СПС
t0 = 3                      # Минимальная длительность события
t1 = 3                      # Время отсутствия, после которого СПС считается законченным

# ------------------------------------------------------------- #

print('Введите каналы (10, 30, 50, 100) через пробел')
ch = input()
channels = ch.split(' ')
channels = [int(c) for c in channels]

datafile = "PROTONS_FINAL_DEEP6.csv"
file = ("EVENTS_FINAL_%sMEV.csv") % ch

# ------------------------------------------------------------- #
fopen = pd.read_csv(datafile)
year = fopen[[0]]; month = fopen[[1]]; day = fopen[[2]]; time = fopen[[3]]
if 10 in channels:
    data = fopen[[8]]
if 30 in channels:
    data = fopen[[13]]
if 50 in channels:
    data = fopen[[18]]
if 100 in channels:
    data = fopen[[23]]

i = 0; flag = 0; boundary = 0; s = 0
start = 0; fin = 0; lastfin = 0
array = []
k = 50                       # минимальное кол-во часов, за которые считаем фон
cnt = 0
ar = pd.DataFrame()

while (i < len(data)):

    if ((data.iloc[i,0]-boundary) > (3*s)):                                  
        if (flag==1):
            pass
        else:
            start = i
            flag = 1
        f = i
    else:
        if (flag==1):
            if ((i-f) <= t1):
                pass
            else:
                if ((f-start) > t0):
                    fin = f
                    lastfin = f
                    cnt+=1
                    info = fopen.iloc[(start-reserve):(fin+reserve),:]
                    ar = pd.concat([ar,info])
                    i = f+reserve-1
                    print(cnt)                                                                                                          
                    print('start ', year.iloc[start,0], ' ', month.iloc[start,0], ' ', day.iloc[start,0], ' ', time.iloc[start,0])       
                    print('fin ', year.iloc[fin,0], ' ', month.iloc[fin,0], ' ', day.iloc[fin,0], ' ', time.iloc[fin,0])                
                else:
                    pass
                flag = 0; start = 0; fin = 0

        else:
            if ((i-k) <= (i-lastfin)):                        # проверка, что от конца последнего события прошло не менее k часов
                boundary = data.iloc[(i-k):i,0].mean()        # для подсчёта среднего
                s = data.iloc[(i-k):i,0].std()
            else:
                pass
    i+=1

    #print(boundary)                               
    #print('cnt=',cnt)                             

print('FINAL cnt=', cnt)
print('cnt=', cnt)

print('before drop_duplicates ', len(ar))
ar.drop_duplicates(inplace=True)
print('after drop_duplicates ', len(ar))

ar = ar.reset_index(drop=True)

pd.DataFrame.to_csv(ar, file, index=False)

import pandas as pd
import datetime as dt
import numpy as np
df = pd.read_csv('fabforno_live.csv')
df.rename({'Minu':'Minute'}, axis = 'columns', inplace=True)
df['datetime'] = pd.to_datetime(df.iloc[:,[0,1,2,3,4]])


# dia en que el pluviometro fue destapado
df = df[df.datetime >= dt.datetime(2024,12,10)]

# obteniendo acumulado diario
dats = []; rains = []
for day in df.datetime.dt.date.unique():
    df_ = df[df.datetime.dt.date == day]
    dat = day + dt.timedelta(days=-366)
    acum_day = df_.rain.to_list()[-1]
    last_data = df_.datetime.to_list()[-1]
    dats.append(dat)
    rains.append(round(acum_day,1))
    
rains[0] = rains[0]+170.1
rains = np.cumsum(rains)
df_exp = pd.DataFrame(list(zip(dats, rains)), columns = ['date','rainacum'])
df_exp['last_point'] = last_data
print('Último dato',last_data)
df_exp.to_csv('rain2024_live.csv', index = False)

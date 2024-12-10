import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime as dt

# reading files
#data live (15min)
dav2 = pd.read_csv('cota_cota_live.csv')
dav2.rename({'Minu':'Minute'}, axis = 'columns', inplace=True)
dav2['datetime'] = pd.to_datetime(dav2.iloc[:,[0,1,2,3,4]])

# dia en que el pluviometro fue destapado
lim = dt.datetime.now() + dt.timedelta(days = -1)
lim = lim.replace(hour = 0, minute= 0, second=0)
df = dav2[dav2.datetime >= lim]
df = df[['datetime','rain']]

df2 = df.set_index('datetime').resample('1h').min().reset_index()#.drop('datetime', axis = 'columns').reset_index()
hrly = [0]
rain = df2.rain.to_list()
for i in range(len(rain)-1):
    c = rain[i+1] - rain[i]
    if c < 0:
        hrly.append(0)
    else:
        hrly.append(c)

df2['hrly'] = hrly
fig, ax = plt.subplots(figsize = (10,6))
ax.bar(df2.datetime, df2.hrly, width=pd.Timedelta(hours=1), align='edge')
ax.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d%b'))
ax.xaxis.set_major_locator(mdates.HourLocator(np.arange(2,24,2)))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax.tick_params(axis='x', which='minor', pad=18)
ax.set_xlim(lim + dt.timedelta(hours=-1), lim+dt.timedelta(hours = 47, minutes = 30))
ax.grid(which='both', lw = 0.2, alpha = .5)
ax.set_title('Precipitación últimos dos días Cota Cota', fontsize = 18)
ax.set_xlabel('Hora Local', fontsize = 14)
ax.set_ylabel('Precipitación [mm/hora]', fontsize = 14)

fig.savefig('../figs/hourly_plotCC.png', dpi = 300)

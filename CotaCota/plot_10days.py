import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime as dt

# reading files
#ambient weather til nov25
aw = pd.read_csv('cotacota_2024.csv', parse_dates = ['date'])
#davis from nov26
dav = pd.read_csv('rain2024_live.csv', parse_dates = ['date'])

dav.rename({'rainacum':'daily_rain'}, axis = 'columns', inplace=True)
lst_dat = dav.last_point.to_list()[0]
dav = dav[['date', 'daily_rain']]
dav['date'] = dav.date + dt.timedelta(days = 366)
rn = [0]
rns = dav.daily_rain.to_list()
for i in range(len(dav.daily_rain)-1):
    rn.append(round(rns[i+1] - rns[i],1))
dav['daily_rain'] = rn

df = pd.concat([aw, dav], axis = 'rows')
df = df.sort_values('date').reset_index().drop('index', axis = 'columns')
df = df[df.date > (dt.datetime.now() + dt.timedelta(days = -10))]

fig, ax = plt.subplots(figsize = (10,6))
ax.bar(df.date, df.daily_rain, width = pd.Timedelta(days = 1), align = 'edge')
ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))
ax.grid(which='both', lw = 0.2, alpha = .7)
ax.set_title('Precipitación últimos 10 días Cota Cota', fontsize = 18)
ax.set_xlabel('Hora Local', fontsize = 14)
ax.set_ylabel('Precipitación acumulada diaria [mm]', fontsize = 14)
fig.savefig('../figs/10days_plotCC.png')
#plt.show()

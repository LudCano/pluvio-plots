import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime as dt
import os

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

df2 = df.resample('1h',on='datetime').min().reset_index()#.drop('datetime', axis = 'columns').reset_index()
hrly = [0]
rain = df2.rain.to_list()
for i in range(len(rain)-1):
    c = rain[i+1] - rain[i]
    if c < 0:
        hrly.append(0)
    else:
        hrly.append(c)

df2['hrly'] = hrly

if os.path.exists('plot_all_cotacota.png'):
    os.remove('plot_all_cotacota.png')


#########################################
##### figura
#########################################
fig, axs = plt.subplots(3,1,figsize = (8,12))
fig.subplots_adjust(hspace = 0.2, top = 0.98, bottom = 0.05)

#########################################
##### horario
#########################################

ax1 = axs[0]
ax1.bar(df2.datetime, df2.hrly, width=pd.Timedelta(hours=1), align='edge', edgecolor = 'black')
ax1.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d%b'))
ax1.xaxis.set_major_locator(mdates.HourLocator(np.arange(2,24,2)))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax1.tick_params(axis='x', which='minor', pad=18)
ax1.set_xlim(lim + dt.timedelta(hours=-1), lim+dt.timedelta(hours = 47, minutes = 30))
ax1.grid(which='both', lw = 0.2, alpha = .5)
#ax1.set_title('Precipitación últimos dos días Cota Cota', fontsize = 18)
#ax1.set_xlabel('Hora Local', fontsize = 10)
ax1.set_ylabel('Precipitación [mm/hora]', fontsize = 10)


#########################################
##### 10 dias
#########################################
#fig.savefig('hourly_plot.png', dpi = 300)
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

ax2 = axs[1]
ax2.bar(df.date, df.daily_rain, width = pd.Timedelta(days = 1), align = 'edge', edgecolor = 'black')
ax2.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))
ax2.grid(which='both', lw = 0.2, alpha = .7)
#ax2.set_title('Precipitación últimos 10 días Cota Cota', fontsize = 18)
#ax2.set_xlabel('Fecha', fontsize = 10)
ax2.set_ylabel('Precipitación acumulada diaria [mm]', fontsize = 10)


#########################################
##### acumulado
#########################################
hist = pd.read_csv('cotacota_historial.csv', parse_dates = ['dtt'])
aw = pd.read_csv('cotacota_2024.csv', parse_dates = ['date'])
now = pd.read_csv('rain2024_live.csv', parse_dates=['date'])
aw['date'] = aw.date + dt.timedelta(days = -366)
aw['cumrain'] = aw.daily_rain.cumsum()

anhos = hist.hidroyear.unique()
dfss = []


ax3 = axs[2]

for year in anhos:
    df_ = hist[hist.hidroyear == year]
    lin, = ax3.plot(df_.dtt, df_.rainsum, label = f'{min(anhos)}-2023', c = 'k', alpha = .3, lw = .7)
    dfss.append(df_.rainsum.to_list())

rains = np.array(dfss)
rain_cummean = np.mean(rains, axis = 0)


lin2, = ax3.plot(df_.dtt, rain_cummean, label = 'Promedio', c = 'k', lw = 1.5, ls = '--')
lin3, = ax3.plot(aw.date, aw.cumrain, label = '2024', c = 'r', lw = 1.5)
lin3, = ax3.plot(now.date, now.rainacum, label = '2024', c = 'r', lw = 1.5)
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax3.set_xlabel('Año Hidrológico', fontsize = 10)
ax3.set_ylabel('Precipitación acumulada [mm]', fontsize = 10)
#ax3.set_title('Precipitación acumulada Cota Cota', fontsize = 15)
ax3.legend(handles = [lin, lin2, lin3])
last_date = pd.to_datetime(now.last_point).to_list()[-1]
last_date = 'Última actualización ' + dt.datetime.strftime(last_date, '%d%b %H:%M')
last_rain = now.rainacum.to_list()[-1]
txt = f'Precipitación acumulada\n {round(last_rain,1)}mm'
ax3.annotate(txt, (0.96,0.01), xycoords='axes fraction', ha = 'right', fontsize = 12)
ax3.annotate(last_date, (0.96,0.01), xycoords='figure fraction', ha = 'right', fontsize = 6)


fig.savefig('plot_all_cotacota.png', dpi = 400)
#plt.show()
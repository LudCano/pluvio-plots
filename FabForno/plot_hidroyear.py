import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import os


#os.remove('pluvio.png')

hist = pd.read_csv('fabforno_historial.csv', parse_dates = ['dtt'])
aw = pd.read_csv('fabforno_2024.csv', parse_dates = ['date'])
now = pd.read_csv('rain2024_live.csv', parse_dates=['date'])
aw['date'] = aw.date + dt.timedelta(days = -366)
aw['cumrain'] = aw.daily_rain.cumsum()

fig, ax = plt.subplots()
anhos = hist.hidroyear.unique()
dfss = []
for year in anhos:
    df_ = hist[hist.hidroyear == year]
    lin, = ax.plot(df_.dtt, df_.rainsum, label = f'{min(anhos)}-2023', c = 'k', alpha = .3, lw = .7)
    dfss.append(df_.rainsum.to_list())

rains = np.array(dfss)
rain_cummean = np.mean(rains, axis = 0)
lin2, = ax.plot(df_.dtt, rain_cummean, label = 'Promedio', c = 'k', lw = 1.5, ls = '--')
lin3, = ax.plot(aw.date, aw.cumrain, label = '2024', c = 'r', lw = 1.5)
lin3, = ax.plot(now.date, now.rainacum, label = '2024', c = 'r', lw = 1.5)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xlabel('Año Hidrológico', fontsize = 12)
ax.set_ylabel('Precipitación acumulada [mm]', fontsize = 12)
ax.set_title('Precipitación acumulada Cota Cota', fontsize = 15)
ax.legend(handles = [lin, lin2, lin3])
last_date = pd.to_datetime(now.last_point).to_list()[-1]
last_date = 'Última actualización ' + dt.datetime.strftime(last_date, '%d%b %H:%M')
last_rain = now.rainacum.to_list()[-1]
txt = f'Precipitación acumulada\n {round(last_rain,1)}mm'
ax.annotate(txt, (0.96,0.01), xycoords='axes fraction', ha = 'right', fontsize = 12)
ax.annotate(last_date, (0.96,0.01), xycoords='figure fraction', ha = 'right', fontsize = 6)
#plt.show()

fig.savefig('../figs/pluvioFF.png', dpi = 300)

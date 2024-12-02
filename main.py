import os
print('Downloading data...')
with open('download_data.py') as file:
    exec(file.read())

print('Processing...')
with open('proc_live_data.py') as file:
    exec(file.read())

os.remove('hourly_plot.png')
os.remove('10days_plot.png')

print('Plotting hidroyear...')
with open('plot_hidroyear.py') as file:
    exec(file.read())
print('Plot generated!')

print('Plotting hourly...')
with open('plot_hourly.py') as file:
    exec(file.read())
print('Plot generated!')


print('Plotting 10 days acum...')
with open('plot_10days.py') as file:
    exec(file.read())
print('Plot generated!')


print('Plotting everything...')
with open('plot_cotacota.py') as file:
    exec(file.read())
print('Plot generated!')

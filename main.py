import os

# Cleaning figures
for f in os.listdir('figs'):
    os.remove(os.path.join('figs',f))
    print('removed',f)



print('------------------')
print('WORKING COTA COTA')
print('------------------')

os.chdir('CotaCota')

with open('download_data.py') as file:
    exec(file.read())

print('Processing...')
with open('proc_live_data.py') as file:
    exec(file.read())


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


print('------------------')
print('WORKING FABRICA FORNO')
print('------------------')

os.chdir('../FabForno')

with open('download_data.py') as file:
    exec(file.read())

print('Processing...')
with open('proc_live_data.py') as file:
    exec(file.read())


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
with open('plot_fabforno.py') as file:
    exec(file.read())
print('Plot generated!')

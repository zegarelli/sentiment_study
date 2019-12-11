import read_data
import matplotlib.pyplot as plt

data_set = read_data.main('CPC')

date = []
spx = []
cpc = []
spread = []

for day in data_set['days']:
    date.append(day.date)
    spx.append(day.spx)
    cpc.append(day.cpc)
    spread.append(day.prior_week_spread)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)


plt.show()

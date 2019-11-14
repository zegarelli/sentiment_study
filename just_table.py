import read_data
import os

"""
Setup output file
"""
log_file = 'full_data.csv'

try:
    os.remove(log_file)
except FileNotFoundError:
    pass

"""
Read data from csv's
"""
data_set = read_data.main()

days = data_set['days']

with open(log_file, "a") as f:
    f.write('Date,CPC,Bulls,Bears,SPX91,SPX182,SPX365')
    for day in days:
        f.write('\n{},{},{},{},{},{},{}'.format(day.date, day.cpc, day.prior_week_bulls['close'],
                                                day.prior_week_bears['close'], day.spx91_return,
                                                day.spx182_return, day.spx365_return))

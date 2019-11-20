import read_data
import stats
import os

log_file = 'output.txt'

try:
    os.remove(log_file)
except FileNotFoundError:
    pass

data_set = read_data.main()

days = data_set['days']
cpc_stats = data_set['cpc_stats']
bulls_stats = data_set['bulls_stats']
bears_stats = data_set['bears_stats']


def mprint(text):
    with open(log_file, "a") as f:
        f.write('\n{}'.format(text))
        print(text)

mprint('DATA STATS')
mprint('cpc_stats')
mprint(cpc_stats)
mprint('\nbulls_stats')
mprint(bulls_stats)
mprint('\nbears_stats')
mprint(bears_stats)
mprint('\n--------------------------------Begin Analysis-----------------------------------\n')


def test_cpc(day, threshold, cpc_gt):
    if not cpc_gt:
        if day.cpc < cpc_stats['mean'] - threshold * cpc_stats['std']:
            return True
    else:
        if day.cpc > cpc_stats['mean'] + threshold * cpc_stats['std']:
            return True


def test_condition(day, threshold, condition_gt, bears):
    if not bears:
        if not condition_gt:
            if day.prior_week_bulls['close'] < bulls_stats['mean'] - threshold * bulls_stats['std']:
                return True
        else:
            if day.prior_week_bulls['close'] > bulls_stats['mean'] + threshold * bulls_stats['std']:
                return True
    else:
        if not condition_gt:
            if day.prior_week_bears['close'] < bears_stats['mean'] - threshold * bears_stats['std']:
                return True
        else:
            if day.prior_week_bears['close'] > bears_stats['mean'] + threshold * bears_stats['std']:
                return True


def analyze(cpc_treshold, condition_treshold=None, cpc_gt=None, condition_gt=None, bears=None):
    output = []
    for day in days:
        if test_cpc(day, cpc_treshold, cpc_gt):
            if condition_treshold:
                if test_condition(day, condition_treshold, condition_gt, bears):
                    output.append(day)
            else:
                output.append(day)
    cpc_operator = '< Mean-'
    if cpc_gt:
        cpc_operator = '> Mean+'
    condition_operator = '< Mean-'
    if condition_gt:
        condition_operator = '> Mean+'
    condition_name = 'Bulls'
    if bears:
        condition_name = 'Bears'
    test_name = 'CPC {}{}xSTD'.format(cpc_operator, cpc_treshold)
    if condition_treshold:
        test_name += ' & {} {}{}xSTD'.format(condition_name, condition_operator, condition_treshold)
    stat = stats.calculate(output)
    mprint('\n{},{},{},{},{},{},{},{}'.format(test_name, len(output), stat['spx91_mean'], stat['spx91_std'],
                                            stat['spx182_mean'], stat['spx182_std'],
                                            stat['spx365_mean'], stat['spx365_std']))
    with open(test_name + '.csv', "a") as f:
        f.write('Date,CPC,Bulls,Bears,SPX91,SPX182,SPX365')
        for outday in output:
            f.write('\n{},{},{},{},{},{},{}'.format(outday.date, outday.cpc, outday.prior_week_bulls['close'],
                                                    outday.prior_week_bears['close'], outday.spx91_return,
                                                    outday.spx182_return, outday.spx365_return))


analyze(cpc_treshold=2)
analyze(cpc_treshold=1.5)
analyze(cpc_treshold=2, cpc_gt=True)
analyze(cpc_treshold=1.5, cpc_gt=True)

analyze(cpc_treshold=2, condition_treshold=2, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1.75, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1.5, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1.25, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1, condition_gt=True)
analyze(cpc_treshold=1.5, condition_treshold=2, condition_gt=True)
analyze(cpc_treshold=1.5, condition_treshold=1.5, condition_gt=True)
analyze(cpc_treshold=1.5, condition_treshold=1, condition_gt=True)
analyze(cpc_treshold=1, condition_treshold=2, condition_gt=True)
analyze(cpc_treshold=1, condition_treshold=1.5, condition_gt=True)
analyze(cpc_treshold=1, condition_treshold=1, condition_gt=True)

analyze(cpc_treshold=2, cpc_gt=True, condition_treshold=2, condition_gt=True, bears=True)
analyze(cpc_treshold=2, cpc_gt=True, condition_treshold=1.5, condition_gt=True, bears=True)
analyze(cpc_treshold=2, cpc_gt=True, condition_treshold=1, condition_gt=True, bears=True)
analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=2, condition_gt=True, bears=True)
analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1.5, condition_gt=True, bears=True)
analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1, condition_gt=True, bears=True)
analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=2, condition_gt=True, bears=True)
analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1.5, condition_gt=True, bears=True)
analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1, condition_gt=True, bears=True)

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
    with open("output.txt", "a") as f:
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


def test_condition(day, threshold, condition_gt):
    if not condition_gt:
        if day.prior_week_bulls['close'] < bulls_stats['mean'] - threshold * bulls_stats['std']:
            return True
    else:
        if day.prior_week_bulls['close'] > bulls_stats['mean'] + threshold * bulls_stats['std']:
            return True


def analyze(cpc_treshold, condition_treshold=None, cpc_gt=None, condition_gt=None):
    just_cpc = []
    cpc_and_bulls = []
    for day in days:
        if not cpc_gt:
            if test_cpc(day, cpc_treshold, cpc_gt):
                just_cpc.append(day)

                if condition_treshold and test_condition(day, condition_treshold, condition_gt):
                    cpc_and_bulls.append(day)

    if not condition_treshold:
        mprint('\n-----------  CPC Treshold = mean - {}*stdev  -----------'.format(cpc_treshold))
        mprint('Count: {}'.format(len(just_cpc)))
        for key, value in stats.calculate(just_cpc).items():
            mprint('{}: {}'.format(key, value))
        for cpc in just_cpc:
            mprint(cpc)
    else:
        mprint('\n-----------  CPC Treshold = mean - {}*stdev & Bulls Treshold = mean + {}*stdev  -----------'.format(cpc_treshold, condition_treshold))
        mprint('Count: {}'.format(len(cpc_and_bulls)))
        for key, value in stats.calculate(cpc_and_bulls).items():
            mprint('{}: {}'.format(key, value))
        for cpcb in cpc_and_bulls:
            mprint(cpcb)


analyze(cpc_treshold=2)
analyze(cpc_treshold=2, condition_treshold=2, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1.75, condition_gt=True)
analyze(cpc_treshold=2, condition_treshold=1.5, condition_gt=True)
analyze(cpc_treshold=1.75)
analyze(cpc_treshold=1.75, condition_treshold=2, condition_gt=True)
analyze(cpc_treshold=1.75, condition_treshold=1.75, condition_gt=True)
analyze(cpc_treshold=1.75, condition_treshold=1.5, condition_gt=True)

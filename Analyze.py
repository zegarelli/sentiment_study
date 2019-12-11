import read_data
import stats
import os
from datetime import datetime
from plotting import plot_multiple_tests_average, plot_spx_with_points, plot_equity_curve

log_file = 'output/summary.csv'
try:
    os.remove(log_file)
except FileNotFoundError:
    pass

for case in ['ICBOETPCR', 'CPC', 'CPCE']: # , 'CPCI', 'CPC2003', 'CPC', 'CPCE'

    if case != 'CPC2003':
        data_set = read_data.main(case)
    else:
        data_set = read_data.main('CPC', datetime.strptime('01/01/2003', '%m/%d/%Y').date())

    days = data_set['days']
    cpc_stats = data_set['cpc_stats']
    bulls_stats = data_set['bulls_stats']
    bears_stats = data_set['bears_stats']
    spread_stats = data_set['spread_stats']


    def mprint(text):
        with open(log_file, "a") as f:
            f.write('\n{}'.format(text))
            print(text)

    mprint('\n{} DATA STATS'.format(case))
    mprint(',MEAN,STDEV,MAX,MIN')
    mprint('{},{},{},{},{}'.format(case, cpc_stats['mean'], cpc_stats['std'], cpc_stats['max'], cpc_stats['min']))
    mprint('{},{},{},{},{}'.format('Bulls', bulls_stats['mean'], bulls_stats['std'], bulls_stats['max'], bulls_stats['min']))
    mprint('{},{},{},{},{}'.format('Bears', bears_stats['mean'], bears_stats['std'], bears_stats['max'], bears_stats['min']))
    mprint('{},{},{},{},{}'.format('Spread', spread_stats['mean'], spread_stats['std'], spread_stats['max'], spread_stats['min']))
    mprint('\nTest,Count, SPX91, SPX91SD, SPX182, SPX182SD, SPX365, SPX365SD')


    def test_cpc(day, threshold, cpc_gt):
        if not cpc_gt:
            if day.cpc < cpc_stats['mean'] - threshold * cpc_stats['std']:
                return True
        else:
            if day.cpc > cpc_stats['mean'] + threshold * cpc_stats['std']:
                return True


    def test_condition(day, threshold, condition_gt, condition):
        if condition == 'Bulls':
            if not condition_gt:
                if day.prior_week_bulls['close'] < bulls_stats['mean'] - threshold * bulls_stats['std']:
                    return True
            else:
                if day.prior_week_bulls['close'] > bulls_stats['mean'] + threshold * bulls_stats['std']:
                    return True
        elif condition == 'Bears':
            if not condition_gt:
                if day.prior_week_bears['close'] < bears_stats['mean'] - threshold * bears_stats['std']:
                    return True
            else:
                if day.prior_week_bears['close'] > bears_stats['mean'] + threshold * bears_stats['std']:
                    return True
        elif condition == 'Spread':
            if not condition_gt:
                if day.prior_week_spread['close'] < spread_stats['mean'] - threshold * spread_stats['std']:
                    return True
            else:
                if day.prior_week_spread['close'] > spread_stats['mean'] + threshold * spread_stats['std']:
                    return True
        else:
            print('CONDITION NOT RECOGNIZED')

    def analyze(cpc_treshold, condition_treshold=None, cpc_gt=None, condition_gt=None, condition_name=None):
        output = []
        plot_days = []
        plot_spx = []
        plot_points = []
        trigger_dates = []
        for n, day in enumerate(days):
            plot_days.append(day.date)
            plot_spx.append(day.spx)
            if test_cpc(day, cpc_treshold, cpc_gt):
                if condition_treshold:
                    if test_condition(day, condition_treshold, condition_gt, condition_name):
                        output.append(day)
                        plot_points.append(n)
                        trigger_dates.append(day.date)
                else:
                    output.append(day)
                    plot_points.append(n)
                    trigger_dates.append(day.date)
        cpc_operator = '-'
        if cpc_gt:
            cpc_operator = '+'
        condition_operator = '-'
        if condition_gt:
            condition_operator = '+'
        test_name = '{}{}{}'.format(case, cpc_operator, cpc_treshold)
        if condition_treshold:
            test_name += '_&_{}{}{}'.format(condition_name, condition_operator, condition_treshold)
        stat = stats.calculate(output)
        mprint('{},{},{},{},{},{},{},{}'.format(test_name, len(output), stat['spx91_mean'], stat['spx91_std'],
                                                stat['spx182_mean'], stat['spx182_std'],
                                                stat['spx365_mean'], stat['spx365_std']))
        with open('output/{}/{}.csv'.format(case, test_name), 'a') as f:
            f.write('Date,CPC,Bulls,Bears,SPX91,SPX182,SPX365')
            for outday in output:
                f.write('\n{},{},{},{},{},{},{}'.format(outday.date, outday.cpc, outday.prior_week_bulls['close'],
                                                        outday.prior_week_bears['close'], outday.spx91_return,
                                                        outday.spx182_return, outday.spx365_return))
        # plot_multiple_days_serial(output, test_name)
        # plot_multiple_days(output, test_name)
        # plot_multiple_days_average(output, test_name)
        plot_spx_with_points(plot_days, plot_spx, plot_points, 'output/figures/{}/{}'.format(case, test_name))
        plot_equity_curve(days, trigger_dates, 'output/figures/{}/Equity_{}'.format(case, test_name))
        tests.append([output, test_name])

    tests = []

    """
    Negative CPC
    """
    analyze(cpc_treshold=1.5)
    analyze(cpc_treshold=1.25)
    analyze(cpc_treshold=1)

    """
    Bulls
    """
    analyze(cpc_treshold=1.5, condition_treshold=1.5, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1.5, condition_treshold=1.25, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1.5, condition_treshold=1, condition_gt=True, condition_name='Bulls')

    analyze(cpc_treshold=1.25, condition_treshold=1.5, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1.25, condition_treshold=1.25, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1.25, condition_treshold=1, condition_gt=True, condition_name='Bulls')

    analyze(cpc_treshold=1, condition_treshold=1.5, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1, condition_treshold=1.25, condition_gt=True, condition_name='Bulls')
    analyze(cpc_treshold=1, condition_treshold=1, condition_gt=True, condition_name='Bulls')

    plot_multiple_tests_average(tests, '{}/All_{}- & Bulls'.format(case, case))

    tests = []
    """
    Positive CPC
    """
    analyze(cpc_treshold=1.5, cpc_gt=True)
    analyze(cpc_treshold=1.25, cpc_gt=True)
    analyze(cpc_treshold=1, cpc_gt=True)

    """
    Bears
    """

    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1.5, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1.25, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1, condition_gt=True, condition_name='Bears')

    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1.5, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1.25, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1, condition_gt=True, condition_name='Bears')

    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1.5, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1.25, condition_gt=True, condition_name='Bears')
    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1, condition_gt=True, condition_name='Bears')

    plot_multiple_tests_average(tests, '{}/All_{}+ & Bears'.format(case, case))

    tests = []

    """
    Negative CPC
    """
    analyze(cpc_treshold=1.5)
    analyze(cpc_treshold=1.25)
    analyze(cpc_treshold=1)

    """
    Spread
    """
    analyze(cpc_treshold=1.5, condition_treshold=1.5, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1.5, condition_treshold=1.25, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1.5, condition_treshold=1, condition_gt=True, condition_name='Spread')

    analyze(cpc_treshold=1.25, condition_treshold=1.5, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1.25, condition_treshold=1.25, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1.25, condition_treshold=1, condition_gt=True, condition_name='Spread')

    analyze(cpc_treshold=1, condition_treshold=1.5, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1, condition_treshold=1.25, condition_gt=True, condition_name='Spread')
    analyze(cpc_treshold=1, condition_treshold=1, condition_gt=True, condition_name='Spread')

    plot_multiple_tests_average(tests, '{}/All_{}+ & Spread+'.format(case, case))

    tests = []

    """
    Positive CPC
    """
    analyze(cpc_treshold=1.5, cpc_gt=True)
    analyze(cpc_treshold=1.25, cpc_gt=True)
    analyze(cpc_treshold=1, cpc_gt=True)

    """
    Spread
    """
    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1.5, condition_name='Spread')
    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1.25, condition_name='Spread')
    analyze(cpc_treshold=1.5, cpc_gt=True, condition_treshold=1, condition_name='Spread')

    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1.5, condition_name='Spread')
    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1.25, condition_name='Spread')
    analyze(cpc_treshold=1.25, cpc_gt=True, condition_treshold=1, condition_name='Spread')

    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1.5, condition_name='Spread')
    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1.25, condition_name='Spread')
    analyze(cpc_treshold=1, cpc_gt=True, condition_treshold=1, condition_name='Spread')

    plot_multiple_tests_average(tests, '{}/All_{}+ & Spread-'.format(case, case))

import read_data
import stats

data_set = read_data.main()

days = data_set['days']
cpc_stats = data_set['cpc_stats']
bulls_stats = data_set['bulls_stats']
bears_stats = data_set['bears_stats']

just_cpc = []
cpc_and_bulls = []


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
    for day in days:
        if not cpc_gt:
            if test_cpc(day, cpc_treshold, cpc_gt):
                just_cpc.append(day)

                if test_condition(day, condition_treshold, condition_gt):
                    cpc_and_bulls.append(day)

    print('\nCPC and Bulls\nCount: {}'.format(len(just_cpc)))
    for key, value in stats.calculate(cpc_and_bulls).items():
        print(key, value)
    for cpcb in cpc_and_bulls:
        print(cpcb)

    print('\nJust CPC\nCount: {}'.format(len(just_cpc)))
    for key, value in stats.calculate(just_cpc).items():
        print(key, value)
    for cpc in just_cpc:
        print(cpc)


analyze(cpc_treshold=1.5, condition_treshold=1.25)

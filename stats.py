import statistics


def calculate(dates):
    spx91 = []
    spx182 = []
    spx365 = []
    for date in dates:
        if date.spx91_return:
            spx91.append(date.spx91_return)
        if date.spx182_return:
            spx182.append(date.spx182_return)
        if date.spx365_return:
            spx365.append(date.spx365_return)

    try:
        results = {
            'spx91_std': round(statistics.stdev(spx91), 4),
            'spx91_mean': round(statistics.mean(spx91), 4),
            'spx91_median': round(statistics.median(spx91), 4),
            'spx91_min': round(min(spx91), 4),
            'spx91_max': round(max(spx91), 4),

            'spx182_std': round(statistics.stdev(spx182), 4),
            'spx182_mean': round(statistics.mean(spx182), 4),
            'spx182_median': round(statistics.median(spx182), 4),
            'spx182_min': round(min(spx182), 4),
            'spx182_max': round(max(spx182), 4),

            'spx365_std': round(statistics.stdev(spx365), 4),
            'spx365_mean': round(statistics.mean(spx365), 4),
            'spx365_median': round(statistics.median(spx365), 4),
            'spx365_min': round(min(spx365), 4),
            'spx365_max': round(max(spx365), 4)
        }
    except:
        results = {
            'spx91_std': None,
            'spx91_mean': None,
            'spx91_median': None,
            'spx91_min': None,
            'spx91_max': None,

            'spx182_std': None,
            'spx182_mean': None,
            'spx182_median': None,
            'spx182_min': None,
            'spx182_max': None,

            'spx365_std': None,
            'spx365_mean': None,
            'spx365_median': None,
            'spx365_min': None,
            'spx365_max': None
        }

    return results

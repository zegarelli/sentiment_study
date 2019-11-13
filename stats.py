import statistics

def calculate(dates):
    spx91 = []
    spx182 = []
    spx365 = []
    for date in dates:
        spx91.append(date.spx91_return)
        spx182.append(date.spx182_return)
        spx365.append(date.spx365_return)

    return {
        'spx91_std': round(statistics.stdev(spx91), 2),
        'spx91_mean': round(statistics.mean(spx91), 2),
        'spx91_median': round(statistics.median(spx91), 2),
        'spx91_min': round(min(spx91), 2),
        'spx91_max': round(max(spx91), 2),

        'spx182_std': round(statistics.stdev(spx182), 2),
        'spx182_mean': round(statistics.mean(spx182), 2),
        'spx182_median': round(statistics.median(spx182), 2),
        'spx182_min': round(min(spx182), 2),
        'spx182_max': round(max(spx182), 2),

        'spx365_std': round(statistics.stdev(spx365), 2),
        'spx365_mean': round(statistics.mean(spx365), 2),
        'spx365_median': round(statistics.median(spx365), 2),
        'spx365_min': round(min(spx365), 2),
        'spx365_max': round(max(spx365), 2)
    }

from datetime import timedelta


def get_SPX_by_date(date, SPX):
    for spx in SPX:
        if spx['date'] == date:
            return spx['close']


def get_SPX_by_date_delta(date, delta, SPX):
    search_date = date + timedelta(days=delta)
    prior_date = None
    for spx in SPX:
        if spx['date'] > search_date:
            return prior_date['close']
        prior_date = spx


def get_prior_week(date, data_set):
    prior_date = None
    for data_date in data_set['data']:
        # Subtracting two days, because the reports come out on Thursday for the prior week
        if data_date['date'] > date - timedelta(days=2):
            return prior_date
        prior_date = data_date
    return {
        'date': None,
        'close': None
    }

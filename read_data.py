from datetime import datetime
import statistics
import date_utils


class TradeDay:
    def __init__(self, cpcDay, Bulls, Bears, SPX):
        self.date = cpcDay['date']
        self.cpc = cpcDay['close']
        self.prior_week_bulls = date_utils.get_prior_week(self.date, Bulls)
        self.prior_week_bears = date_utils.get_prior_week(self.date, Bears)
        self.spx = date_utils.get_SPX_by_date(self.date, SPX)
        self.spx91 = date_utils.get_SPX_by_date_delta(self.date, 91, SPX)
        self.spx182 = None
        self.spx365 = None
        self.spx91_return = None
        self.spx182_return = None
        self.spx365_return = None
        if self.spx91:
            self.spx91_return = round((self.spx91/self.spx - 1), 4)
            self.spx182 = date_utils.get_SPX_by_date_delta(self.date, 182, SPX)
            if self.spx182:
                self.spx182_return = round((self.spx182/self.spx - 1), 4)
                self.spx365 = date_utils.get_SPX_by_date_delta(self.date, 365, SPX)
                if self.spx365:
                    self.spx365_return = round((self.spx365/self.spx - 1), 4)

    def __repr__(self):
        return '{} - CPC: {}, Bulls: {}, Bears: {}, SPX: {}, SPX91: {}%, SPX182: {}%, SPX365: {}%'.format(
            self.date, self.cpc, self.prior_week_bulls['close'], self.prior_week_bears,
            self.spx, self.spx91_return, self.spx182_return, self.spx365_return
        )


def main():
    """
    Reads and formats the raw CSV files and returns them in a single data object
    """
    data = {}

    file_path = '$SPX.csv'
    file = 'SPX'
    with open(file_path, 'r') as f:
        data[file] = []
        contents = f.readlines()
        for line in contents[2:]:
            line = line.replace(' ', '').split(',')
            date = datetime.strptime(line[0], '%m/%d/%Y').date()
            close = float(line[4])
            data[file].append({
                'date': date,
                'close': close
            })

    file_path = '$CPC.csv'
    file = 'CPC'
    with open(file_path, 'r') as f:
        data[file] = {
            'data': [],
            'raw': []
                      }
        contents = f.readlines()
        for line in contents[2:]:
            line = line.replace(' ', '').split(',')
            date = datetime.strptime(line[0], '%m/%d/%Y').date()
            close = float(line[4])
            data[file]['data'].append({
                'date': date,
                'close': close
            })
            data[file]['raw'].append(close)

    file_path = 'Total Bulls.csv'
    file = 'Bulls'
    with open(file_path, 'r') as f:
        data[file] = {
            'data': [],
            'raw': []
                      }
        contents = f.readlines()
        for line in contents[1:]:
            line = line.replace(' ', '').split(',')
            date = datetime.strptime(line[0][:10], '%Y-%m-%d').date()
            close = float(line[1])
            data[file]['data'].append({
                'date': date,
                'close': close
            })
            data[file]['raw'].append(close)

        # Reverse these two pieces to match the other data sets
        data[file]['raw'].reverse()
        data[file]['data'].reverse()

    file_path = 'Total Bears.csv'
    file = 'Bears'
    with open(file_path, 'r') as f:
        data[file] = {
            'data': [],
            'raw': []
                      }
        contents = f.readlines()
        for line in contents[1:]:
            line = line.replace(' ', '').split(',')
            date = datetime.strptime(line[0][:10], '%Y-%m-%d').date()
            close = float(line[1])
            data[file]['data'].append({
                'date': date,
                'close': close
            })
            data[file]['raw'].append(close)

        # Reverse these two pieces to match the other data sets
        data[file]['raw'].reverse()
        data[file]['data'].reverse()

    output = {
        'cpc_stats': {
            'std': statistics.stdev(data['CPC']['raw']),
            'mean': statistics.mean(data['CPC']['raw']),
            'median': statistics.median(data['CPC']['raw']),
            'max': max(data['CPC']['raw']),
            'min': min(data['CPC']['raw'])
        },
        'bulls_stats': {
            'std': statistics.stdev(data['Bulls']['raw']),
            'mean': statistics.mean(data['Bulls']['raw']),
            'median': statistics.median(data['Bulls']['raw']),
            'max': max(data['Bulls']['raw']),
            'min': min(data['Bulls']['raw'])
        },
        'bears_stats': {
            'std': statistics.stdev(data['Bears']['raw']),
            'mean': statistics.mean(data['Bears']['raw']),
            'median': statistics.median(data['Bears']['raw']),
            'max': max(data['Bears']['raw']),
            'min': min(data['Bears']['raw'])
        },
        'days': []
    }

    for cpc in data['CPC']['data']:
        output['days'].append(TradeDay(cpc, data['Bulls'], data['Bears'], data['SPX']))

    return output


if __name__ == '__main__':
    results = main()
    print('done')

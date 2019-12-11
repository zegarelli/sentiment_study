import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statistics

"""
Read data from csv's
"""
spx = []
with open('$SPX.csv', 'r') as f:
    contents = f.readlines()
    for line in contents[2:]:
        line = line.replace(' ', '').split(',')
        date = datetime.strptime(line[0], '%m/%d/%Y').date()
        close = float(line[4])
        spx.append({
            'date': date,
            'close': close
        })


def plot_day(day):
    days = []
    values = []
    for date in spx:
        if day.date <= date['date'] <= day.date + timedelta(days=365):
            delta = date['date'] - day.date
            days.append(delta.days)
            values.append(round(((date['close'] - day.spx)/day.spx)*100, 2))
    plt.plot(days, values, label='{}'.format(day.date))


def plot_multiple_days(days, title):
    for day in days:
        plot_day(day)

    plt.xlabel('Days')
    plt.ylabel('SPX Return %')
    plt.title(title)
    plt.legend()
    plt.show()


def plot_multiple_tests_average(tests, dir):
    for test in tests:
        days = test[0]
        data_set = test[1]
        years = []
        output_day_count = None
        for day in days:
            values = []
            day_count = []
            for date in spx:
                if day.date <= date['date'] <= day.date + timedelta(days=365):
                    delta = date['date'] - day.date
                    day_count.append(delta.days)
                    values.append(round(((date['close'] - day.spx) / day.spx) * 100, 2))
            years.append(values)
            if not output_day_count:
                output_day_count = day_count

        average_values = []
        for n, value_we_dont_care_about in enumerate(years[0]):
            sum = []
            for start_date in years:
                try:
                    sum.append(start_date[n])
                except Exception as e:
                    pass
            average_values.append(statistics.mean(sum))

        plt.plot(output_day_count[:240], average_values[:240], label = data_set)

    plt.xlabel('Days')
    plt.ylabel('Average SPX Return %')
    plt.title('All Tests')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('output/figures/{}.png'.format(dir), bbox_inches='tight')
    plt.close()


def plot_multiple_days_average(days, title):
    years = []
    output_day_count = None
    for day in days:
        values = []
        day_count = []
        for date in spx:
            if day.date <= date['date'] <= day.date + timedelta(days=365):
                delta = date['date'] - day.date
                day_count.append(delta.days)
                values.append(round(((date['close'] - day.spx)/day.spx)*100, 2))
        years.append(values)
        if not output_day_count:
            output_day_count = day_count

    average_values = []
    for n, value_we_dont_care_about in enumerate(years[0]):
        sum = []
        for start_date in years:
            try:
                sum.append(start_date[n])
            except Exception as e:
                pass
        average_values.append(statistics.mean(sum))

    plt.plot(output_day_count[:251], average_values[:251])

    plt.xlabel('Days')
    plt.ylabel('Average SPX Return %')
    plt.title(title)
    plt.savefig('figures/{}.png'.format(title), bbox_inches='tight')
    plt.close()


def plot_multiple_days_serial(days, title):
    prior_percent = 0
    plot_days = []
    plot_values = []
    for day in days:
        if len(plot_days) == 0 or day.date > plot_days[-1]:
            for date in spx:
                if day.date <= date['date'] <= day.date + timedelta(days=365):
                    plot_days.append(day.date)
                    plot_values.append(prior_percent + round(((date['close'] - day.spx) / day.spx) * 100, 2))
        prior_percent = plot_values[-1]

    plt.plot(plot_days[:251], plot_values[:251])
    plt.xlabel('Dates')
    plt.ylabel('SPX Return %')
    plt.title(title)
    plt.savefig('figures/{}.png'.format(title), bbox_inches='tight')
    plt.close()

def plot_spx_with_points(days, spx, points, save_location):
    plt.rcParams["figure.figsize"] = (20, 10)
    plt.plot(days, spx, color='black', markevery=points,
             marker='.', markerfacecolor='green', markeredgecolor='green', markersize=10)
    plt.ylabel('SPX Value')
    plt.title(save_location.split('/')[-1])
    plt.savefig(save_location + '.png', bbox_inches='tight')
    plt.close()


def plot_equity_curve(days, triggers, save_location):
    postitions = []
    plot_profit = []
    plot_days = []
    for day in days:
        plot_days.append(day.date)
        if day.date in triggers and (len(postitions) == 0 or not postitions[-1]['working']):
            postitions.append({'open_date': day.date, 'open_value': day.spx, 'ROI': 0, 'working': True, 'profit': 0})
        profit = 0
        for position in postitions:
            if position['open_date'] <= day.date <= position['open_date'] + timedelta(days=365):
                if position['working']:
                    position['ROI'] = (position['open_value'] - day.spx) / position['open_value']
                    position['profit'] = (position['open_value'] - day.spx) / position['open_value'] * 100000
                    if position['ROI'] <= -0.05 or day.date >= position['open_date'] + timedelta(days=365):
                        position['working'] = False
                        position['close_date'] = day.date
                        position['close_value'] = day.spx
            elif position['working']:
                position['working'] = False
                position['close_date'] = day.date
                position['close_value'] = day.spx
            profit += position['profit']
        plot_profit.append(profit)
    with open(save_location + '.txt', 'w') as f:
        f.write('OpenDate,OpenValue,CloseDate,CloseValue,ROI,Profit')
        for position in postitions:
            if not position['working']:
                f.write('\n{},{},{},{},{},{}'.format(position['open_date'], position['open_value'], position['close_date'], position['close_value'], position['ROI'], position['profit']))
            else:
                f.write('\n{},{},{},{},{},{}'.format(position['open_date'], position['open_value'], '', '', position['ROI'], position['profit']))

    plt.rcParams["figure.figsize"] = (20, 10)
    plt.plot(plot_days, plot_profit)
    plt.ylabel('Net Profit ($)')
    plt.title(save_location.split('/')[-1])
    plt.savefig(save_location + '.png', bbox_inches='tight')
    plt.close()



class Test:
    def __init__(self, date, spx):
        self.date = datetime.strptime(date, '%m/%d/%Y').date()
        self.spx = spx


def main():
    date = Test('04/13/2005', 1173.79)
    date1 = Test('04/27/2005', 1156.38)
    date2 = Test('05/16/2018', 2722.46)
    plot_multiple_days([date, date1, date2])


if __name__ == '__main__':
    results = main()
    print('done')

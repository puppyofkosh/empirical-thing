import datetime
import matplotlib.pyplot as plt
from scipy import linspace, polyval, polyfit, sqrt, stats, randn

MONTH_TO_BUGS = {
    datetime.date(2014, 1, 1): {'buggy_fixes': 2, 'total_fixes': 110},
    datetime.date(2014, 2, 1): {'buggy_fixes': 4, 'total_fixes': 97},
    datetime.date(2014, 3, 1): {'buggy_fixes': 3, 'total_fixes': 95},
    datetime.date(2014, 4, 1): {'buggy_fixes': 5, 'total_fixes': 106},
    datetime.date(2014, 5, 1): {'buggy_fixes': 7, 'total_fixes': 160},
    datetime.date(2014, 6, 1): {'buggy_fixes': 4, 'total_fixes': 109},
    datetime.date(2014, 7, 1): {'buggy_fixes': 6, 'total_fixes': 100},
    datetime.date(2014, 8, 1): {'buggy_fixes': 8, 'total_fixes': 138},
    datetime.date(2014, 9, 1): {'buggy_fixes': 8, 'total_fixes': 189},
    datetime.date(2014, 10, 1): {'buggy_fixes': 5, 'total_fixes': 175},
    datetime.date(2014, 11, 1): {'buggy_fixes': 4, 'total_fixes': 176},
    datetime.date(2014, 12, 1): {'buggy_fixes': 5, 'total_fixes': 153},
    datetime.date(2015, 1, 1): {'buggy_fixes': 7, 'total_fixes': 229},
    datetime.date(2015, 2, 1): {'buggy_fixes': 7, 'total_fixes': 223},
    datetime.date(2015, 3, 1): {'buggy_fixes': 10, 'total_fixes': 232},
    datetime.date(2015, 4, 1): {'buggy_fixes': 6, 'total_fixes': 231},
    datetime.date(2015, 5, 1): {'buggy_fixes': 11, 'total_fixes': 276},
    datetime.date(2015, 6, 1): {'buggy_fixes': 8, 'total_fixes': 253},
    datetime.date(2015, 7, 1): {'buggy_fixes': 19, 'total_fixes': 286},
    datetime.date(2015, 8, 1): {'buggy_fixes': 14, 'total_fixes': 225},
    datetime.date(2015, 9, 1): {'buggy_fixes': 10, 'total_fixes': 249},
    datetime.date(2015, 10, 1): {'buggy_fixes': 15, 'total_fixes': 352},
    datetime.date(2015, 11, 1): {'buggy_fixes': 10, 'total_fixes': 333},
    datetime.date(2015, 12, 1): {'buggy_fixes': 7, 'total_fixes': 292},
    datetime.date(2016, 1, 1): {'buggy_fixes': 14, 'total_fixes': 368},
    datetime.date(2016, 2, 1): {'buggy_fixes': 12, 'total_fixes': 383},
    datetime.date(2016, 3, 1): {'buggy_fixes': 17, 'total_fixes': 418},
    datetime.date(2016, 4, 1): {'buggy_fixes': 14, 'total_fixes': 391},
    datetime.date(2016, 5, 1): {'buggy_fixes': 12, 'total_fixes': 424},
    datetime.date(2016, 6, 1): {'buggy_fixes': 18, 'total_fixes': 486},
    datetime.date(2016, 7, 1): {'buggy_fixes': 11, 'total_fixes': 407},
    datetime.date(2016, 8, 1): {'buggy_fixes': 18, 'total_fixes': 570},
    datetime.date(2016, 9, 1): {'buggy_fixes': 9, 'total_fixes': 460},
    datetime.date(2016, 10, 1): {'buggy_fixes': 9, 'total_fixes': 413},
    datetime.date(2016, 11, 1): {'buggy_fixes': 2, 'total_fixes': 203}}

# Return the y values for the l1 regression of x and y
def do_regression(x, y):
    (ar,br)=polyfit(x,y,1)
    xr=polyval([ar,br],x)
    print("slope: {0}, yint: {1}".format(ar, br))
    return xr

def plot_with_best_fit_line(x, y, x_labels,
                            x_title, y_title, title):
    plt.plot(x, y, 'ro')
    y_line = do_regression(x, y)
    plt.plot(x, y_line, 'b-')
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    locs, _ = plt.xticks()
    new_labels = [x_labels[int(i)] if i < len(x_labels) else x_labels[-1]
                  for i in locs]
    plt.xticks(locs, new_labels)
    plt.show()

    
def main():
    dates_x = []
    y1 = []
    y2 = []
    y3 = []

    for month in sorted(MONTH_TO_BUGS):
        dates_x.append(month)
        obj = MONTH_TO_BUGS[month]
        y_val = obj['buggy_fixes']/obj['total_fixes']
        y1.append(y_val)
        y2.append(obj['buggy_fixes'])
        y3.append(obj['total_fixes'])

    x = list(range(0, len(dates_x)))

    plot_with_best_fit_line(x, y2, dates_x,
                            'Month', 'Number of Buggy Bug Fixes',
                            'Number of Buggy Bug Fixes Per Month')
    plot_with_best_fit_line(x, y1, dates_x,
                            'Month', 'Proportion of Buggy Bug Fixes',
                            'Proportion of Buggy Bug Fixes Per Month')
    plot_with_best_fit_line(x, y3, dates_x,
                            'Month', 'Total Bug Fixes',
                            'Bug Fixes Per Month')


if __name__ == "__main__":
    main()

import datetime
import matplotlib.pyplot as plt

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


def main():
    x = []
    y1 = []
    y2 = []
    y3 = []

    for month in sorted(MONTH_TO_BUGS):
        x.append(month)
        obj = MONTH_TO_BUGS[month]
        y_val = obj['buggy_fixes']/obj['total_fixes']
        y1.append(y_val)
        y2.append(obj['buggy_fixes'])
        y3.append(obj['total_fixes'])

    plt.plot(x, y2, 'ro')
    plt.xlabel('Month')
    plt.ylabel('Number of Buggy Bug Fixes')
    plt.title('Number of Buggy Bug Fixes Per Month')
    plt.show()

    plt.plot(x, y1, 'ro')
    plt.xlabel('Month')
    plt.ylabel('Proportion of Buggy Bug Fixes')
    plt.title('Proportion of Buggy Bug Fixes Per Month')
    plt.show()

    plt.plot(x, y3, 'ro')
    plt.xlabel('Month')
    plt.ylabel('Total Bug Fixes')
    plt.title('Bug Fixes Per Month')
    plt.show()

if __name__ == "__main__":
    main()

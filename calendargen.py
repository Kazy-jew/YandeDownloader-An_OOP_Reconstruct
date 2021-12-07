from datetime import date, timedelta, datetime
import os

if not os.path.exists('./current_dl'):
    os.mkdir('./current_dl')


class Calendar:
    def __init__(self):
        self.year = 2021
        self.date_list = []

    def set_year(self, year):
        self.year = year

    def date_range(self, start, end):
        delta = end - start
        date_lis = []
        for i in range(delta.days+1):
            date_lis.append(str(start+timedelta(days=i)))
        with open('./current_dl/dl_date.txt', 'w') as f:
            for _ in date_lis:
                f.write('{}\n'.format(_))
        date_lis = [_.replace('{}-'.format(self.year), '') for _ in date_lis]
        return date_lis

    # for monthly
    def dates_input(self):
        date_in = [x for x in input('please input a date range(month, date, date): ').split()]
        self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                              int('{:>2}'.format(date_in[0])),
                                              int('{:>2}'.format(date_in[1]))),
                                         date(int('{}'.format(self.year)),
                                              int('{:>2}'.format(date_in[0])),
                                              int('{:>2}'.format(date_in[2]))))
        print(self.date_list)
        return self.date_list

    # for cross-months
    def input_dates(self):
        d = [x for x in input('please input a date range(month, date, month, date): ').split()]
        self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                              int('{:>2}'.format(d[0])),
                                              int('{:>2}'.format(d[1]))),
                                         date(int('{}'.format(self.year)),
                                              int('{:>2}'.format(d[2])),
                                              int('{:>2}'.format(d[3]))))
        print(self.date_list)
        return self.date_list


if __name__ == "__main__":
    now = datetime.now()
    nowdate = now.date()
    then = date(2021, 7, 15)
    delta = nowdate - then
    print(now, then, delta)
from datetime import date, timedelta, datetime
from weburl import SiteSpace
import os

if not os.path.exists('./current_dl'):
    os.mkdir('./current_dl')


class Calendar(SiteSpace):
    def __init__(self):
        super(Calendar, self).__init__()
        self.year = 2022
        self.form = 'date'
        self.date_list = []

    def set_year(self, year):
        self.year = year

    def date_range(self, start, end):
        delta = end - start
        date_lis = []
        for i in range(delta.days+1):
            date_lis.append(str(start+timedelta(days=i)))
        date_lis = [_.replace('{}-'.format(self.year), '') for _ in date_lis]
        return date_lis

    # generate dates list [month-date, month-date]
    def input_dates(self):
        while not self.date_list:
            date_in = [x for x in input('please input a date range (format: m or m/d/d or m/d/m/d for cross-months): ').split('/')]
            if len(date_in) == 1:
                self.form = 'month'
                if int(date_in[0]) != 12:
                    self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                          int('{:>2}'.format(date_in[0])),
                                                          int('{:>2}'.format(1))),
                                                     date(int('{}'.format(self.year)),
                                                          int('{:>2}'.format(date_in[0]))+1,
                                                          int('{:>2}'.format(1))))
                    self.date_list = self.date_list[:-1]
                else:
                    self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                          int('{:>2}'.format(date_in[0])),
                                                          int('{:>2}'.format(1))),
                                                     date(int('{}'.format(self.year)),
                                                          int('{:>2}'.format(date_in[0])),
                                                          int('{:>2}'.format(31))))
            elif len(date_in) == 3:
                self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(date_in[0])),
                                                      int('{:>2}'.format(date_in[1]))),
                                                 date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(date_in[0])),
                                                      int('{:>2}'.format(date_in[2]))))
            elif len(date_in) == 4:
                self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(date_in[0])),
                                                      int('{:>2}'.format(date_in[1]))),
                                                 date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(date_in[2])),
                                                      int('{:>2}'.format(date_in[3]))))
            else:
                print("Invalid Form !")
        print(self.date_list)
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'w') as f:
            for _ in self.date_list:
                f.write('{}-{}\n'.format(self.year, _))
        return self.date_list


if __name__ == "__main__":
    # now = datetime.now()
    # nowdate = now.date()
    # then = date(2021, 7, 15)
    # delta_ = nowdate - then
    # print(now, then, delta_)
    Calendar().input_dates()

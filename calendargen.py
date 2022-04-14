from datetime import date, timedelta, datetime
from pathlib import Path
from weburl import Site
import settings


class Calendar(Site):
    def __init__(self):
        super(Calendar, self).__init__()
        self.form = 'date'
        self.year = 2022
        self.date_list = []
        self.grouped_date_list = []

    def init_year(self):
        self.year = settings.config[self.site_tag]["year"]

    def set_year(self):
        y = input('please enter za year: ')
        settings.config[self.site_tag]["year"] = int(y)
        self.year = int(y)
        self.date_list = []
        print(f'set {self.site} download year to {y}...')
        settings.write_config()
        return int(y)

    def date_range(self, start, end):
        delta = end - start
        date_lis = []
        for i in range(delta.days+1):
            date_lis.append(str(start+timedelta(days=i)))
        date_lis = [_.replace('{}-'.format(self.year), '') for _ in date_lis]
        return date_lis

    def group_dates(self, interval=1):
        if not self.date_list:
            self.input_dates()
        dates = self.date_list
        start_month = int(dates[0][:2])
        end_month = int(dates[-1][:2])
        index = 0
        for i in range(start_month, end_month+1, interval):
            grouped_date_list = [x for x in self.date_list if i <= int(x[:2]) < i + interval]
            self.grouped_date_list.insert(index, grouped_date_list)
            index += 1
        return self.grouped_date_list

    # generate dates list [month-date, month-date]
    def input_dates(self):
        date_in = [x for x in input(
            'please input a date range (format: m or m/d or m/d/d or m/d/m/d for cross-months): ').split('/')]
        try:
            start_month = int(date_in[0])
            end_month = int(date_in[-1])
            if start_month < 1 and end_month > 12:
                print("not a valid date range!")
                raise SystemExit(-1)
        except ValueError:
            print("not a valid date format!")
            raise SystemExit(-1)
        if len(date_in) == 1:
            self.form = 'month'
            if int(date_in[0]) != 12:
                self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(
                                                          date_in[0])),
                                                      int('{:>2}'.format(1))),
                                                 date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(
                                                          date_in[0]))+1,
                                                      int('{:>2}'.format(1))))
                self.date_list = self.date_list[:-1]
            else:
                self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(
                                                          date_in[0])),
                                                      int('{:>2}'.format(1))),
                                                 date(int('{}'.format(self.year)),
                                                      int('{:>2}'.format(
                                                          date_in[0])),
                                                      int('{:>2}'.format(31))))
        elif len(date_in) == 2:
            self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[0])),
                                                  int('{:>2}'.format(date_in[1]))),
                                             date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[0])),
                                                  int('{:>2}'.format(date_in[1]))))
        elif len(date_in) == 3:
            self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[0])),
                                                  int('{:>2}'.format(date_in[1]))),
                                             date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[0])),
                                                  int('{:>2}'.format(date_in[2]))))
        elif len(date_in) == 4:
            self.date_list = self.date_range(date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[0])),
                                                  int('{:>2}'.format(date_in[1]))),
                                             date(int('{}'.format(self.year)),
                                                  int('{:>2}'.format(
                                                      date_in[2])),
                                                  int('{:>2}'.format(date_in[3]))))
        else:
            print("Invalid Form !")
            self.input_dates()
        # print(self.date_list)
        if not Path('./current_dl').exists():
            Path('./current_dl').mkdir(exist_ok=True)
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'w') as f:
            for _ in self.date_list:
                f.write('{}-{}\n'.format(self.year, _))
        return self.date_list


if __name__ == "__main__":
    # now = datetime.now()
    # nowdate = now.date()
    # then = date(2021, 7, 15)
    # print(datetime.fromtimestamp(1592661641).day)
    Calendar().group_dates(3)
    # delta_ = nowdate - then
    # print(now, then, delta_)
    # Calendar().input_dates()

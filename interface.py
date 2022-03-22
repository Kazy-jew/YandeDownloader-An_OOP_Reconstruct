from weburl import Site
from crawler import Downloader
from archiver import Archive
from settings import config
import os
# from pprint import pprint
# import requests


class Yande_re(Site, Archive, Downloader):
    
    def __init__(self):
        super(Yande_re, self).__init__()
        self.set_site('yande')
        self.init_year()
        self.set_download_path()
        print(config[self.tag])

    @staticmethod
    def welcome():
        print('  Welcome to Yande.re Downloader !  ')
        print('------------------------------------------')
        print('|****************************************|')
        print('|*** 1.download  2.download remaining ***|')
        print('|*** 3.update    4.update remaining *****|')
        print('|*** 5.set year  6.exit               ***|')
        print('|****************************************|')
        print('------------------------------------------')

    # download
    def bulk_dl(self):
        dates = self.input_dates()
        self.sln_multi_dates(dates)
        # return
        original_id = self.get_id(dates)
        id_list = original_id
        sgl = 's'  # input('Enter s to start or q to quit: \n(If encountered disk space issue and \n
        # reselected date range, '
        # 'enter q to quit and select "download remaining")')
        if sgl == 's':
            self.downloader_y(dates, original_id, id_list, eigenvalue=1)
        elif sgl == 'q':
            print('download aborted')
            return
        else:
            print('invalid input !')

    # check unfinished
    def chk_dl(self, eigenvalue=1):
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'r') as r:
            dates = r.read().splitlines()
        dates = [x.replace(f'{self.year}-', '') for x in dates if str(self.year) in x]
        original_id = self.check_dl(dates)
        remain_id = self.remain_id()
        self.downloader_y(dates, original_id, remain_id, eigenvalue)

    # check update
    def update_chk(self):
        eigenvalue = 2
        dates = self.input_dates()
        self.multi_dates(dates)
        original_id = self.update(dates)
        update_id = self.get_id(dates)
        self.downloader_y(dates, original_id, update_id, eigenvalue)

    # check unfinished update
    def update_chk_dl(self):
        eigenvalue = 2
        self.chk_dl(eigenvalue)

    def downloader_y(self, dates, original_id, id_list, eigenvalue):
        # original_id: 初始id列表
        # id_list: 当前列表(需要下载的列表)
        # eigenvalue的值(1 or 2)用来区别1:初次下载时/ 2: update时, 下载完成后文件夹的创建和文件的移动
        # fin用于处理源网站图库更新后(图片由于不合要求被moderator删除)新的图片列表和本地的图片列表不一致的情况
        # while及count_num用于处理本地网络原因导致的图片下载失败/同时检查源网页图片是否已被删除
        original_list = original_id
        count_num = 0
        fin = True
        while id_list:
            self.sln_download(id_list, count_num, True)
            self.check_dl(dates)
            id_list = self.remain_id()
            count_num += 1
            print('Retry times left:', 4 - count_num)
            # 退出，同时检查源网页图片是否已被删除
            if count_num == 4:
                # id_list为未下载的图片id, fin = True时，代表源网页的图片已删除， 否则fin = 未下载的图片列表
                fin = self.remove_deleted(id_list)
                break
        # 源网页的图片已删除时，更新本地图片列表文件(单个日期的图片列表文件不做改动)
        if fin is True:
            print('All images downloaded successfully')
            if id_list:
                new_list = list(set(original_list) - set(id_list))
                self.rewrite(dates, new_list)
            if eigenvalue == 1:
                self.move(dates)
            else:
                self.move(dates, updates=True)
            self.flush_update(dates)
        # 下载失败时，检查 & 下载或直接归档
        else:
            print('Please check the info above')
            tsuzuku = input("Do you want to proceed archiving with broken downloads? s to proceed any else to quit: ")
            if tsuzuku == 's':
                if eigenvalue == 1:
                    self.move(dates)
                else:
                    self.move(dates, updates=True)
                self.flush_update(dates)
            else:
                return

    def run(self):
        self.welcome()
        while True:
            choice = input('select option: ')
            if choice == '1':
                self.bulk_dl()
            elif choice == '2':
                self.chk_dl()
            elif choice == '3':
                self.update_chk()
            elif choice == '4':
                self.update_chk_dl()
            elif choice == '5':
                self.year = self.set_year()
            elif choice == '6':
                raise SystemExit(1)
            else:
                print('Invalid Input !')


class Konachan(Site, Archive, Downloader):

    def __init__(self):
        super(Konachan, self).__init__()
        self.set_site('konachan')
        self.init_year()
        self.set_download_path()
        print(config[self.tag])

    @staticmethod
    def welcome():
        print('   Welcome to Konachan Downloader ! ')
        print('--------------------------------------')
        print('|************************************|')
        print('|*** 1.download   2.the remaining ***|')
        print('|*** 3.set year   4.exit          ***|')
        print('|************************************|')
        print('¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')
        # print(Konachan.date_link)
        # pprint(dir(Konachan()))

    def bulk_dl(self):
        dates = self.input_dates()
        self.sln_multi_dates(dates, True)
        self.chk_dl()
        # id_list = archive.get_id(dates)
        # print(id_list)
        # self.downloader_k(dates, id_list)

    def chk_dl(self):
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'r') as r:
            dates = r.read().splitlines()
        dates = [x.replace(f'{self.year}-', '') for x in dates]
        print(dates)
        print('check {}'.format([self.site + '.' + str(self.year) + '-' + x + '.txt' for x in dates]))
        self.check_dl(dates)
        id_list = self.remain_id()
        self.downloader_k(dates, id_list)

    def downloader_k(self, dates, id_list):
        retry = 0
        while id_list:
            self.sln_download(id_list, retry, True)
            self.check_dl(dates)
            retry += 1
            id_list = self.remain_id()
        # archive.move(dates, prefix='Konachan.com')
        if self.form == 'month':
            self.month_mv(dates)
        else:
            self.move(dates)
        for _ in dates:
            os.remove('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, _))
        # os.remove('./current_dl/{}.{0}-{1}_{0}-{2}.txt'.format(self.site, self.year, dates[0], dates[-1]))

    def run(self):
        self.welcome()
        while True:
            choice = input('select operation: ')
            if choice == '1':
                self.bulk_dl()
            elif choice == '2':
                self.chk_dl()
            elif choice == '3':
                self.set_year()
            elif choice == '4':
                raise SystemExit(1)
            else:
                print('Invalid Input')


class Minitokyo(Site, Archive, Downloader):
    def __init__(self):
        super(Minitokyo, self).__init__()
        self.set_site('minitokyo')
    latest_id = ''
    pass


if __name__ == "__main__":
    pass
    # requests.get('https://konachan.com/post?page=1&tags=date%3A2021-12-01')
    # Konachan().run()
    # print(Yande_re().year)

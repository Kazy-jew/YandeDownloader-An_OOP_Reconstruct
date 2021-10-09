from calendargen import Calendar
from crawler import Downloader
import archive
import os

curt_year = Calendar().year


class Yande_re(Downloader):
    
    def __init__(self):
        super(Yande_re, self).__init__()

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
        self.multi_dates(dates)
        original_id = archive.get_id(dates)
        id_list = original_id
        sgl = input('Enter s to start or q to quit: \n(If encountered disk space issue and reselected date range,'
                    'enter q to quit and select "download remaining")')
        if sgl == 's':
            self.downloader_y(dates, original_id, id_list)
        elif sgl == 'q':
            print('download aborted')
            return
        else:
            print('invalid input !')

    # check unfinished
    def chk_dl(self):
        with open('./current_dl/dl_date.txt', 'r') as r:
            dates = r.read().splitlines()
        original_id = archive.check_dl(dates)
        remain_id = archive.remain_id()
        self.downloader_y(dates, original_id, remain_id)

    # check update
    def update_chk(self):
        eigenvalue = 2
        dates = self.input_dates()
        self.multi_dates(dates)
        original_id = archive.update(dates)
        update_id = archive.get_id(dates)
        self.downloader_y(dates, original_id, update_id, eigenvalue)

    # check unfinished update
    def update_chk_dl(self):
        eigenvalue = 2
        with open('./current_dl/dl_date.txt', 'r') as r:
            dates = r.read().splitlines()
        original_id = archive.check_dl(dates)
        remain_id = archive.remain_id()
        self.downloader_y(dates, original_id, remain_id, eigenvalue)

    def downloader_y(self, dates, original_id, id_list, eigenvalue=1):
        # original_id: 初始id列表
        # id_list: 当前列表(需要下载的列表)
        # eigenvalue的值(1 or 2)用来区别1:初次下载时/ 2: update时, 下载完成后文件夹的创建和文件的移动
        # fin用于处理源网站图库更新后(图片由于不合要求被moderator删除)新的图片列表和本地的图片列表不一致的情况
        # while及count_num用于处理本地网络原因导致的图片下载失败/同时检查源网页图片是否已被删除
        original_list = original_id
        count_num = 0
        fin = True
        while id_list:
            self.sln_download(id_list)
            archive.check_dl(dates)
            id_list = archive.remain_id()
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
                archive.rewrite(dates, new_list)
            if eigenvalue == 1:
                archive.move(dates)
            else:
                archive.move(dates, updates=True)
            archive.flush_update(dates)
        # 下载失败时，检查 & 下载或直接归档
        else:
            print('Please check the info above')
            tsuzuku = input("Do you want to proceed archiving with broken downloads? s to proceed any else to quit: ")
            if tsuzuku == 's':
                if eigenvalue == 1:
                    archive.move(dates)
                else:
                    archive.move(dates, updates=True)
                archive.flush_update(dates)
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
                set_year = input('please enter za year:')
                global curt_year
                curt_year = self.set_year(int(set_year))
            elif choice == '6':
                exit()
            else:
                print('Invalid Input !')


class Konachan(Downloader):

    def __init__(self):
        super(Konachan, self).__init__()

    @staticmethod
    def welcome():
        print('   Welcome to Konachan Downloader ! ')
        print('--------------------------------------')
        print('|************************************|')
        print('|*** 1.download   2.the remaining ***|')
        print('|*** 3. exit                      ***|')
        print('|************************************|')
        print('¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')

    def bulk_dl(self):
        dates = self.dates_input()
        self.multi_dates(dates)
        id_list = archive.get_id(dates)
        self.downloader_k(dates, id_list)

    def chk_dl(self):
        with open('./current_dl/dl_date.txt', 'r') as r:
            dates = r.read().splitlines()
        print(dates)
        id_list = archive.check_dl(dates, prefix='Konachan.com')
        self.downloader_k(dates, id_list)

    def downloader_k(self, dates, id_list):
        while id_list:
            self.sln_download(id_list)
            id_list = archive.check_dl(dates, prefix='Konachan.com')
        archive.move(dates, prefix='Konachan.com')
        for _ in dates:
            os.remove('./{}-{}'.format(self.year, _))
        os.remove('./{}_{}'.format(dates[0], dates[-1]))

    def run(self):
        self.welcome()
        while True:
            choice = input('select operation')
            if choice == '1':
                self.bulk_dl()
            elif choice == '2':
                self.chk_dl()
            elif choice == '3':
                exit()
            else:
                print('Invalid Input')


class Minitokyo:
    pass

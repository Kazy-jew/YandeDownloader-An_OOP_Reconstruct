import time

from crawler import Downloader
from archiver import rmdir_current_dl
import settings
# from pprint import pprint


class Yande_re(Downloader):

    def __init__(self):
        super(Yande_re, self).__init__()
        self.set_site('yande')
        self.init_year()
        self.set_download_path()
        print([{k: v} for k, v in settings.config[self.site_tag].items()][:2])

    @staticmethod
    def welcome():
        print('         Welcome to Yande.re Downloader !     ')
        print('------------------------------------------------------')
        print('|****************************************************|')
        print('|*** 1.download(date)  2.download remaining(date) ***|')
        print('|*** 3.update(date)    4.update remaining(date)   ***|')
        print('|*** 5.download(tag)   6.check remaining(tag)     ***|')
        print('|*** 7.update(tag)     8.?????????????????????    ***|')
        print('|*** 9.set year        10.exit                    ***|')
        print('|****************************************************|')
        print('-----------------------------------------------------|')

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
                self.tag_dl()
            elif choice == '6':
                self.check_tag()
            elif choice == '7':
                pass
            elif choice == '8':
                pass
            elif choice == '9':
                self.year = self.set_year()
            elif choice == '10' or 'q':
                raise SystemExit(1)
            else:
                print('Invalid Input !')

    # init essential self properties
    def init_(self):
        pass

    # download
    def bulk_dl(self):
        settings.Img_data = {}
        grouped_dates = self.group_dates(interval=3)
        for dates in grouped_dates:
            self.date_list = dates
            json_info = self.init_json_path()
            self.sln_multi_dates(dates)
            original_id = self.get_id(dates)
            id_list = original_id
            sgl = 's'
            # ''' input('Enter s to start or q to quit: \n(If encountered disk space issue and \n
            #  reselected date range,
            #  enter q to quit and select "download remaining")')'''
            if sgl == 's':
                self.downloader_y(dates, original_id, id_list, eigenvalue=1, json_info=json_info)
            elif sgl == 'q':
                print('download aborted')
                return
            else:
                print('invalid input !')
                raise SystemExit(2)

    # check unfinished
    def chk_dl(self, eigenvalue=1):
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'r') as r:
            dates = r.read().splitlines()
        dates = [x.replace(f'{self.year}-', '')
                 for x in dates if str(self.year) in x]
        self.date_list = dates
        json_info = self.init_json_path()
        original_id = self.check_dl(dates)
        remain_id = self.remain_id()
        self.downloader_y(dates, original_id, remain_id, eigenvalue, json_info=json_info)

    # check update
    def update_chk(self):
        eigenvalue = 2
        dates = self.input_dates()
        self.date_list = dates
        json_info = self.init_json_path()
        self.sln_multi_dates(dates)
        original_id = self.update(dates)
        update_id = self.get_id(dates)
        self.downloader_y(dates, original_id, update_id, eigenvalue, json_info=json_info)

    # check unfinished update
    def update_chk_dl(self):
        eigenvalue = 2
        self.chk_dl(eigenvalue)

    # download by tag(s)
    def tag_dl(self):
        self.dl_tag = input("please input the tag you want to download: ")
        json_info = self.init_json_path()
        if settings.read_data(self.data_folder, self.data_file):
            tag_list = [*settings.Img_data]
        else:
            tag_list = self.sln_tags(self.dl_tag)
        self.downloader_tag(tag_list, json_info)
    
    def check_tag(self):
        if not self.dl_tag:
            self.dl_tag = input("please input the tag you want to check: ")
        json_info = self.init_json_path()
        remain_list = self.check_tag_dl(self.dl_tag)
        if remain_list:
            self.downloader_tag(remain_list, json_info)

    # download by date
    def downloader_y(self, dates, original_id, id_list, eigenvalue, json_info=True):
        # original_id: 初始id列表
        # id_list: 当前列表(需要下载的列表)
        # eigenvalue的值(1 or 2)用来区别1:初次下载时/ 2: update时, 下载完成后文件夹的创建和文件的移动
        # fin用于处理源网站图库更新后(图片由于不合要求被moderator删除)新的图片列表和本地的图片列表不一致的情况
        # while及count_num用于处理本地网络原因导致的图片下载失败/同时检查源网页图片是否已被删除
        # fetch_info_only: fetch image info without downloading --
        # need to change Downloader.check_complete to True
        fetch_info_only = True
        original_list = original_id
        count_num = 0
        fin = True
        while id_list:
            # fetch info only
            if not settings.Img_data:
                settings.read_data(self.data_folder, self.data_file)
            print(f'{len(original_list)} images id in total')
            print(f'{len(settings.Img_data)} images have a json index')
            id_list = [x for x in id_list if len(settings.Img_data[x]) == 2]
            print(f'{len(id_list)} of total {len(settings.Img_data)} images have no info')
            if not id_list:
                print(f"No update of json data {self.data_file}")
                time.sleep(2)
                return 
            finish = self.sln_download(id_list, max_wait_time=60, json_info=json_info, js=self.use_js)
            if not finish:
                print("sleeping...")
                time.sleep(1000)
                continue
            if fetch_info_only:
                time.sleep(2)
                print(f"json data {self.data_file} fetch finished...")
                return
            self.check_dl(dates)
            id_list = self.remain_id()
            if id_list:
                print('Retry times left:', 3 - count_num)
            # 退出，同时检查源网页图片是否已被删除
            if count_num == 3:
                # id_list为未下载的图片id, fin = True时，代表源网页的图片已删除， 否则fin = 未下载的图片列表
                fin = self.sln_remove_deleted(id_list)
                break
            count_num += 1
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
            tsuzuku = input(
                "Do you want to proceed archiving with broken downloads? s to proceed any else to quit: ")
            if tsuzuku == 's':
                if eigenvalue == 1:
                    self.move(dates)
                else:
                    self.move(dates, updates=True)
                self.flush_update(dates)
            else:
                return

    # download by tag
    def downloader_tag(self, tag_list, json_info):
        retry_num = 0
        going = []
        dl_tag_list = [x for x in tag_list if not settings.Img_data[x].get('download_state')]
        print(f"{len(dl_tag_list)} in array...")
        while dl_tag_list:
            self.sln_download(dl_tag_list, max_wait_time=60, json_info=json_info, js=self.use_js)
            dl_tag_list = self.check_tag_dl(self.dl_tag)
            going = dl_tag_list
            retry_num += 1
            print('Retry times left: ', 4 - retry_num)
            if retry_num == 4:
                going = self.check_tag_dl(self.dl_tag)
                break
        if not going:
            print('All images downloaded successfully')
        else:
            print('check fail info')
            for x in going:
                print(f'{settings.Img_data[x]["id"]}: {settings.Img_data[x]["file_url"]}\n')


class Konachan(Downloader):

    def __init__(self):
        super(Konachan, self).__init__()
        self.set_site('konachan')
        self.init_year()
        self.set_download_path()
        print(settings.config[self.site_tag])

    @staticmethod
    def welcome():
        print('   Welcome to Konachan Downloader !   ')
        print('--------------------------------------')
        print('|************************************|')
        print('|*** 1.download      2.check   ******|')
        print('|*** 4.download(tag) 4.check(tag) ***|')
        print('|*** 5.set year      6.exit   *******|')
        print('|************************************|')
        print('¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')
        # print(Konachan.date_link)
        # pprint(dir(Konachan()))

    def run(self):
        self.welcome()
        while True:
            choice = input('select operation: ')
            if choice == '1':
                self.bulk_dl()
            elif choice == '2':
                self.chk_dl()
            elif choice == '3':
                self.tag_dl()
            elif choice == '4':
                self.check_tag()
            elif choice == '5':
                self.set_year()
            elif choice == '6' or 'q':
                raise SystemExit(1)
            else:
                print('Invalid Input')

    def bulk_dl(self):
        dates = self.input_dates()
        self.date_list = dates
        json_info = self.init_json_path()
        self.sln_multi_dates(dates)
        # self.chk_dl()
        id_list = self.get_id(dates)
        # print(id_list)
        self.downloader_k(dates, id_list, json_info=json_info)

    def chk_dl(self):
        with open('./current_dl/{}.dl_date.txt'.format(self.site), 'r') as r:
            dates = r.read().splitlines()
        dates = [x.replace(f'{self.year}-', '') for x in dates]
        self.date_list = dates
        json_info = self.init_json_path()
        print('check {}'.format(
            [self.site + '.' + str(self.year) + '-' + x + '.txt' for x in dates]))
        self.check_dl(dates)
        id_list = self.remain_id()
        self.downloader_k(dates, id_list, json_info=json_info)

    def downloader_k(self, dates, id_list, json_info):
        retry = 0
        while id_list:
            self.sln_download(id_list, max_wait_time=60, json_info=json_info, js=self.use_js)
            self.check_dl(dates)
            retry += 1
            id_list = self.remain_id()
        # archive.move(dates, prefix='Konachan.com')
        if self.form == 'month':
            self.month_mv(dates)
        else:
            self.move(dates)
        rmdir_current_dl()
        # os.remove('./current_dl/{}.{0}-{1}_{0}-{2}.txt'.format(self.site, self.year, dates[0], dates[-1]))


class Minitokyo(Downloader):
    def __init__(self):
        super(Minitokyo, self).__init__()
        self.set_site('minitokyo')
    latest_id = ''
    pass


if __name__ == "__main__":
    # pass
    Yande_re().check_tag()
    # requests.get('https://konachan.com/post?page=1&tags=date%3A2021-12-01')
    # Konachan().run()
    # print(Yande_re().year)

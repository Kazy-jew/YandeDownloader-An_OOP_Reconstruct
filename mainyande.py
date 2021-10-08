from calendargen import Calendar
from crawler import Page_ID, Downloader
import archive
import os

def downloader(dates, original_id, id_list, eigenvalue):
    # original_id: 初始id列表
    # id_list: 当前列表(需要下载的列表)
    # eigenvalue的值(1 or 2)用来区别1:初次下载时/ 2: update时, 下载完成后文件夹的创建和文件的移动
    # fin用于处理源网站图库更新后(图片由于不合要求被moderator删除)新的图片列表和本地的图片列表不一致的情况
    # while及count_num用于处理本地网络原因导致的图片下载失败/同时检查源网页图片是否已被删除
    original_list = original_id
    count_num = 0
    fin = True
    while id_list:
        Downloader.sln_download(id_list)
        archive.check_dl(dates)
        id_list = archive.remain_id()
        count_num += 1
        print('Retry times left:', 4 - count_num)
        # 退出，同时检查源网页图片是否已被删除
        if count_num == 4:
            # id_list为未下载的图片id, fin = True时，代表源网页的图片已删除， 否则fin = 未下载的图片列表
            fin = Page_ID.remove_deleted(id_list)
            break
    # 源网页的图片已删除时，更新本地列表(单个日期的图片列表不做改动)
    if fin is True:
        print('All images downloaded successfully')
        if id_list:
            new_list = list(set(original_list) - set(id_list))
            archive.rewrite(dates, new_list)
        if eigenvalue == 1:
            archive.move(dates)
        else:
            archive.move(dates, update=True)
        archive.flush_update(dates)
    # 下载失败时，检查 & 下载或直接归档
    else:
        print('Please check the info above')
        tsuzuku = input("Do you want to proceed archiving with broken downloads? s to proceed any else to quit: ")
        if tsuzuku == 's':
            if eigenvalue == 1:
                archive.move(dates)
            else:
                archive.move(dates, update=True)
            archive.flush_update(dates)
        else:
            return


class Yande_re:

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

    @staticmethod
    def bulk_dl():
        dates = Calendar().input_dates()

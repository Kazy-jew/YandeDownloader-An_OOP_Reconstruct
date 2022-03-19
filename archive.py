"""
retrieving & updating & merging the id list, archive id list after download finished
"""
import re
import os
import shutil
from calendargen import Calendar


# for windows
def syspath():
    # dl_path = os.path.expanduser('~')
    # dl_path = os.path.join(dl_path, r'\Downloads')
    dl_path = r'D:\Konachantest'
    return dl_path


curt_year = Calendar().year
path = syspath()


# get_id是为了在继续下载时覆盖dates_list里原有的初始id列表，如在磁盘空间有限时，退出程序重新选择一小部分日期下载
def get_id(dates):
    id_list = []
    if dates:
        # 更新下载日期范围
        with open('./current_dl/dl_date.txt', 'w') as dl:
            for _ in dates:
                dl.write('{}\n'.format(_))
        with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1])) as f:
            id_list += f.read().splitlines()
    else:
        print('No date file!')
    return id_list


# raw_id为直接从原始id列表合并的初始列表
def raw_id(dates):
    id_list = []
    with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1])) as k:
        id_list += k.read().splitlines()
    return id_list


# 未下载的id列表
def remain_id():
    remain_list = []
    with open('./current_dl/remain_dl.txt') as r:
        remain_list += r.read().splitlines()
    return remain_list


def update_id(dates):
    update_list = []
    for _ in dates:
        list_update = os.listdir('./updated_list')
        if 'img_list_{}-{}.txt'.format(curt_year, _) in list_update:
            with open('./updated_list/img_list_{}-{}.txt'.format(curt_year, _)) as r:
                update_list += r.read().splitlines()
    if len(update_list) > 0:
        print('update start...')
    return update_list


def rewrite(dates, new_list):
    # 更新初始列表文件，将源已删除的图片id去除
    with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1]), 'w') as rw:
        for _ in new_list:
            rw.write('{}\n'.format(_))
    print('List updated')
    return


# list3：初始id列表，list2: 已下载的id列表，list1: 下载的文件；返回初始列表, for yande.re
def check_dl(dates, prefix='yande.re'):
    print(dates[0], dates[-1])
    list1 = os.listdir(path)
    list2 = []
    list3 = []
    if (not os.path.exists("./current_dl/dl_date.txt")) or (not os.path.exists('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1]))):
        print('nothing remain to be downloaded')
        return
    for name in list1:
        if name.startswith(prefix) and (not name.endswith('crdownload')) and os.path.isfile(path + '\\' + name):
            # can use match case here after python 3.10
            if prefix == 'yande.re':
                list2.append(name.split(' ')[1])
            elif prefix == 'Konachan.com':
                list2.append(name.split(' ')[2])
    # print(list2)
    # os.system("pause")
    with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1])) as k:
        list3 += k.read().splitlines()
    diff = list(set(list3) - set(list2))
    if 0 < len(diff) <= 10:
        print('remain to be downloaded', diff)
    else:
        print('{} items remain'.format(len(diff)))
    with open('./current_dl/remain_dl.txt', 'w') as m:
        for _ in diff:
            m.write('{}\n'.format(_))
    if len(diff) == 0:
        print('No images to download')
    return list3


def update(dates):
    dates_list = []
    for i in dates:
        with open('./current_dl/{}-{}.txt'.format(curt_year, i)) as p:
            li1 = p.read().splitlines()
        with open('./namelist_date/nl_{}-{}.txt'.format(curt_year, i)) as q:
            li2 = q.read().splitlines()
        updated_img = list(set(li1) - set(li2))
        dates_list += updated_img
        if updated_img:
            with open('./updated_list/img_list_{}-{}.txt'.format(curt_year, i), 'w') as r:
                for _ in updated_img:
                    r.write('{}\n'.format(_))
        else:
            print('date {} no image updated'.format(i))
    with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1]), 'w') as f:
        for _ in dates_list:
            f.write('{}\n'.format(_))
    return dates_list


def flush_update(dates):
    for _ in dates:
        os.replace('./current_dl/{}-{}.txt'.format(curt_year, _), './namelist_date/nl_{}-{}.txt'.format(curt_year, _))
        # os.replace('./current_dl/{}-{}.txt'.format(curt_year, _), './namelist_date/nl_{}.txt'.format(_))
    return


# 2021 ver
def flush_all():
    list1 = os.listdir('./current_dl')
    list2 = []
    for i in list1:
        if i.startswith('{}'.format(curt_year)):
            list2.append(i)
    for j in list2:
        date = re.sub(r'\.txt$', '', '{}-{}'.format(j.split('-')[-2], j.split('-')[-1]))
        with open('./current_dl/{}'.format(j)) as r:
            list3 = r.read().splitlines()
        with open('./namelist_date/nl_{}-{}.txt'.format(curt_year, date), 'w') as f:
            for _ in list3:
                f.write('{}\n'.format(_))
    return


# archive image file by month
def month_mv(dates, prefix='yande.re', updates=None):
    list1 = os.listdir(path)
    list2 = []
    for i in list1:
        if i.startswith(prefix) and (not i.endswith('crdownload')) and os.path.isfile(path + '\\' + i):
            list2.append(i)
    month = dates[0].split('-')[0]
    if not updates:
        folder = prefix + ' ' + str(curt_year) + '.' + month
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))
        for _ in list2:
            shutil.move(os.path.join(path, _), os.path.join(path, folder))
    else:
        pass


# move image file only, not id list file
def move(dates, prefix='yande.re', updates=None):
    list1 = os.listdir(path)
    list2 = []
    for i in list1:
        if i.startswith(prefix) and (not i.endswith('crdownload')) and os.path.isfile(path + '\\' + i):
            list2.append(i)
    if not updates:
        for m in dates:
            with open('./current_dl/{}-{}.txt'.format(curt_year, m)) as r:
                pair = r.read().splitlines()
            folder = prefix + ' ' + str(curt_year) + '.' + m.replace('-', '.')
            if not os.path.exists(os.path.join(path, folder)):
                os.makedirs(os.path.join(path, folder))
            if len(list2) == 0:
                print('No file to archive')
            else:
                for item in list2:
                    if prefix == 'Konachan.com':
                        name_id = item.split(' ')[2]
                    elif prefix == 'yande.re':
                        name_id = item.split(' ')[1]
                    else:
                        name_id = item
                    if name_id in pair:
                        shutil.move(os.path.join(path, item), os.path.join(path, folder))
    # for yande.re only
    else:
        folder = 'update_{}-{}'.format(dates[0].replace('-', ''), dates[-1].replace('-', ''))
        if not os.path.exists(os.path.join(path, folder)):
            os.makedirs(os.path.join(path, folder))
        with open('./current_dl/{0}-{1}_{0}-{2}.txt'.format(curt_year, dates[0], dates[-1])) as r:
            pair = r.read().splitlines()
        for item in list2:
            name_id = item.split(' ')[1]
            if name_id in pair:
                shutil.move(os.path.join(path, item), os.path.join(path, folder))
    return


if __name__ == "__main__":
    pass

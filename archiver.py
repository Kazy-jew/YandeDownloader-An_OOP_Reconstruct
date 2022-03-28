"""
retrieving & updating & merging the id list, archive id list after download finished
"""
import re
import os
import shutil
import settings
from pathlib import Path
from calendargen import Calendar


class Archive(Calendar):
    def __init__(self):
        super(Archive, self).__init__()
        self.data_folder = ''
        self.data_file = ''
        self.dl_tag = ''

    def set_download_path(self):
        self.dl_path = settings.config[self.site_tag]["location"]
        if not Path(self.dl_path).exists():
            Path(self.dl_path).mkdir(parents=True)

    def init_json_path(self):
        if self.date_list:
            self.data_folder = self.site_tag + "Data"
            self.data_file = self.site + str(self.year) + "." + self.date_list[0] + "_" + self.date_list[-1]
            return True
        elif self.dl_tag:
            self.data_folder = self.site_tag + "Data" + "/" + "By.Tag"
            self.data_file = self.site + " tag#" + self.dl_tag
            return True
        else:
            return False

    # get_id是为了在继续下载时覆盖dates_list里原有的初始id列表，如在磁盘空间有限时，退出程序重新选择一小部分日期下载
    def get_id(self, dates):
        id_list = []
        if dates:
            # 更新下载日期范围
            with open('./current_dl/{}.dl_date.txt'.format(self.site), 'w') as dl:
                for _ in dates:
                    dl.write('{}-{}\n'.format(self.year, _))
            with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])) as f:
                id_list += f.read().splitlines()
        else:
            print('No date file!')
        return id_list

    # raw_id为直接从原始id列表合并的初始列表
    def raw_id(self, dates):
        id_list = []
        with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])) as k:
            id_list += k.read().splitlines()
        return id_list

    # 未下载的id列表
    def remain_id(self):
        remain_list = []
        with open('./current_dl/{}.remain_dl.txt'.format(self.site)) as r:
            remain_list += r.read().splitlines()
        return remain_list

    def update_id(self, dates):
        update_list = []
        for _ in dates:
            list_update = os.listdir('./updated_list/{}'.format(self.site))
            if 'img_list_{}-{}.txt'.format(self.year, _) in list_update:
                with open('./updated_list/{}/img_list_{}-{}.txt'.format(self.site, self.year, _)) as r:
                    update_list += r.read().splitlines()
        if len(update_list) > 0:
            print('update start...')
        return update_list

    def rewrite(self, dates, new_list):
        # 更新初始列表文件，将源已删除的图片id去除
        with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1]), 'w') as rw:
            for _ in new_list:
                rw.write('{}\n'.format(_))
        print('List updated')
        return

    # list3：初始id列表，list2: 已下载的id列表，list1: 下载的文件；返回初始列表, for yande.re
    def check_dl(self, dates):
        # print(self.prefix)
        list1 = os.listdir(self.dl_path)
        list2 = []
        list3 = []
        data_folder = self.site_tag + "Data"
        data_file = self.site + str(self.year) + '.' + \
            self.date_list[0] + "_" + self.date_list[-1]
        self.data_folder = data_folder
        self.data_file = data_file
        # print(f"{data_folder}/{data_file}.json")
        settings.read_data(data_folder, data_file)
        if not settings.Img_data:
            raise Exception("No json Data file")
        # raise Exception('stop here')
        if (not os.path.exists(f"./current_dl/{self.site}.dl_date.txt")) or (not os.path.exists('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1]))):
            raise Exception('No date or date-lists file !!')
        for name in list1:
            if name.startswith(self.prefix) and (not name.endswith('crdownload')) and os.path.isfile(self.dl_path + r'/'+ name):
                # can use match case here after python 3.10
                if self.prefix == 'yande.re':
                    list2.append(name.split(' ')[1])
                elif self.prefix == 'Konachan.com':
                    list2.append(name.split(' ')[2])
        # print(list2)
        # os.system("pause")
        with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])) as k:
            list3 += k.read().splitlines()
        diff = list(set(list3) - set(list2))
        if len(diff) > 0:
            if len(diff) <= 10:
                print('remain to be downloaded', diff)
            else:
                print('{} items remain'.format(len(diff)))
        else:
            print('No images to download')
        with open(f'./current_dl/{self.site}.remain_dl.txt', 'w') as m:
            for _ in diff:
                # print(_)
                if settings.Img_data.get(_):
                    settings.Img_data[_]["download_state"] = False
                else:
                    print(f"key {_} not find")
                m.write('{}\n'.format(_))
        settings.write_data(data_folder, data_file)
        return list3

    def check_tag_dl(self, tag):
        list_all = os.listdir(self.dl_path)
        list_dl = []
        data_folder = self.site_tag + "Data" + "/" + "By.Tag"
        data_file = self.site + " tag#" + tag
        self.data_folder = data_folder
        self.data_file = data_file
        if not settings.Img_data:
            settings.Img_data = settings.read_data(data_folder, data_file)
        for name in list_all:
            if name.startswith(self.prefix) and (not name.endswith('crdownload')) and os.path.isfile(self.dl_path + '\\' + name):
                # can use match case here after python 3.10
                if self.prefix == 'yande.re':
                    list_dl.append(name.split(' ')[1])
                elif self.prefix == 'Konachan.com':
                    list_dl.append(name.split(' ')[2])
        list_tag = [*settings.Img_data]
        failed_dl = list(set(list_tag) - set(list_dl))
        # print(len(list_tag), len(list_dl), failed_dl)
        if len(failed_dl) > 0:
            if len(failed_dl) <= 10:
                print('remain to be downloaded', failed_dl)
            else:
                print('{} items remain'.format(len(failed_dl)))
            for _ in failed_dl:
                settings.Img_data[_]["download_state"] = False
            settings.write_data(data_folder, data_file)
            return failed_dl
        else:
            print('No images remain to download')
            return None

    def update(self, dates):
        dates_list = []
        if not Path(f'./namelist_date/{self.site}').exists():
            Path(
                f'./namelist_date/{self.site}').mkdir(parents=True, exist_ok=True)
        if not Path(f'./updated_list/{self.site}').exists():
            Path(
                f'./updated_list/{self.site}').mkdir(parents=True, exist_ok=True)
        for i in dates:
            try:
                with open('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, i)) as p:
                    li1 = p.read().splitlines()
                with open('./namelist_date/{}/nl_{}-{}.txt'.format(self.site, self.year, i)) as q:
                    li2 = q.read().splitlines()
            except FileNotFoundError:
                return 'Specific File not Found'
            updated_img = list(set(li1) - set(li2))
            dates_list += updated_img
            if updated_img:
                with open('./updated_list/{}/img_list_{}-{}.txt'.format(self.site, self.year, i), 'w') as r:
                    for _ in updated_img:
                        r.write('{}\n'.format(_))
            else:
                print('date {} no image updated'.format(i))
        with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1]), 'w') as f:
            for _ in dates_list:
                f.write('{}\n'.format(_))
        return dates_list

    def flush_update(self, dates):
        if not Path(f'./namelist_date/{self.site}').exists():
            Path(
                f'./namelist_date/{self.site}').mkdir(parents=True, exist_ok=True)
        for _ in dates:
            Path('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, _)).\
                replace(
                    './namelist_date/{}/nl_{}-{}.txt'.format(self.site, self.year, _))
        shutil.rmtree('./current_dl', ignore_errors=True)
        return

    # copy date id files to namelist folder
    def flush_all(self):
        if not Path(f'./namelist_date/{self.site}').exists():
            Path(
                f'./namelist_date/{self.site}').mkdir(parents=True, exist_ok=True)
        list1 = os.listdir('./current_dl')
        list2 = []
        for i in list1:
            if i.startswith('{}.{}'.format(self.site, self.year)) and ("_" not in i):
                list2.append(i)
        for j in list2:
            date = re.sub(
                r'\.txt$', '', '{}-{}'.format(j.split('-')[-2], j.split('-')[-1]))
            with open('./current_dl/{}'.format(j)) as r:
                list3 = r.read().splitlines()
            with open('./namelist_date/{}/nl_{}-{}.txt'.format(self.site, self.year, date), 'w') as f:
                for _ in list3:
                    f.write('{}\n'.format(_))
        tip = input('remove original files?')
        print(list2)
        if tip == '':
            print('deleting...')
            [Path(f'./current_dl/{x}').unlink(missing_ok=True) for x in list2]
            print('done')
        return

    # archive image file by month
    def month_mv(self, dates, updates=None):
        list1 = os.listdir(self.dl_path)
        list2 = []
        for i in list1:
            if i.startswith(self.prefix) and (not i.endswith('crdownload')) and os.path.isfile(self.dl_path + '\\' + i):
                list2.append(i)
        month = dates[0].split('-')[0]
        if not updates:
            folder = self.prefix + ' ' + str(self.year) + '.' + month
            if not os.path.exists(os.path.join(self.dl_path, folder)):
                os.makedirs(os.path.join(self.dl_path, folder))
            for _ in list2:
                shutil.move(os.path.join(self.dl_path, _),
                            os.path.join(self.dl_path, folder))
        else:
            pass

    # move image file only, not id list file
    def move(self, dates, updates=None):
        list1 = os.listdir(self.dl_path)
        list2 = []
        for i in list1:
            if i.startswith(self.site) and (not i.endswith('crdownload')) and os.path.isfile(self.dl_path + r'/' + i):
                list2.append(i)
        if not updates:
            for m in dates:
                with open('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, m)) as r:
                    pair = r.read().splitlines()
                folder = self.site + ' ' + \
                    str(self.year) + '.' + m.replace('-', '.')
                if not os.path.exists(os.path.join(self.dl_path, folder)):
                    os.makedirs(os.path.join(self.dl_path, folder))
                if len(list2) == 0:
                    print('No file to archive')
                else:
                    for item in list2:
                        if self.prefix == 'Konachan.com':
                            name_id = item.split(' ')[2]
                        elif self.prefix == 'yande.re':
                            name_id = item.split(' ')[1]
                        else:
                            name_id = item
                        if name_id in pair:
                            # shutil.move(os.path.join(path, item), os.path.join(path, folder, item))
                            Path(os.path.join(self.dl_path, item)).replace(
                                os.path.join(self.dl_path, folder, item))
        # for yande.re only
        else:
            folder = '{}.update_{}.{}-{}'.format(
                self.site, self.year, dates[0].replace('-', ''), dates[-1].replace('-', ''))
            if not os.path.exists(os.path.join(self.dl_path, folder)):
                os.makedirs(os.path.join(self.dl_path, folder))
            with open('./current_dl/{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])) as r:
                pair = r.read().splitlines()
            for item in list2:
                name_id = item.split(' ')[1]
                if name_id in pair:
                    shutil.move(os.path.join(self.dl_path, item),
                                os.path.join(self.dl_path, folder))
        return


def rmdir_current_dl():
    shutil.rmtree('./current_dl')


if __name__ == "__main__":
    pass
    # Arch().flush_all()

"""
Downloader core, including fetching id list from web, downloading images & managing
the image list
1.download dates: use date_link
2.download id list: use post_link
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException as TE
from selenium.common.exceptions import NoSuchElementException as NSEE
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from lxml import html
from colorama import Fore, Style
from tqdm import tqdm
from termcolor import colored, cprint
import os
import pyautogui
import re
import requests
import time
import urllib.parse
from archiver import Archive
import settings
import json


class Downloader(Archive):

    def __init__(self):
        super(Downloader, self).__init__()
        self.illustrate = ''
        self.id_list = []

    def sln_chrome(self):
        root = os.path.expanduser('~')
        chrome_data = self.chrome_profile
        # print(chrome_data)
        data_dir = os.path.join(root, chrome_data)
        # print(data_dir)
        chrome_options = Options()
        # change to your own chrome profile path if is not installed with default configuration,
        # you can find it in chrome browser under address chrome://version/
        prefs = {'download.default_directory': self.dl_path}
        chrome_options.add_argument("--user-data-dir={}".format(data_dir))
        # keep browser open
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    # 生成原始id列表(多文件)和合并原始列表后的初始列表(单文件)，返回输入的日期
    def multi_dates(self, dates):
        download_folder = 'current_dl'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        # print(self.date_link)
        # id list of date range
        dates_list = []
        # id list of a date
        for n in dates:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              'Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.277'}
            proxy_url = {'http': '127.0.0.1:7890'}

            date_list = []
            # 已经下载完成的列表不重复下载
            if os.path.exists('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, n)):
                print('list {} already downloaded...'.format(n))
                with open('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, n), 'r') as r:
                    date_list += r.read().splitlines()
            else:
                # print('in else')
                mark_tag = None
                for i in range(1, 36):
                    if not self.date_link:
                        raise ValueError('no effect site link')
                    else:
                        url = self.date_link.format(i, self.year, n)
                    # print(url)
                    # In selenium, you can use driver.page_source to get the same result
                    # source = driver.page_source (here source equals page_.content)
                    # tree = html.fromstring(source)
                    page_ = requests.get(
                        url, headers=headers, proxies=proxy_url)
                    tree = html.fromstring(page_.content)
                    if self.site_tag == 'yande':
                        mark_tag = tree.xpath(
                            '//*[@id="post-list"]/div[2]/div[4]/p/text()')
                    elif self.site_tag == 'konachan':
                        mark_tag = tree.xpath(
                            '//*[@id="post-list"]/div[3]/div[4]/p/text()')
                    if not mark_tag:
                        date_list += tree.xpath(
                            '//*[@id="post-list-posts"]/li/@id')
                    elif mark_tag == ['Nobody here but us chickens!']:
                        date_list = [w.replace('p', '') for w in date_list]
                        break
                with open(os.path.join(download_folder, '{}.{}.txt'.format(self.site, url.split('%3A')[-1])), 'w') as f:
                    for item in date_list:
                        f.write('{}\n'.format(item))
                print('{}...done'.format(url.split('%3A')[-1]))
            dates_list += date_list
        with open(os.path.join(download_folder,
                               '{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])), 'w') as f:
            for item in dates_list:
                f.write('{}\n'.format(item))
        return

    # 确定图片未下载成功的原因：若源已经不存在则输出删除的信息，否则为本地原因 (deprecated)
    def remove_deleted(self, id_list):
        id_to_remove = []
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36'}
        proxy_url = {'http': 'http://127.0.0.1:7890'}
        for _ in tqdm(id_list):
            url = self.post_link.format(_)
            page = requests.get(url, headers=headers, proxies=proxy_url)
            tree = html.fromstring(page.content)
            deleted_info = tree.xpath('//*[@id="post-view"]/div[1]/text()')
            image_info = tree.xpath('//*[@id="image"]')
            if image_info:
                print(Fore.RED + 'Warning !\n',
                      Fore.BLUE + 'Image {} still exists \
                      but failed to be downloaded too many times, '.format(colored(_, 'green')),
                      Fore.BLUE + 'please check manually')
                print(Style.RESET_ALL)
            else:
                print('{}:'.format(_), deleted_info[0])
                # 原post已经删除，需要从列表中去除
                id_to_remove.append(_)
        if len(id_list) == len(id_to_remove):
            # 所有的图片网站上原post已经删除
            return True
        else:
            # 存在未下载成功的图片，返回该图片id列表
            return list(set(id_list) - set(id_to_remove))

    # selenium realization of remove_deleted, for ip restriction
    def sln_remove_deleted(self, id_list):
        id_to_remove = []
        driver = self.sln_chrome()
        print("checking the remaining posts...")
        for _ in tqdm(id_list):
            url = self.post_link.format(_)
            driver.get(url)
            WebDriverWait(driver, 3)
            source = driver.page_source
            tree = html.fromstring(source)
            deleted_info = tree.xpath('//*[@id="post-view"]/div[1]/text()')
            image_info = tree.xpath('//*[@id="image"]')
            if image_info:
                print(Fore.RED + 'Warning !\n',
                      Fore.BLUE + 'Image {} still exists \
                      but failed to be downloaded too many times, '.format(colored(_, 'green')),
                      Fore.BLUE + 'please check manually')
                print(Style.RESET_ALL)
            else:
                print('{}:'.format(_), deleted_info[0])
                # the post is deleted，remove from download list
                id_to_remove.append(_)
        driver.close()
        if len(id_list) == len(id_to_remove):
            # all the remaining post is deleted
            return True
        else:
            # return the failed to download image list
            return list(set(id_list) - set(id_to_remove))

    # selenium realization of multi_dates, for ip restriction of anti-crawler
    def sln_multi_dates(self, dates):
        download_folder = 'current_dl'
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        # print(self.date_link)
        # id list of date range
        dates_list = []
        driver = self.sln_chrome()
        for n in dates:
            # id list of a date
            date_list = []
            # 已经下载完成的列表不重复下载
            if os.path.exists('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, n)):
                print('list {} already downloaded...'.format(n))
                with open('./current_dl/{}.{}-{}.txt'.format(self.site, self.year, n), 'r') as r:
                    date_list += r.read().splitlines()
            else:
                url = self.date_link.format(1, self.year, n)
                driver.get(url)
                try:
                    pages_num_element = driver.find_element(
                        By.XPATH, '//*[@id="paginator"]/div')
                    pages_num = int(pages_num_element.text.split(' ')[-3])
                except NSEE:
                    pages_num = 1
                page_img = driver.find_elements(
                    By.XPATH, '//*[@id="post-list-posts"]/li')
                print('Date {}-{} has {} pages'.format(self.year, n, pages_num))
                date_list += [x.get_attribute('id') for x in page_img]
                # print(self.site, (script and self.site == 'Konachan'))
                # if js and self.site == 'Konachan':
                #     time.sleep(15)
                if pages_num > 1:
                    for i in range(2, pages_num + 1):
                        url = self.date_link.format(i, self.year, n)
                        driver.get(url)
                        page_img = driver.find_elements(
                            By.XPATH, '//*[@id="post-list-posts"]/li')
                        date_list += [x.get_attribute('id') for x in page_img]
                        # if js and self.site == 'Konachan':
                        #     time.sleep(15)
                date_list = [w.replace('p', '') for w in date_list]
                with open(os.path.join(download_folder, '{}.{}.txt'.format(self.site, url.split('%3A')[-1])), 'w') as f:
                    for item in date_list:
                        f.write('{}\n'.format(item))
                print('{}...done'.format(url.split('%3A')[-1]))
            dates_list += date_list
        with open(os.path.join(download_folder,
                               '{0}.{1}-{2}_{1}-{3}.txt'.format(self.site, self.year, dates[0], dates[-1])),
                  'w') as f:
            for item in dates_list:
                f.write('{}\n'.format(item))
        self.id_list = dates_list
        if settings.read_data(self.data_folder, self.data_file, dumb=True):
            print("json data found....")
        else:
            settings.Img_data = {x: {"retrieved": False, "download_state": False} for x in dates_list}
            settings.write_data(self.data_folder, self.data_file)
            print(f"write {self.data_file} to file...")
        driver.close()
        return self.id_list

    # get id list under tag(s)
    def sln_tags(self, tag, js=None):
        tag_list = []
        url = self.tag_link.format(1, tag)
        driver = self.sln_chrome()
        driver.get(url)
        try:
            pages_num_element = driver.find_element(
                By.XPATH, '//*[@id="paginator"]/div')
            pages_num = int(pages_num_element.text.split(' ')[-3])
        except NSEE:
            pages_num = 1
        print(f"tag {tag} has {pages_num} page(s)...")
        page_img = driver.find_elements(
            By.XPATH, '//*[@id="post-list-posts"]/li')
        tag_list += [x.get_attribute('id') for x in page_img]
        if pages_num > 1:
            for i in tqdm(range(2, pages_num + 1)):
                url = self.tag_link.format(i, tag)
                driver.get(url)
                page_img = driver.find_elements(
                    By.XPATH, '//*[@id="post-list-posts"]/li')
                tag_list += [x.get_attribute('id') for x in page_img]
        tag_list = [x.replace('p', '') for x in tag_list]
        for _ in tag_list:
            tag_dict = {_: {"retrieved": False, "download_state": False}}
            settings.Img_data.update(tag_dict)
        tag_folder = self.site_tag + "Data" + "/" + "By.Tag"
        tag_file = self.site + " tag#" + tag
        settings.write_data(tag_folder, tag_file)
        driver.close()
        return tag_list

    # normal
    def download(self, id_list):
        download_folder = self.site + ' ' + \
            re.sub('[-]', '.', self.date_link.split('%3A')[-1])  # 创建下载文件夹
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        print('start downloading...')
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 '
                                 'Firefox/67.0'}
        proxy_url = {'http': 'http://127.0.0.1:7890'}
        for i in tqdm(id_list):
            url = self.post_link.format(i)  # 图片页面的链接
            page = requests.get(url, headers=headers, proxies=proxy_url)
            tree = html.fromstring(page.content)
            if tree.xpath('//*[@id="png"]/@href'):  # 从图片页面获得原图片文件元素xpath
                # 图片页面没有png格式, 更换xpath
                source = tree.xpath('//*[@id="png"]/@href')
            else:
                source = tree.xpath('//*[@id="highres"]/@href')
            file_name = source[0].split('/')[-1]  # 从原图片地址的最后一段中获得图片描述的部分
            name = urllib.parse.unquote(file_name)  # 将其中的url转码为对应字符作为下载的文件名
            name_modify = re.sub('[*:?/|<>"]', '_', name)
            data = requests.get(source[0], headers=headers, proxies=proxy_url)
            with open(os.path.join(download_folder, name_modify), "wb") as file:  # 保存文件
                file.write(data.content)
            time.sleep(2)
        print('Download Successful')
        return

    # check if download finished
    @staticmethod
    def check_complete(driver):
        case1 = driver.find_elements(By.XPATH, '//*[@id="tip2"]')
        if case1[0].text:
            return True
        else:
            return False
    
    # selenium
    def sln_download(self, id_list, max_wait_time=60, json_info=True, js=None):
        driver = self.sln_chrome()
        print('start downloading...')
        count = 0
        try:
            for _ in tqdm(id_list):
                count += 1
                wait_time = max_wait_time
                url = self.post_link.format(_)
                driver.get(url)
                wait = WebDriverWait(driver, 3)
                source = driver.page_source
                if json_info:
                    self.sln_getInfo(source, _)
                    if count == 50:
                        settings.write_data(self.data_folder, self.data_file)
                        count = 0
                if not js:
                    try:
                        img = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="png"]')))
                    except TE:
                        try:
                            img = wait.until(EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="highres"]')))
                        except NSEE:
                            continue
                    actions = ActionChains(driver)
                    actions.click(img)
                    actions.perform()
                    # time.sleep(1)
                    pyautogui.hotkey('ctrl', 's')
                    time.sleep(1)
                    pyautogui.typewrite(['enter'])
                while not Downloader().check_complete(driver):
                    time.sleep(1)
                    wait_time -= 1
                    if wait_time <= 0:
                        print(f"post {_} max time reached...")
                        break
                # give browser time to save to disk
                if _ == id_list[-1]:
                    time.sleep(5)
                # time.sleep(2 + retry * 5)
                # if len(id_list) == 1:
                #     time.sleep(100)
            print('traverse list complete')
            driver.close()
            settings.write_data(self.data_folder, self.data_file)
            return 'list complete'
        except:
            if json_info:
                settings.write_data(self.data_folder, self.data_file)
            print(f"Interrupted at {_}")
            driver.close()
            return False

    # retrieved: whether been to the image page, init is False, set to True when has been to the image page.
    # download_state: first set to True when fetching image page, set to False if not found in disk after check
    """ two conditions: 1. old json has info but no retrieved property -> go else branch (id, info)
                        2. new json has retrieved property but no info -> go if branch   (id, retrieve)
    """
    def sln_getInfo(self, source, pid):
        if not settings.Img_data[pid]["retrieved"]:
            id_data = {
                pid: {
                    "posts": [],
                    "pools": [],
                    "pool_posts": [],
                    "tags": None,
                    "date": list,
                    "download_state": bool,
                    "retrieved": True
                }
            }
            tree = html.fromstring(source)
            description = tree.xpath('//*[@id="post-view"]/div[1]/text()')[0].strip()
            self.illustrate = description
            if "delete" in description:
                id_data = {
                    pid: {
                        "deleted": True,
                        "description": re.sub(r'\n', '', description),
                        "download_state": False
                    }
                }
            else:
                imgInfo = tree.xpath('//*[@id="post-view"]/script/text()')
                raw_string = imgInfo[0].strip()
                json_string = raw_string.lstrip(
                    'Post.register_resp(').rstrip(');')
                raw_data = json.loads(json_string)
                filter_list = ["id", "tags", "created_at", "updated_at", "score", "md5", "width",
                               "height", "file_size", "file_ext", "file_url", "rating", "has_children", "parent_id"]
                id_data[pid]["posts"] = [
                    {i: x[i] for i in x if i in filter_list} for x in raw_data["posts"]]
                c_timestamp = raw_data["posts"][0]["created_at"]
                date_data = [datetime.fromtimestamp(c_timestamp).year, datetime.fromtimestamp(
                    c_timestamp).month, datetime.fromtimestamp(c_timestamp).day]
                id_data[pid]["date"] = date_data
                id_data[pid]["download_state"] = True
                id_data[pid]["tags"] = raw_data["tags"]
                if raw_data["pools"]:
                    id_data[pid]["pools"] = [{i: x[i] for i in x if i not in [
                        "user_id", "is_public"]} for x in raw_data["pools"]]
                else:
                    id_data[pid]["pools"] = []
                if raw_data["pool_posts"]:
                    for _ in range(len(raw_data["pool_posts"])):
                        id_data[pid]["pool_posts"].append(
                            {i: raw_data["pool_posts"][_][i] for i in raw_data["pool_posts"][_] if i != 'active'})
                else:
                    id_data[pid]["pool_posts"] = []
                if raw_data["posts"][0]["has_children"]:
                    children_Info = tree.xpath(
                        '//*[@id="post-view"]/div[3]/a/text()')
                    children_post_id = [int(x) for x in children_Info[1:]]
                    id_data[pid]["posts"][0]["children"] = children_post_id
            settings.Img_data.update(id_data)
        else:
            if settings.Img_data[pid].get("deleted"):
                print(f"post {pid} deleted, skip")
            else:
                settings.Img_data[pid]["download_state"] = True
                if not settings.Img_data[pid].get("retrieved"):
                    settings.Img_data[pid]["retrieved"] = True
            # downloaded, yet been deleted later, add deleted property
            if "delete" in self.illustrate:
                settings.Img_data[pid]["deleted"] = True
        # settings.write_data(data_folder, data_file)

    def sln_minitokyo(self, id_list):
        signal = 'confirm'
        circle_times = 0
        driver = self.sln_chrome()
        # no need to login if use user profile:
        # with open('./login', 'r') as r:
        #     userinfo = r.read().splitlines()
        # account = userinfo[0]
        # auth = userinfo[-1]
        # http_proxy = "127.0.0.1:7890"
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
        # driver = webdriver.Chrome()  # options=chrome_options)
        # url_login = 'http://my.minitokyo.net/login'
        # driver.get(url_login)
        # username = driver.find_element(By.XPATH, '//*[@id="username"]')
        # username.send_keys(account)
        # password = driver.find_element(By.XPATH, '//*[@id="content"]/form/li[2]/input')
        # password.send_keys(auth)
        # log_in = driver.find_element(By.XPATH, '//*[@id="content"]/form/li[3]/input')
        # log_in.click()
        # time.sleep(3)
        while signal == 'confirm':
            circle_times += 1
            list1 = os.listdir(self.dl_path)
            minitokyo_downloaded = []
            for name in list1:
                if name.endswith('jpg'):
                    minitokyo_image = name.split('.')[0]
                    minitokyo_downloaded.append(minitokyo_image)
            diff = list(set(id_list) - set(minitokyo_downloaded))
            if len(diff) == 0:
                signal = 'deny'
                print('Finally, all pictures have been downloaded')
            elif circle_times == 5:
                signal = 'deny'
                print('Almost downloaded with some exceptions')
                print(diff)
            else:
                print('start downloading...')
                for _ in tqdm(diff):
                    url = self.post_link.format(_)
                    driver.get(url)
                    location = driver.find_element(
                        By.XPATH, '//*[@id="image"]/p/a')
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(
                        location, 100, 100).perform()
                    actions.context_click().perform()
                    pyautogui.typewrite(['down', 'down', 'enter'])
                    time.sleep(0.8)
                    pyautogui.typewrite(['enter'])
                print('download successful')
                # time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    # testurl = ['https://yande.re/post/show/208854', 'https://yande.re/post/show/650982',
    #            'https://yande.re/post/show/650990', 'https://yande.re/post/show/938322', 'https://yande.re/post/show/938391']
    # testid = [x.split('/')[-1] for x in testurl]
    # testid2 = [856161, 783832, 721830, 608268, 608269, 605545]
    # Downloader().sln_download(testid2, json_info=False, js=True)
    # testdriver = Downloader().sln_chrome()
    # testdriver.get(testurl[-1])
    # Downloader().check_finish(testdriver)
    # for _ in tqdm(testurl):
    #     testdriver.get(_)
    #     wait = WebDriverWait(testdriver, 3)
    #     source = testdriver.page_source
    #     img_id = _.split('/')[-1]
    #     Downloader().sln_getInfo(source, img_id)
    # with open("test5Image.json", "w") as o:
    #     json.dump(settings.Imgdata, o, indent=4)
    # tree = html.fromstring(source)
    # imgInfo = tree.xpath('//*[@id="post-view"]/div[1]/text()')
    # imgInfo = [int(x) for x in imgInfo[1:]]
    # info = testdriver.find_element(By.XPATH, '//*[@id="post-view"]/script')
    # info1 = testdriver.find_element(By.XPATH,  '/html/body/div[8]/div[1]/div[4]')
    # Ink1 = info1.find_elements_by_tag_name('a')
    # Ink1li = [x.get_attribute('href') for x in Ink1]
    # info2 = testdriver.find_element(By.XPATH,  '/html/body/div[8]/div[1]/div[3]')
    # Ink2 = info2.find_elements_by_tag_name('a')
    # Ink2li = [x.get_attribute('href') for x in Ink2]
    # info3 = testdriver.find_element(By.XPATH, '//*[@id="highres"]')
    # info1txt = info1.text
    # info2txt = info2.text
    # print(info1.get_attribute('class'), '\n', info2.get_attribute('class'))
    # print(info3.get_attribute('href'))
    # print(re.sub(r'\n', '', imgInfo[0]))
    Downloader().sln_chrome()
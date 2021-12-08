from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NSe
from selenium.webdriver.common.by import By
import json
import time

def coser_lewd():
    http_proxy = "127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = 'https://cosindex.251.sh/#/Cosersets'
    driver.get(url)
    sgn = 0
    lewd_dict = {}
    for i in range(1, 130):
        if sgn == 3:
            with open('coser.json', 'w', encoding='utf-8') as f:
                json.dump(lewd_dict, f, ensure_ascii=False, indent=4)
            print('All cosers have been lewd ( ´ ▽ ` ).｡ｏ♡')
            break
        try:
            coser = driver.find_element(By.XPATH, '//*[@id="treeview"]/ul/li/ul/li[{}]/span/a'.format(i))
            print(coser.text)
            coser_name = coser.text
            coser_resource = []
            coser.click()
            lewd_info = driver.find_element(By.XPATH, '//*[@id="list_footer_info_label"]')
            print(lewd_info.text)
            file_number = int(lewd_info.text.split(" ")[4])
            for i in range(1, file_number+1):
                lewd_resource = driver.find_element(By.XPATH, '//*[@id="files"]/tbody/tr[{}]/td[1]/span/a'.format(i))
                link = lewd_resource.get_attribute("href")
                coser_resource.append(link)
                print(link)
                # time.sleep(0.3)
            coser_dict = {coser_name:coser_resource}
            lewd_dict.update(coser_dict)
            # time.sleep(0.1)
        except NSe:
            sgn += 1
            continue


if __name__ == '__main__':
    coser_lewd()

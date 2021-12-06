from selenium import webdriver
import time
import pyautogui

def pixiv_daily():
    http_proxy = "127.0.0.1:7890"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(http_proxy))
    chrome_options.add_argument("--user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument('--profile-directory=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
    # chrome_options.add_extension("C:\\Users\\Administrator\\Desktop\\dkndmhgdcmjdmkdonmbgjpijejdcilfh.crx")
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = 'https://www.pixiv.net/ranking.php?mode=daily&date=20211130'
    driver.get(url)
    dl_btn = driver.find_element_by_xpath('//*[@id="openCenterPanelBtn"]')
    dl_btn.click()
    crawl_debut = driver.find_element_by_xpath('/html/body/div[6]/div[4]/slot/form/div[1]/div/slot[1]/button[2]')
    crawl_debut.click()


def daily_gen():
    return



# if __name__ == '__main__':
#     pixiv_daily()
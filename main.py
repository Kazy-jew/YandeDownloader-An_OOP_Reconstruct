from mainyande import Yande_re, Konachan, Minitokyo


def run_main():
    site_crawler = None
    console_log = input("""
    select downloader(default: yande.re, enter q to quit):
    1.yande.re    2.konachan   3.minitokyo
    """)
    if console_log in ['2', 'k', 'konachan', 'konachan.com']:
        site_crawler = Konachan
    elif console_log in ['3', 'm', 'minitokyo']:
        site_crawler = Minitokyo
    elif console_log == 'q':
        exit()
    else:
        site_crawler = Yande_re
    site_crawler.run()


if __name__ == '__main__':
    run_main()

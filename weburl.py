from settings import config


class Site():

    def __init__(self, site='yande.re'):
        self.site = site
        self.date_link = config["yande"]["weburl"][0]
        self.post_link = config["yande"]["weburl"][1]
        self.tag = config["yande"]["tag"]
        self.prefix = config["yande"]["prefix"]

    def set_site(self, site):
        if site in ['yande.re', 'yande', 'y']:
            self.tag = config["yande"]["tag"]
            self.site = config["yande"]["site"]
            self.prefix = config["yande"]["prefix"]
            self.date_link = config["yande"]["weburl"][0]
            self.post_link = config["yande"]["weburl"][1]
        elif site in ['konachan', 'konachan.com', 'k']:
            self.tag = config["konachan"]["tag"]
            self.site = config["konachan"]["site"]
            self.prefix = config["konachan"]["prefix"]
            self.date_link = config["konachan"]["weburl"][0]
            self.post_link = config["konachan"]["weburl"][1]
        elif site in ['minitokyo', 'm']:
            self.tag = config["minitokyo"]["tag"]
            self.site = config["minitokyo"]["site"]
            self.date_link = ''
            self.prefix = config["minitokyo"]["prefix"]
            self.post_link = config["minitokyo"]["weburl"][0]
        else:
            raise Exception("No a Valid Site!")



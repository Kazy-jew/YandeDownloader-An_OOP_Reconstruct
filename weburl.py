class WebURL:
    konachan = ['https://konachan.com/post?page={}&tags=date%3A{}-{}',
                'https://konachan.com/post/show/{}']
    yande = ['https://yande.re/post?page={}&tags=date%3A{}-{}',
             'https://yande.re/post/show/{}']
    minitokyo = 'http://gallery.minitokyo.net/download/{}'


class SiteSpace(WebURL):

    def __init__(self, site='yande.re'):
        self.site = site
        self.site_link = self.yande[0]
        self.post_link = self.yande[1]

    def set_link(self, site):
        if site in ['yande.re', 'yande', 'y']:
            self.tag = 1
            self.site = 'yande.re'
            self.site_link = self.yande[0]
            self.post_link = self.yande[1]
        elif site in ['konachan', 'konachan.com', 'k']:
            self.tag = 2
            self.site = 'Konachan'
            self.site_link = self.konachan[0]
            self.post_link = self.konachan[1]
        elif site in ['minitokyo', 'm']:
            self.tag = 3
            self.site = 'minitokyo'
            self.site_link = ''
            self.post_link = self.minitokyo
        else:
            return



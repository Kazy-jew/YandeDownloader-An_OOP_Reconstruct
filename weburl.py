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
        self.tag = 'yande'
        self.prefix = 'yande.re'

    def set_site(self, site):
        if site in ['yande.re', 'yande', 'y']:
            self.tag = 'yande'
            self.site = 'yande.re'
            self.prefix = 'yande.re'
            self.site_link = self.yande[0]
            self.post_link = self.yande[1]
        elif site in ['konachan', 'konachan.com', 'k']:
            self.tag = 'konachan'
            self.site = 'Konachan'
            self.prefix = 'Konachan.com'
            self.site_link = self.konachan[0]
            self.post_link = self.konachan[1]
        elif site in ['minitokyo', 'm']:
            self.tag = 'minitokyo'
            self.site = 'minitokyo'
            self.site_link = ''
            self.prefix = ''
            self.post_link = self.minitokyo
        else:
            return



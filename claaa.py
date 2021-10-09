class C:
    def __init__(self):
        self.year = 2021


class D(C):

    def __init__(self, site='yande.re'):
        super(D, self).__init__()
        self.site = site
        self.site_link = None
        self.post_link = None
        if site in ['yande.re', 'yande', 'y']:
            self.site_link = 1
            self.post_link = 1.1
        elif site in ['konachan', 'konachan.com', 'k']:
            self.site_link = 2
            self.post_link = 2.2
        elif site in ('minitokyo' or 'm'):
            self.post_link = 3
            self.site_link = None

    def start(self):
        print('self.post_link: {} is used here'.format(self.post_link))

I = D()
# c, d = C(), D()
# print(type(I), I.__class__, type(C), C.__class__)
# type(c) == type(d)
# import _pickle as cpk
#
# with open(r'userinfo', 'rb') as inp:
#     e = cpk.load(inp)
#
# print(e)


import json
from pprint import pprint

class C:
    def __init__(self):
        self.year = 2021


class D(C):

    def __init__(self, site='yande.re'):
        super(D, self).__init__()
        self.site = site
        self.date_link = None
        self.post_link = None
        if site in ['yande.re', 'yande', 'y']:
            self.date_link = 1
            self.post_link = 1.1
        elif site in ['konachan', 'konachan.com', 'k']:
            self.date_link = 2
            self.post_link = 2.2
        elif site in ('minitokyo' or 'm'):
            self.post_link = 3
            self.date_link = None

    def start(self):
        print('self.post_link: {} is used here'.format(self.post_link))

I = D()
pprint(dir(D()))
# c, d = C(), D()
# print(type(I), I.__class__, type(C), C.__class__)
# type(c) == type(d)
# import _pickle as cpk
#
# with open(r'userinfo', 'rb') as inp:
#     e = cpk.load(inp)
#
# print(e)
# blackjack_hand = (8, "Q")
# with open('test_data.json', 'w') as jw:
#     json.dump(blackjack_hand, jw)
# with open('configyan.json', 'r') as jr:
#     jrstr = json.load(jr)

# id_list decouple
# id_list = [j['imgId']  for i in jrstr['dates']  for j in i['id-info']]
# print(id_list)

# date_list decouple
# dates_list = [jrstr['year']+'-'+x['date'] for x in jrstr['dates']]
# print(dates_list)
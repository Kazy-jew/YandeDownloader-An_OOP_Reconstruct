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

# I = D()
# pprint(dir(D()))
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

# raw_list = [' Post.register_resp({"posts":[{"id":650982,"tags":"asian_clothes ass breast_hold dress erect_nipples nopan see_through skirt_lift tony_taka","created_at":1592661641,"updated_at":1641057144,"creator_id":220654,"approver_id":null,"author":"kiyoe","change":4674935,"source":"","score":74,"md5":"c7fc5909f20598bf98ea578aa278da1c","file_size":7367542,"file_ext":"png","file_url":"https://files.yande.re/image/c7fc5909f20598bf98ea578aa278da1c/yande.re%20650982%20asian_clothes%20ass%20breast_hold%20dress%20erect_nipples%20nopan%20see_through%20skirt_lift%20tony_taka.png","is_shown_in_index":true,"preview_url":"https://assets.yande.re/data/preview/c7/fc/c7fc5909f20598bf98ea578aa278da1c.jpg","preview_width":105,"preview_height":150,"actual_preview_width":210,"actual_preview_height":300,"sample_url":"https://files.yande.re/sample/c7fc5909f20598bf98ea578aa278da1c/yande.re%20650982%20sample%20asian_clothes%20ass%20breast_hold%20dress%20erect_nipples%20nopan%20see_through%20skirt_lift%20tony_taka.jpg","sample_width":1049,"sample_height":1500,"sample_file_size":196387,"jpeg_url":"https://files.yande.re/jpeg/c7fc5909f20598bf98ea578aa278da1c/yande.re%20650982%20asian_clothes%20ass%20breast_hold%20dress%20erect_nipples%20nopan%20see_through%20skirt_lift%20tony_taka.jpg","jpeg_width":2802,"jpeg_height":4005,"jpeg_file_size":989063,"rating":"q","is_rating_locked":false,"has_children":true,"parent_id":null,"status":"active","is_pending":false,"width":2802,"height":4005,"is_held":false,"frames_pending_string":"","frames_pending":[],"frames_string":"","frames":[],"is_note_locked":false,"last_noted_at":0,"last_commented_at":0}],"pool_posts":[{"id":316108,"pool_id":97266,"post_id":650982,"active":true,"sequence":"3","next_post_id":650990,"prev_post_id":650980}],"pools":[{"id":97266,"name":"[T2_ART_WORKS_(Tony)]_Tony_MAGAZINE_C98_Air_Comike_SP_(Various)","created_at":"2020-06-20T14:11:01.151Z","updated_at":"2020-06-20T14:16:48.370Z","user_id":220654,"is_public":false,"post_count":22,"description":""}],"tags":{"asian_clothes":"general","ass":"general","breast_hold":"general","dress":"general","erect_nipples":"general","nopan":"general","see_through":"general","skirt_lift":"general","tony_taka":"artist"},"votes":{}}); ']
# raw_string = raw_list[0].strip()
# rm_head = raw_string.replace('Post.register_resp(', '')
# rm_tail = rm_head[:-2]
# data = json.loads(rm_tail)
# print(type(data["posts"][0]["id"]))


dict1 = {
    1: [
        {"a": 1, "b": 2, "c": 3},
        {"a1": 1, "b1": 2, "c1": 3}
    ],
    2: [
        {"a": 1, "b": 2, "c": 3},
        {"a1": 1, "b1": 2, "c1": 3}
    ]
}
dict2 = {
    1: [],
    2: []
}

dict3 = {}
# for _ in range(len(dict1[1])):
#     print(dict1[1][_])
#     new_dict1 = dict1[1][_]
#     new1_dict1 = {i: new_dict1[i] for i in new_dict1 if i not in ['c', 'c1']}
#     dict2[1].append(new1_dict1)
#     print(dict2)
print(dict2.get("new"))
numbers = [4, 5, 7, 1, 3, 6, 9, 8, 0]
output = numbers.sort()
print("The Value in the output variable is:", output)

str = 'Post.register_tags({"ass":"general","gothic_lolita":"general","kakao_rantan":"artist","lolita_fashion":"general"});'
print(str.lstrip('Post.register_tags(').rstrip(');'))

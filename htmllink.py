from lxml import html
import requests
import bs4
import re
name_path = '//*[@id="treeview"]/ul/li/ul/li[104]/span/a'

# with open("F:\\coser.html", "r", encoding='utf-8') as f:
#     text = f.read()
# tree = html.fromstring(text)
# raw_content = text.split('		Array.prototype.p = Array.prototype.push;\n')[-1]
# raw_str = raw_content.split('delete(Array.prototype.p)')[0]
#
# content_list = raw_str.splitlines()[2:]
# with open("F:\\raw-list.txt", "w", encoding='utf-8') as f:
#     for _ in content_list:
#         f.write('{}\n'.format(_))
with open("F:\\raw-list.txt", 'r', encoding='utf-8') as r:
    raw_list = r.read().splitlines()
coser_name = []
pattern = re.compile('/.*?\*')
for i in raw_list:
    coser_name.append(i.split(',')[0])
coser_name = coser_name[:-4]
print(len(coser_name))
# coser = [pattern.split(x)[1] for x in coser_name]
# print(coser)
result = pattern.search(coser_name[0])
print(result)


import json
from pathlib import Path

with open("config.json", "r") as r:
    config = json.load(r)

Img_data = {}


def write_config():
    with open("config.json", "w", encoding='utf8') as o:
        json.dump(config, o, indent=4)


def write_data(folder, file):
    if not Path(f'./ImageData/{folder}').exists():
        Path(f'./ImageData/{folder}').mkdir(parents=True, exist_ok=True)
    with open(f"./ImageData/{folder}/{file}.json", "w", encoding='utf-8') as o:
        json.dump(Img_data, o, indent=4, ensure_ascii=False)


def read_data(folder, file):
    global Img_data
    if not Path(f'./ImageData/{folder}/{file}.json').exists():
        return {}
    else:
        with open(f'./ImageData/{folder}/{file}.json', encoding='utf-8') as ir:
            Img_data = json.load(ir)
        print("load imageData... done")
        return Img_data


# with open('./ImageData/yandeData/yande.re202203-02_03-02.json', 'r') as rj:
#     Img_data = json.load(rj)
#
# print(len(Img_data))
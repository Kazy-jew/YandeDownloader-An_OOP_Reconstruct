import json
from pathlib import Path

with open("config.json", "r", encoding='utf-8') as r:
    config = json.load(r)

Img_data = {}


def write_config():
    with open("config.json", "w", encoding='utf-8') as o:
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
        with open(f'./ImageData/{folder}/{file}.json', 'r', encoding='utf-8') as ir:
            Img_data = json.load(ir)
        print("load imageData... done")
        return Img_data


def clean_data():
    global Img_data
    with open(f"./ImageData/yandeData/yande.re2022.03-02_03-02.json", 'r', encoding='utf-8') as raw:
        Img_data = json.load(raw)
        for _ in Img_data:
            Img_data[_]["retrieved"] = True
    with open(f"./ImageData/yandeData/yande.re2022.03-02_03-02.json", 'w', encoding='utf-8') as m:
        json.dump(Img_data, m, indent=4, ensure_ascii=False)


def debug_data():
    global Img_data
    with open(f"./ImageData/konachanData/Konachan.com2022.03-19_03-25.json", 'r', encoding='utf-8') as raw:
        Img_data = json.load(raw)
    print(len(Img_data))
    has_info = [x for x in Img_data if len(Img_data[x]) > 2]
    for x in Img_data:
        Img_data[x]["download_state"] = True
    print(len(has_info))
    with open(f"./ImageData/konachanData/Konachan.com2022.03-19_03-25.json", 'w', encoding='utf-8') as raw:
        json.dump(Img_data, raw, indent=4, ensure_ascii=False)


# with open('./ImageData/yandeData/yande.re202203-02_03-02.json', 'r') as rj:
#     Img_data = json.load(rj)
#
# print(len(Img_data))


if __name__ == "__main__":
    debug_data()

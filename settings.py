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
        print(f"./ImageData{folder}/{file}.json")
        return {}
    else:
        with open(f'./ImageData/{folder}/{file}.json', 'r', encoding='utf-8') as ir:
            Img_data = json.load(ir)
            # print(len(Img_data))
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
    with open('./ImageData/yandeData/yande.re2022.03-11_03-15.json', 'r', encoding='utf-8') as rj:
        Img_data = json.load(rj)
    with open('./current_dl/yande.re.2022-03-11_2022-03-15.txt', 'r') as rk:
        list1 = rk.read().splitlines()
    Img_data = {x: {"retrieved": False, "download_state": False} for x in list1}
    with open('./ImageData/yandeData/yande.re2022.03-11_03-15.json', 'w', encoding='utf-8') as wj:
        json.dump(Img_data, wj, indent=4, ensure_ascii=False)
    print(len(Img_data))
    # with open(f"./ImageData/konachanData/Konachan.com2022.03-18_03-18.json", 'r', encoding='utf-8') as raw:
    #     Img_data = json.load(raw)
    # with open(f"./ImageData/konachanData/Konachan.com2022.03-19_03-25.json", 'r', encoding='utf-8') as raw:
    #     Img_data2 = json.load(raw)
    # # print(len(Img_data))
    # list1 = [*Img_data]
    # list2 = [*Img_data2]
    # print(list1 == list2)
    # has_info = [x for x in Img_data if len(Img_data[x]) > 2]
    # for x in Img_data:
    #     Img_data[x]["download_state"] = True
    # print(len(has_info))
    # with open(f"./ImageData/konachanData/Konachan.com2022.03-19_03-25.json", 'w', encoding='utf-8') as raw:
    #     json.dump(Img_data, raw, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    debug_data()

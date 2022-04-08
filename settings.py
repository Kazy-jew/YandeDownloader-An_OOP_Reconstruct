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


def read_data(folder, file, dumb=False):
    global Img_data
    if not Path(f'./ImageData/{folder}/{file}.json').exists():
        print(f"./ImageData{folder}/{file}.json")
        return {}
    else:
        with open(f'./ImageData/{folder}/{file}.json', 'r', encoding='utf-8') as ir:
            Img_data = json.load(ir)
            # print(len(Img_data))
        if not dumb:
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
    p = Path('./ImageData/yandeData')
    file_list = [x for x in p.iterdir() if x.is_file()]
    for q in file_list:
        with q.open(encoding='utf-8') as qr:
            Img_data = json.load(qr)
        keys = [*Img_data]
        has_empty = [x for x in keys if len(Img_data[x]) == 2]
        if has_empty:
            print(q)


if __name__ == "__main__":
    debug_data()
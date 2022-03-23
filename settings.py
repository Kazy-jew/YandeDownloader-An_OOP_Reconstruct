import json
from pathlib import Path

with open("config.json", "r") as r:
    config = json.load(r)

Imgdat = {}


def write_config():
    with open("config.json", "w") as o:
        json.dump(config, o, indent=4)


def write_data(folder, file):
    if not Path(f'./ImageData/{folder}').exists():
        Path(f'./ImageData/{folder}').mkdir(parents=True, exist_ok=True)
    with open(f"{file}.json", "w") as o:
        json.dump(Imgdat, o, indent=4)

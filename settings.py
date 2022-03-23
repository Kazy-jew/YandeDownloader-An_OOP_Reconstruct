import json


with open("config.json", "r") as r:
    config = json.load(r)
dat = {}


def write_config():
    with open("config.json", "w") as o:
        json.dump(config, o, indent=4)


def write_data(name):
    with open(f"{name}.json", "w") as o:
        json.dump(dat, o, indent=4)

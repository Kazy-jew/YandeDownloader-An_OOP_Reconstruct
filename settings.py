import json


with open("config.json", "r") as r:
    config = json.load(r)


def write_config():
    with open("config.json", "w") as o:
        json.dump(config, o, indent=4)

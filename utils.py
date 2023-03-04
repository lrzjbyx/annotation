import json


def loadLabelJson(filename):
    with open(filename,"r",encoding="utf-8") as f:
        content = f.read()
    return json.loads(content)
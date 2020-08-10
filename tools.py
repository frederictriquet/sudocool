import json

def loadJson(filename: str):
    with open(filename) as jsonFile:
        stringData = jsonFile.read()
        return json.loads(stringData)
    return None

import json

def loadJson(filename: str):
    try:
        with open(filename) as jsonFile:
            stringData = jsonFile.read()
            return json.loads(stringData)
    except FileNotFoundError:
        print(f'File not found: {filename}')
        return None

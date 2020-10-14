import json
import urllib.request

def loadJson(filename: str):
    try:
        with open(filename) as jsonFile:
            stringData = jsonFile.read()
            return json.loads(stringData)
    except FileNotFoundError: # LGTM ?
        print(f'File not found: {filename}')
        return None

def loadJsonFromUrl(url: str):
    response = urllib.request.urlopen(url)
    # mybytes = response.read()
    # mystr = mybytes.decode("utf8")
    # print(mystr)
    data = json.loads(response.read())
    response.close()
    return data

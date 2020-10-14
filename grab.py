#! /usr/bin/env python3
import json
import tools
import sys

def main():
    id = sys.argv[1]
    url = 'https://firebasestorage.googleapis.com/v0/b/sudoku-sandbox.appspot.com/o/' + id
    j = tools.loadJsonFromUrl(url)
    # print(j)
    token = j['downloadTokens']
    url = url + '?alt=media&token=' + token
    j = tools.loadJsonFromUrl(url)
    # print(j)
    # print(j['cells'])
    data = []
    for row in j['cells']:
        lineData = ''
        for cell in row:
            if 'value' in cell:
                lineData += cell['value']
            else:
                lineData += '.'
        data.append(lineData)
    print(json.dumps(data, indent=2))
if __name__ == "__main__":
    # execute only if run as a script
    main()
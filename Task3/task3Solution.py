# ToDo refactoring, add aditional features and tests

import pandas as pd
import json

url = 'https://d2hmvvndovjpc2.cloudfront.net/efe'

def ExcelToJSON(file_path):

    data = pd.read_excel(file_path)

    json_data = data.where(pd.notnull(data), "").to_dict(orient='records')

    with open('original_data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4, default=str)

    return json_data

def SortJSON(json_data):
    sorted_json = sorted(json_data, key=lambda x: x['levelColor'], reverse=False)

    with open('sorted_data.json', 'w') as json_file:
        json.dump(sorted_json, json_file, indent=4, default=str)

    return sorted_json

def addField(sorted_json, url):
    for book in sorted_json:
        full_url = f"{url.rstrip('/')}/{book.get('filepath').lstrip('/')}/{book.get('filename')}"
        book.update({'url': full_url})

    
    with open('sorted_data_with_URL.json', 'w') as json_file:
        json.dump(sorted_json, json_file, indent=4, default=str)

    return sorted_json

if __name__ == "__main__":
    addField(SortJSON(ExcelToJSON('data.xlsx')),url)


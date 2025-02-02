import pandas as pd
import json

URL = 'https://d2hmvvndovjpc2.cloudfront.net/efe'
SORT_CATEGORY = 'levelColor'
DATA_FILE = 'data.xlsx'
OUTPUT_FILE = 'final_result.json'

def ExcelToJSON(file_path):
    try:
        data = pd.read_excel(file_path)
        json_data = data.where(pd.notnull(data), "").to_dict(orient='records')
        return json_data
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return []

def json_writer(json_data, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, default=str)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")

def SortJSON(json_data, sort_category):
    try:
        sorted_json = sorted(json_data, key=lambda x: x[sort_category], reverse=False)
        return sorted_json
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return []

def addField(sorted_json, url):
    try:
        for book in sorted_json:
            full_url = f"{url.rstrip('/')}/{book.get('filepath').lstrip('/')}/{book.get('filename')}"
            book.update({'url': full_url})
        return sorted_json
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return []

if __name__ == "__main__":
    json_data = ExcelToJSON(DATA_FILE)
    sorted_json = SortJSON(json_data, SORT_CATEGORY)
    sorted_json_with_url = addField(sorted_json, URL)
    json_writer(sorted_json_with_url, OUTPUT_FILE)


import csv
import json

def convert_csv_to_json(csv_file, json_file):
    csv_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append(row)
    with open(json_file, 'w') as file:
        json.dump(csv_data, file)

csv_file_path = 'C:/users/data/results.csv'
json_file_path = 'C:/users/data/results.json'

convert_csv_to_json(csv_file_path, json_file_path)
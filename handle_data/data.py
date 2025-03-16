import json
from pathlib import Path

project_root = Path(__file__).parent.parent
client_data_path = project_root / "data/clients.json"

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def get_data():
    return read_json_file(client_data_path)
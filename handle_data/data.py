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

def search_client(*args):
    full_name, phone, email = args
    data = get_data()
    for client in data.get("clients", []):
        if phone and client.get("phone") == phone:
            return client
        if not phone and full_name and email:
            if client.get("fullName") == full_name and client.get("email") == email:
                return client
    return None
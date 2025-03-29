import json
from pathlib import Path
import hashlib

project_root = Path(__file__).parent.parent
client_data_path = project_root / "data/clients.json"

def hash_string(input_string, algorithm='sha256', encoding='utf-8'):

    hash_object = hashlib.new(algorithm)
    hash_object.update(input_string.encode(encoding))
    return hash_object.hexdigest()

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_data():
    return read_json_file(client_data_path)

def search_client(*args):
    # Existing search implementation
    full_name, phone, email = args
    data = get_data()
    for client in data.get(phone, []):
        if phone and client.get("phone") == phone:
            return client
        if not phone and full_name and email:
            if client.get("fullName") == full_name and client.get("email") == email:
                return client
    return None

def add_client(full_name, phone, email, inquiry_type, 
              property_of_interest, payment_method, urgency, comments, language):
    data = get_data()
    
    payment_key = payment_method.split()[0] if payment_method else None
    
    new_client = {
        "fullName": full_name.strip(),
        "phone": phone,
        "email": email.strip(),
        "inquiryType": inquiry_type,
        "propertyOfInterest": property_of_interest.strip() or None,
        "paymentMethod": payment_key,
        "urgency": urgency.strip() or None,
        "comments": comments,
        "language": language  # Added language field
    }

    if phone not in data:
        data[phone] = []
    data[phone].append(new_client)
    
    write_json_file(client_data_path, data)


import json
from pathlib import Path

project_root = Path(__file__).parent.parent
client_data_path = project_root / "data/clients.json"

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
    for client in data.get("clients", []):
        if phone and client.get("phone") == phone:
            return client
        if not phone and full_name and email:
            if client.get("fullName") == full_name and client.get("email") == email:
                return client
    return None

def add_client(full_name, phone, email, inquiry_type, 
              property_of_interest, payment_method, urgency, comments):
    # Get existing data
    data = get_data()
    
    # Process payment method to extract key (e.g., "Cash" from "Cash (Rent/Buy)")
    payment_key = payment_method.split()[0] if payment_method else None
    
    # Create new client object matching JSON structure
    new_client = {
        "fullName": full_name.strip(),
        "phone": phone,
        "email": email.strip(),
        "inquiryType": inquiry_type,
        "propertyOfInterest": property_of_interest.strip() or None,
        "paymentMethod": payment_key,
        "urgency": urgency.strip() or None,
        "comments": comments
    }
    
    # Add to clients array
    data["clients"].append(new_client)
    
    # Write updated data back to file
    write_json_file(client_data_path, data)
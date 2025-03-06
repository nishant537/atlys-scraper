import json
import os
from dotenv import load_dotenv
from html_response_codes import *

load_dotenv()
DATA_FILE = os.getenv('DATA_FILE')

class JSONDatabase:
    def __init__(self, path=DATA_FILE):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    def update_products(self, new_products):
        existing_data = ''
        # loading existing data
        with open(self.path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        existing_dict = {p["product_title"]: p for p in existing_data}

        updated_count = 0
        for product in new_products:
            title = product["product_title"]
            if title not in existing_dict or existing_dict[title]["product_price"] != product["product_price"]:
                existing_dict[title] = product
                updated_count += 1

        # updating in json file
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(list(existing_dict.values()), f, indent=4)
        return updated_count
    
    # health_check api for checking if database service is up and running, for now checking health checking database file, can do with external database service.
    def health_check(self):
        if not os.path.exists(DATA_FILE):
            return ErrorResponseModel(404, "File not found")
        
        try:
            with open(DATA_FILE, "r") as file:
                json.load(file)
        except Exception as e:
            return ErrorResponseModel(500, f"File is corrupted - {e}")
        
        return {"status": "ok", "message": "File is valid"}

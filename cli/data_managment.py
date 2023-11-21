import os
import json
from data import personnel, stock

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")


def create_directoriy(directory):
    new_dir = os.path.join(ROOT, directory)

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    else:
        print(f"The directory {new_dir} already exists.")


def write_json_file(directory, filename, data):
    file_path = os.path.join(directory, filename)

    if os.path.exists(file_path):
        print(f"The file {filename} already exists in {directory}")
    else:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=1)


create_directoriy("data")

json_file_personnel = "personnel.json"
json_file_stock = "stock.json"

write_json_file(DATA_DIR, json_file_personnel, personnel)
write_json_file(DATA_DIR, json_file_stock, stock)

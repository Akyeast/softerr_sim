import json

def get_file_data(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data.strip()

def get_config(filename):
    with open(filename, 'r') as f:
        cfg = json.load(f)
    return cfg
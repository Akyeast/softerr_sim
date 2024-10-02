import json

def get_file_data(filename):
    with open(filename, 'r') as f:
        data = f.read()
    return data.strip()

def get_file_avg(filename):
    with open(filename, 'r') as f:
        data = f.readlines()
    data = [x.strip().split(',') for x in data]
    
    method_avg = []
    for line in zip(*data):
        line = list(float(d) for d in line)
        method_avg.append(sum(line) / len(line))
    return method_avg


def get_config(filename):
    with open(filename, 'r') as f:
        cfg = json.load(f)
    return cfg
import json

def build_string(params):
    return '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])

class Logger():
    def __init__(self, params, filepath=''):
        with open('cfg/logger_cfg.json', 'r') as f:
            self.cfg = json.load(f)

        if filepath == '':
            filepath = self.cfg['output_path']

        self.filepath = '{}/{}.txt'.format(filepath, build_string(params))
    
    def write(self, content):
        with open(self.filepath, 'a') as f:
            f.write(content+'\n')
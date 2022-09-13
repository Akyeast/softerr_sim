import json

def build_string(params):
    return '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])

class Logger():
    def __init__(self, params, level='low', filepath='', log_params=[]):
        assert level in ['low', 'high']
        self.level = level

        with open('cfg/logger_cfg.json', 'r') as f:
            self.cfg = json.load(f)

        if filepath == '':
            filepath = self.cfg['output_path']

        if len(log_params) == 0: 
            self.filepath = '{}/{}.txt'.format(filepath, build_string(params))
        else :
            new_params = {k: v for k, v in params.items() if k in log_params}
            self.filepath = '{}/{}.txt'.format(filepath, build_string(new_params))
    
    def write(self, content):
        with open(self.filepath, 'a') as f:
            f.write(content+'\n')
    
    def print(self, content):
        if self.level == 'low':
            print(content)
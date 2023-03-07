import json
from generator.generator import generate_tasksets
from core.wo_drop import get_num_core_ours_wo_drop
from core.all_lockstep import get_num_core_LS
from core.ours import get_num_core_ours
from logger.logger import Logger

def exp(cfg, logger):
    tasks = generate_tasksets(cfg)
    print(cfg)
    
    for task_set in tasks:
        stateless_ts = task_set.get_tasks(sort=True, desc=True)

        core, prms, mapped_tasks = get_num_core_ours(stateless_ts)
        utilization_sum = [t[1]/t[0] if t is not None else 0.0  for t in prms]
        for task in mapped_tasks:
            if task[2] == 1:
                utilization_sum[task[3]] += task[1]/task[0]
        utilization_avg = sum(utilization_sum)/len(utilization_sum)
        logger.write('{}'.format(utilization_avg))
    print('\n')

def main():
    with open('cfg/utilization_cfg.json', 'r') as f:
        cfg = json.load(f)

    for num_states in cfg['num_states_list']:
        for criticality_prob in cfg['critical_prob_list'] :
            new_cfg = cfg.copy()
            new_cfg['num_states'] = num_states
            new_cfg['critical_prob'] = criticality_prob
            logger = Logger(new_cfg, filepath="output/utilization", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
            exp(new_cfg, logger)

if __name__ == '__main__':
    main()
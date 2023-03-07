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

        num_core_LS = get_num_core_LS(stateless_ts, method='rta_single')
        num_core_wo_drop, _, _ = get_num_core_ours_wo_drop(stateless_ts, method='rta_single')
        num_core_ours, _, _ = get_num_core_ours(stateless_ts)

        logger.write('{},{},{}'.format(num_core_LS, num_core_wo_drop, num_core_ours))
        print(f'ls: {num_core_LS:2}, wo_drop: {num_core_wo_drop:2}, ours: {num_core_ours:2}')
    print('\n')

def main():
    with open('cfg/rerun_exp_cfg.json', 'r') as f:
        cfg = json.load(f)

    for num_states in cfg['num_states_list']:
        for criticality_prob in cfg['critical_prob_list'] :
            new_cfg = cfg.copy()
            new_cfg['num_states'] = num_states
            new_cfg['critical_prob'] = criticality_prob
            logger = Logger(new_cfg, filepath="output/rerun", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
            exp(new_cfg, logger)

if __name__ == '__main__':
    main()
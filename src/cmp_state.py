import json
from generator.generator import generate_tasksets
from core.ours import get_num_core_ours
from logger.logger import Logger

def exp(cfg, logger):
    tasks = generate_tasksets(cfg)

    for task_set in tasks:
        stateless_ts = task_set.get_tasks(sort=True, desc=True)
        
        num_core_stateless = get_num_core_ours(stateless_ts)
        num_core_statewise = 0

        for state in range(cfg['num_states']):
            state_ts = task_set.get_tasks(sort=True, desc=True, state_num=state)
            num_core = get_num_core_ours(state_ts)

            if num_core_statewise < num_core:
                num_core_statewise = num_core

        logger.write('{},{}\n'.format(num_core_stateless, num_core_statewise))
        print(num_core_stateless, num_core_statewise)


def main():
    with open('cfg/state_exp_cfg.json', 'r') as f:
        cfg = json.load(f)

    for num_states in cfg['num_states_list']:
        for criticality_prob in cfg['critical_prob_list'] :
            new_cfg = cfg.copy()
            new_cfg['num_states'] = num_states
            new_cfg['critical_prob'] = criticality_prob

            logger = Logger(cfg, log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
            exp(new_cfg, logger)
    
if __name__ == '__main__':
    main()
import json
from generator.generator import generate_tasksets
from core.all_lockstep import get_num_core_LS
from core.ours import get_num_core_ours
from logger.logger import Logger

def exp(cfg, logger):
    tasks = generate_tasksets(cfg)
    print(cfg)

    for task_set in tasks:
        stateless_ts = task_set.get_tasks(sort=True, desc=True)

        num_core_LS = get_num_core_LS(stateless_ts, method='rta_single')
        num_core_ours = get_num_core_ours(stateless_ts)

        logger.write('{},{}'.format(num_core_LS, num_core_ours))
        print(r'ls: {}, ours: {}'.format(num_core_LS, num_core_ours))
    print("\n")

def cmp_LSs():
    tasks = generate_tasksets()

    for task_set in tasks:
        stateless_ts = task_set.get_tasks(sort=True, desc=True)
        print(stateless_ts)

        deadline = get_num_core_LS(stateless_ts, method='deadline')
        rta = get_num_core_LS(stateless_ts, method='rta')
        print(deadline, rta)

def main():
    with open('cfg/ls_exp_cfg.json', 'r') as f:
        cfg = json.load(f)

    for num_states in cfg['num_states_list']:
        for criticality_prob in cfg['critical_prob_list'] :
            new_cfg = cfg.copy()
            new_cfg['num_states'] = num_states
            new_cfg['critical_prob'] = criticality_prob
            logger = Logger(new_cfg, filepath="output/ls", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
            exp(new_cfg, logger)

if __name__ == '__main__':
    main()
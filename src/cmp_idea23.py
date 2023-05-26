import json
from generator.generator import generate_tasksets
from core.baseline import get_num_core_baseline
from core.wo_drop import get_num_core_ours_wo_drop
from core.all_lockstep import get_num_core_LS
from core.ours import get_num_core_ours
from logger.logger import Logger

def run_exp(cfg):
    tasks = generate_tasksets(cfg)

    for state in cfg['num_states_list']:
        print({**cfg, 'num_states': state})
        logger = Logger({**cfg, 'num_states': state}, filepath="output/idea23", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
        exp(tasks, state, logger)


def exp(tasks, state, logger):
    for task_set in tasks:
        task_set.assign_new_criticality(state)
        
        num_core_LS, num_core_wo_drop, num_core_ours = 0, 0, 0

        for s in range(state):
            state_ts = task_set.get_tasks(sort=True, desc=True, state_num=s)

            new_num_core_LS, _, _ = get_num_core_baseline(state_ts, method='rta_single')
            new_num_core_wo_drop, _, _ = get_num_core_ours_wo_drop(state_ts, method='rta_single')
            new_num_core_ours, _, _ = get_num_core_ours(state_ts)

            num_core_LS = max(num_core_LS, new_num_core_LS)
            num_core_wo_drop = max(num_core_wo_drop, new_num_core_wo_drop)
            num_core_ours = max(num_core_ours, new_num_core_ours)

            # if num_core_statewise < num_core:
            #     logger.print(f"statewise taskset: {state_ts}")
            #     logger.print(f"statewise numcore: {num_core}")
            #     num_core_statewise = num_core

        logger.write('{},{},{}'.format(num_core_LS, num_core_wo_drop, num_core_ours))
        print(f'ls: {num_core_LS:2}, wo_drop: {num_core_wo_drop:2}, ours: {num_core_ours:2}')



def main():
    with open('cfg/idea23_exp_cfg.json', 'r') as f:
        cfg = json.load(f)

    for criticality_prob in cfg['critical_prob_list'] :
        new_cfg = cfg.copy()
        new_cfg['num_states_list'] = cfg['num_states_list']
        new_cfg['critical_prob'] = criticality_prob
        
        run_exp(new_cfg)
    
if __name__ == '__main__':
    main()
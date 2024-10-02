import json
from generator.generator import generate_tasksets
from core.ours import get_num_core_ours
from logger.logger import Logger

def run_exp(cfg):
    tasks = generate_tasksets(cfg)

    for state in cfg['num_states_list']:
        # cfg['num_states'] = state
        print({**cfg, 'num_states': state})
        logger = Logger({**cfg, 'num_states': state}, filepath="output/state", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
        exp(tasks, state, logger)


def exp(tasks, state, logger):
    for task_set in tasks:
        # task_set = task_set.assign_new_criticality(state)
        task_set.assign_new_criticality(state)

        stateless_ts = task_set.get_tasks(sort=True, desc=True)
        # logger.print(f"stateless taskset: {stateless_ts}")
        # print(f"stateless taskset: {stateless_ts}")
        num_core_stateless, _, _ = get_num_core_ours(stateless_ts)
        
        num_core_statewise = 0
        for s in range(state):
            state_ts = task_set.get_tasks(sort=True, desc=True, state_num=s)

            num_core, _, _ = get_num_core_ours(state_ts)
            # print(f"statewise taskset: {state_ts}")

            if num_core_statewise < num_core:
                logger.print(f"statewise taskset: {state_ts}")
                logger.print(f"statewise numcore: {num_core}")
                num_core_statewise = num_core

        # if num_core_stateless < num_core_statewise:
        #     print(f"taskset: {task_set}")
        #     print(f"stateless taskset: {stateless_ts}")

        logger.write('{},{}'.format(num_core_stateless, num_core_statewise))
        print(f'stateless: {num_core_stateless:2}, statewise: {num_core_statewise:2}')



def main():
    with open('cfg/state_exp_cfg.json', 'r') as f:
        cfg = json.load(f)

    for criticality_prob in cfg['critical_prob_list'] :
        new_cfg = cfg.copy()
        new_cfg['num_states_list'] = cfg['num_states_list']
        new_cfg['critical_prob'] = criticality_prob
        # logger = Logger(new_cfg, 
        #     level='high',
        #     filepath="output/state", 
        #     log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'period'])
        run_exp(new_cfg)
    
if __name__ == '__main__':
    main()
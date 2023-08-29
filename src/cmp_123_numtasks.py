import json
from generator.generator import generate_tasksets
from core.only_lockstep import get_num_core_only_lockstep, get_num_task_schedulable_only_lockstep
from core.dynamic_switching import get_num_core_dynamic_switching, get_num_task_schedulable_dynamic_switching
from core.ours import get_num_core_ours, get_num_task_schedulable_ours
from logger.logger import Logger

def run_exp(cfg):
    tasks = generate_tasksets(cfg)

    for state in cfg['num_states_list']:
        print({**cfg, 'num_states': state})
        logger = Logger({**cfg, 'num_states': state}, filepath="output/cmp123_crit_numtasks", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'delta'])
        exp(tasks, cfg, logger)


def exp(tasks, cfg, logger):
    for task_set in tasks:
        task_set.assign_new_criticality(cfg['num_states'])
        
        # num_core_ours = 0
        num_task_schedulable_only_lockstep = 0
        num_task_schedulable_dynamic_switching = 0
        num_task_schedulable_ours = 0

        for s in range(cfg['num_states']):
            state_ts = task_set.get_tasks(sort=True, desc=True, state_num=s)

            # new_num_core_ours, _, _ = get_num_core_ours_delta(state_ts, cfg['delta'])
            # new_num_core_ours, prms, mapped_task = get_num_core_ours_delta(state_ts, cfg['delta'])
            # num_core_ours = max(num_core_ours, new_num_core_ours)
            # print(state_ts)
            new_num_task_schedulable_only_lockstep, _, _ = get_num_task_schedulable_only_lockstep(state_ts, cfg['delta'], cfg['num_core'], cfg['max_num_task'])
            new_num_task_schedulable_dynamic_switching, _, _ = get_num_task_schedulable_dynamic_switching(state_ts, cfg['delta'], cfg['num_core'], cfg['max_num_task'])
            new_num_task_schedulable_ours, _, _ = get_num_task_schedulable_ours(state_ts, cfg['delta'], cfg['num_core'], cfg['max_num_task'])
            # new_num_tasks_ours, prms, mapped_task = get_num_tasks_ours_delta(state_ts, cfg['delta'])
            num_task_schedulable_only_lockstep = max(num_task_schedulable_only_lockstep, new_num_task_schedulable_only_lockstep)
            num_task_schedulable_dynamic_switching = max(num_task_schedulable_dynamic_switching, new_num_task_schedulable_dynamic_switching)
            num_task_schedulable_ours = max(num_task_schedulable_ours, new_num_task_schedulable_ours)

        # logger.write('{}'.format(num_core_ours))
        logger.write('{}, {}, {}'.format(num_task_schedulable_only_lockstep, num_task_schedulable_dynamic_switching, num_task_schedulable_ours))
        # print(f'ours: {num_core_ours:2}')
        # print(f'ours: {num_task_schedulable_ours:3}')
        # print(prms)
        # print(mapped_task)



def main():
    with open('cfg/cmp123_crit_numtasks_cfg.json', 'r') as f:
        cfg = json.load(f)

    # how many exp?
    for criticality_prob in cfg['critical_prob_list'] :
        for delta in cfg['deltas']:
            new_cfg = cfg.copy()
            new_cfg['num_states_list'] = cfg['num_states_list']
            new_cfg['critical_prob'] = criticality_prob
            new_cfg['delta'] = delta
        
            run_exp(new_cfg)
    
if __name__ == '__main__':
    main() 
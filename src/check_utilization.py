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

        # ls
        ls_core, ls_mapped_tasks = get_num_core_LS(stateless_ts, method='rta_single')
        ls_utilization_sum = [0.0 for _ in range(len(ls_mapped_tasks))]
        for i, ls_tasks in enumerate(ls_mapped_tasks):
            ls_utilization_sum[i] += sum([t[1]/t[0] for t in ls_tasks])
        ls_utilization_avg = sum(ls_utilization_sum)/len(ls_utilization_sum)

        # without rerun
        _, wo_prms, wo_mapped_tasks = get_num_core_ours_wo_drop(stateless_ts)
        wo_utilization_sum = [t[1]/t[0] if t is not None else 0.0  for t in wo_prms]
        for wo_task in wo_mapped_tasks:
            if wo_task[2] == 1:
                wo_utilization_sum[wo_task[3]] += wo_task[1]/wo_task[0]
        wo_utilization_avg = sum(wo_utilization_sum)/len(wo_utilization_sum)

        # ours
        _, ours_prms, ours_mapped_tasks = get_num_core_ours(stateless_ts)
        ours_utilization_sum = [t[1]/t[0] if t is not None else 0.0  for t in ours_prms]
        for task in ours_mapped_tasks:
            if task[2] == 1:
                ours_utilization_sum[task[3]] += task[1]/task[0]
        ours_utilization_avg = sum(ours_utilization_sum)/len(ours_utilization_sum)

        logger.write('{},{},{}'.format(ls_utilization_avg, wo_utilization_avg, ours_utilization_avg))
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
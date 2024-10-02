import json
import time
from generator.generator import generate_tasksets
from core.numtask import get_num_task_schedulable
# from core.only_lockstep import get_num_core_only_lockstep, get_num_task_schedulable_only_lockstep
# from core.dynamic_switching import get_num_core_dynamic_switching, get_num_task_schedulable_dynamic_switching
# from core.ours import get_num_core_ours, get_num_task_schedulable_ours
from logger.logger import Logger

def run_exp(cfg):
    tasks = generate_tasksets(cfg)
    
    for state in cfg['num_states_list']:
        # print({**cfg, 'num_states': state})
        logger = Logger({**cfg, 'num_states': state}, filepath="output/main", log_params=['num_states', 'critical_prob', 'num_tasks', 'task_max_utilization', 'delta'])
        exp(tasks, cfg, logger)


def exp(tasks, cfg, logger):
    worstfit_sort = 0.0
    worstfit_iterative = 0.0
    transform_sort = 0.0
    exp_count = 0
    for task_set in tasks:
        task_set.assign_new_criticality(cfg['num_states'])
        
        # num_core_ours = 0
        num_task_schedulable_only_lockstep = 0
        num_task_schedulable_dynamic_switching = 0
        num_task_schedulable_dynamic_switching_iterative = 0
        num_task_schedulable_ours = 0
        num_task_schedulable_ours_iterative = 0
        # num_task_schedulable_ours_transform = 0


        for s in range(cfg['num_states']):
            ### 여기서 튜플로 변환
            state_ts = task_set.get_tasks(sort=False, desc=True, state_num=s)

            #################################################################
            # binding_policy "sort" / "neighbor" / "iterative" / "exhaustive"
            # partitioning_policy "worstfit" / "transform - trash" / "exhaustive"
            # fault_handling_policy "only_lockstep" / "dynamic_switching" / "ours"
            #################################################################

            
            # ## only_lockstep
            new_num_task_schedulable_only_lockstep, _, _ = get_num_task_schedulable(state_ts, cfg['num_core'], cfg['max_num_task'],
                                                                                        'only_lockstep',
                                                                                        'sort', cfg['binding_constant'],
                                                                                        'worstfit',
                                                                                        cfg['partitioning_constant'], cfg)
            num_task_schedulable_only_lockstep = max(num_task_schedulable_only_lockstep, new_num_task_schedulable_only_lockstep)

            # ## dynamic_switching
            new_num_task_schedulable_dynamic_switching, _, _ = get_num_task_schedulable(state_ts, cfg['num_core'], cfg['max_num_task'],
                                                                                        'dynamic_switching',
                                                                                        'sort', cfg['binding_constant'],
                                                                                        'worstfit',
                                                                                        cfg['partitioning_constant'], cfg)
            num_task_schedulable_dynamic_switching = max(num_task_schedulable_dynamic_switching, new_num_task_schedulable_dynamic_switching)

            new_num_task_schedulable_dynamic_switching_iterative, _, _ = get_num_task_schedulable(state_ts, cfg['num_core'], cfg['max_num_task'],
                                                                                        'dynamic_switching',
                                                                                        'iterative', cfg['binding_constant'],
                                                                                        'worstfit',
                                                                                        cfg['partitioning_constant'], cfg)
            num_task_schedulable_dynamic_switching_iterative = max(num_task_schedulable_dynamic_switching_iterative, new_num_task_schedulable_dynamic_switching_iterative)

            ## ours
            start_time_worstfit_sort = time.time()
            new_num_task_schedulable_ours, _, _ = get_num_task_schedulable(state_ts, cfg['num_core'], cfg['max_num_task'],
                                                                                        'ours',
                                                                                        'sort', cfg['binding_constant'],
                                                                                        'worstfit',
                                                                                        cfg['partitioning_constant'], cfg)
            num_task_schedulable_ours = max(num_task_schedulable_ours, new_num_task_schedulable_ours)
            end_time_worstfit_sort = time.time()
            elapsed_time_worstfit_sort = end_time_worstfit_sort - start_time_worstfit_sort

            start_time_worstfit_iterative = time.time()
            new_num_task_schedulable_ours_iterative, _, _ = get_num_task_schedulable(state_ts, cfg['num_core'], cfg['max_num_task'],
                                                                                        'ours',
                                                                                        'iterative', cfg['binding_constant'],
                                                                                        'worstfit',
                                                                                        cfg['partitioning_constant'], cfg)
            num_task_schedulable_ours_iterative = max(num_task_schedulable_ours_iterative, new_num_task_schedulable_ours_iterative)
            end_time_worstfit_iterative = time.time()
            elapsed_time_worstfit_iterative = end_time_worstfit_iterative - start_time_worstfit_iterative

            worstfit_sort += elapsed_time_worstfit_sort
            worstfit_iterative += elapsed_time_worstfit_iterative
            # transform_sort += elapsed_time_transform_sort

        # logger.write('{}'.format(num_core_ours))
        # logger.write('{}'.format(num_task_schedulable_dynamic_switching))
        # logger.write('{}, {}, {}'.format(num_task_schedulable_only_lockstep, num_task_schedulable_dynamic_switching, num_task_schedulable_ours))
        logger.write('{}, {}, {}, {}, {}'.format(num_task_schedulable_only_lockstep, num_task_schedulable_dynamic_switching, num_task_schedulable_dynamic_switching_iterative, num_task_schedulable_ours, num_task_schedulable_ours_iterative))
        # print(f'ours: {num_core_ours:2}')
        # print(f'ours: {num_task_schedulable_ours:3}')
        # print(prms)
        # print(mapped_task)

    worstfit_sort /= len(tasks)
    worstfit_iterative /= len(tasks)
    # transform_sort /= len(tasks)
    print(f'worstfit_sort:{worstfit_sort}, worstfit_iterative:{worstfit_iterative}, transform_sort:{transform_sort}')

def main():
    with open('cfg/main_cfg.json', 'r') as f:
        cfg = json.load(f)

    # with open('cfg/debug_cfg.json', 'r') as f:
    #     cfg = json.load(f)

    # how many exp?
    for criticality_prob in cfg['critical_prob_list'] :
        new_cfg = cfg.copy()
        new_cfg['num_states_list'] = cfg['num_states_list']
        new_cfg['critical_prob'] = criticality_prob        
        run_exp(new_cfg)
    
if __name__ == '__main__':
    main() 
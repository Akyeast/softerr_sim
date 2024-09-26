import json
from itertools import product
# from src.core.backups.task_sche_check import assign_nc2PRM, assign_nc_bind
from core.utils import argmin, argmax
from core.bind import bind_nc_tasks
from core.tda import tda_analysis_ol, tda_analysis_ds, tda_analysis_ours, tda_analysis_ol_transform, tda_analysis_ds_transform, tda_analysis_ours_transform
from core.partition import partition

# with open('cfg/prm_cfg.json', 'r') as f:
#     cfg = json.load(f)

# ################## cfg
# {
#     "num_task_sets": 2000,
#     "num_tasks": 80,
#     "max_num_task": 80,
#     "critical_prob_list": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
#     "criticality_per_state": false,
#     "period": [10, 50],
#     "num_states_list": [1],
#     "num_states": 1,
#     "task_max_utilization": 0.3,
#     "max_util_list": [1.0],
#     "period_gen": "log",
#     "util_gen": "random",
#     "num_core": 8,
#     "max_num_core": 8,
#     "deltas": [1.0],
#     "binding_constant": 0.1,
#     "partitioning_constant": 0.1
# }

def get_num_task_schedulable(tasks, num_core=8, max_num_task=40,
                             fault_handling_policy="only_lockstep",
                             binding_policy="sort", binding_constant=0.1,
                             partitioning_policy="worstfit", partitioning_constant=0.1,
                             cfg={}):

    # print('NUM TASK::entrance!')
    
    num_task = 0
    is_schedulable = True
    num_task_schedulable = 0
    mapped_tasks = []
    mapped_ls_tasks = [[] for _ in range(num_core)]
    assigned_util = [0.0 for _ in range(num_core)]

    ## task binding debug
    # check_schedulable(tasks[0:max_num_task], num_core, max_num_task,
    #                   fault_handling_policy,
    #                   binding_policy, binding_constant,
    #                   partitioning_policy, partitioning_constant,
    #                   cfg)

    ## tda debug
    # # check_schedulable(tasks[0:max_num_task], num_core, max_num_task,
    #                     fault_handling_policy,
    #                     binding_policy, binding_constant,
    #                     partitioning_policy, partitioning_constant,
    #                     cfg)

    ## transform debug
    # check_schedulable(tasks[0:max_num_task], num_core, max_num_task,
    #                   fault_handling_policy,
    #                   binding_policy, binding_constant,
    #                   partitioning_policy, partitioning_constant,
    #                   cfg)
    
    while is_schedulable:
        num_task += 1
        if num_task > max_num_task:
            break
        
        is_schedulable, mapped_tasks, assigned_util = check_schedulable(tasks[0:num_task], num_core, max_num_task,
                                                                        fault_handling_policy,
                                                                        binding_policy, binding_constant,
                                                                        partitioning_policy, partitioning_constant,
                                                                        cfg)
        

    num_task_schedulable = num_task - 1


    # num_task_schedulable = len(mapped_tasks)

    # print("###############################")
    # print(f'DEBUG_ds_overall: {len(mapped_tasks)}')
    # print("###############################")

    return num_task_schedulable, mapped_tasks, assigned_util

def check_schedulable(tasks, num_core=8, max_num_task=40,
                      fault_handling_policy="only_lockstep",
                      binding_policy="sort", binding_constant=0.1,
                      partitioning_policy="worstfit", partitioning_constant=0.1,
                      cfg={}):
    """
        Input: 
            [(period, execution, critical), (5, 3, 1), ...] 
        Output:
            Schedulable(1,0)
    """    
    is_schedulable = False
    mapped_ls_tasks = [[] for _ in range(num_core)]
    assigned_utils = [0.0 for _ in range(num_core)]
    
    # print("DYNAMIC_SWITCHING: taskbinding call")
    c_tasks = [task for task in tasks if task[2] == 1]
    nc_tasks = [task for task in tasks if task[2] == 0]

    nc_tasks_binded = []

    if fault_handling_policy == "only_lockstep":
        nc_tasks_binded = nc_tasks
    elif fault_handling_policy == "dynamic_switching" or fault_handling_policy == "ours":
        nc_tasks_binded, _ = bind_nc_tasks(nc_tasks, binding_policy, binding_constant)
    else:
        print('never reached??')
    # print("DYNAMIC_SWITCHING: return")
    
    #lockstep_tasks
    ls_tasks = c_tasks+nc_tasks_binded
    num_ls_core = (int)(num_core/2)
    # print(f'ls_tasks = {ls_tasks}')
    # print('DYNAMIC SWITCHING::call tda_analysis')
    
    # utilization overflow when partitioning
    overflow = False

    overflow, mapped_ls_tasks, assigned_utils = partition(ls_tasks, num_ls_core,
                                                         partitioning_policy, partitioning_constant, 
                                                         cfg)
    is_schedulable, mapped_ls_tasks, assigned_utils = tda_analysis(num_ls_core, mapped_ls_tasks,
                                                                   fault_handling_policy, cfg)


    # print(f'return is_schedulable: {is_schedulable}')
    # print(f'return mapped_ls_tasks: {mapped_ls_tasks}')
    # print(f'return assigned_util: {assigned_util}')
    
    return is_schedulable, mapped_ls_tasks, assigned_utils
def tda_analysis(mapped_ls_tasks, num_ls_core=4, fault_handling_policy="worstfit", cfg={}):
    is_schedulable = False

    for core_index in range(num_ls_core):
        if fault_handling_policy == "only_lockstep":
            if tda_analysis_ol(mapped_ls_tasks[core_index]):

    
    return is_schedulable


def partition_and_analysis_worstfit(ls_tasks, num_ls_core=4,
                                    fault_handling_policy="only_lockstep",
                                    partitioning_constant=0.1,
                                    cfg={}):
    
    is_schedulable = False
    mapped_ls_tasks = [[] for _ in range(num_ls_core)]
    assigned_utils = [0.0 for _ in range(num_ls_core)]

    for task in ls_tasks:
        worstfit_core_num = argmin(assigned_utils)
        for core_num in range(0)

        if fault_handling_policy == "only_lockstep":
            if tda_analysis_ol(mapped_ls_tasks[worstfit_core_num]+[task]):
                mapped_ls_tasks[worstfit_core_num].append(task)
                assigned_utils[worstfit_core_num] += task[1]/task[0]
            else:
                break       

        elif fault_handling_policy == "dynamic_switching":
            if tda_analysis_ds(mapped_ls_tasks[worstfit_core_num]+[task]):
                mapped_ls_tasks[worstfit_core_num].append(task)
                assigned_utils[worstfit_core_num] += task[1]/task[0]
            else:
                break
            
        elif fault_handling_policy == "ours":
            if tda_analysis_ours(mapped_ls_tasks[worstfit_core_num]+[task]):
                mapped_ls_tasks[worstfit_core_num].append(task)
                assigned_utils[worstfit_core_num] += task[1]/task[0]
            else:
                break

        else:
            print(f'never reached')
    else:
        is_schedulable = True
    
    # print(is_schedulable)

    return is_schedulable, mapped_ls_tasks, assigned_utils

def partition_and_analysis_bestfit(ls_tasks, num_ls_core=4,
                                    fault_handling_policy="only_lockstep",
                                    partitioning_constant=0.1,
                                    cfg={}):
    
    is_schedulable = False
    mapped_ls_tasks = [[] for _ in range(num_ls_core)]
    assigned_utils = [0.0 for _ in range(num_ls_core)]

    for task in ls_tasks:
        bestfit_core_num = argmax(assigned_utils)

        if fault_handling_policy == "only_lockstep":
            if tda_analysis_ol(mapped_ls_tasks[bestfit_core_num]+[task]):
                mapped_ls_tasks[bestfit_core_num].append(task)
                assigned_utils[bestfit_core_num] += task[1]/task[0]
            else:
                break       

        elif fault_handling_policy == "dynamic_switching":
            if tda_analysis_ds(mapped_ls_tasks[bestfit_core_num]+[task]):
                mapped_ls_tasks[bestfit_core_num].append(task)
                assigned_utils[bestfit_core_num] += task[1]/task[0]
            else:
                break
            
        elif fault_handling_policy == "ours":
            if tda_analysis_ours(mapped_ls_tasks[bestfit_core_num]+[task]):
                mapped_ls_tasks[bestfit_core_num].append(task)
                assigned_utils[bestfit_core_num] += task[1]/task[0]
            else:
                break

        else:
            print(f'never reached')
    else:
        is_schedulable = True
    
    # print(is_schedulable)

    return is_schedulable, mapped_ls_tasks, assigned_utils


################ TBD ##################
def partition_and_analysis_exhaustive(ls_tasks, num_ls_core=4,
                                    fault_handling_policy="only_lockstep",
                                    partitioning_constant=0.1,
                                    cfg={}):
    
    is_schedulable = False
    mapped_ls_tasks = [[] for _ in range(num_ls_core)]
    assigned_utils = [0.0 for _ in range(num_ls_core)]

    if fault_handling_policy == "only_lockstep":
        print(f'fault_handling_policy is {fault_handling_policy}')

    elif fault_handling_policy == "dynamic_switching":
        print(f'fault_handling_policy is {fault_handling_policy}')
        
    elif fault_handling_policy == "ours":
        print(f'fault_handling_policy is {fault_handling_policy}')  
           
    else:
        print(f'never reached')

    return is_schedulable, mapped_ls_tasks, assigned_utils
################ TBD ##################

def transform_ls_tasks(ls_tasks, partitioning_constant=0.1):
    transform_multipliers = []
    transformed_ls_tasks = []

    min_period = min(task[0] for task in ls_tasks)
    min_exec = min(task[1] for task in ls_tasks)

    for task in ls_tasks:
        period, exec, criticality = task
        
        period_multiplier, transformed_period = rounding_down_period_multiplier(period, min_period, partitioning_constant)
        exec_multiplier, transformed_exec = rounding_up_exec_multiplier(exec, min_exec, partitioning_constant)
        
        transform_multipliers.append((period_multiplier, exec_multiplier, criticality))
        transformed_ls_tasks.append((transformed_period, transformed_exec, criticality))

    return min_period, min_exec, transform_multipliers, transformed_ls_tasks

def rounding_down_period_multiplier(period, min_period, partitioning_constant):
    multiplier = 0

    while min_period * (1+partitioning_constant)**multiplier <= period:
        multiplier += 1
    
    multiplier -= 1
    transformed_period = min_period * (1+partitioning_constant)**multiplier
    
    return multiplier, transformed_period

def rounding_up_exec_multiplier(exec, min_exec, partitioning_constant):
    multiplier = 0
    transformed_period = min_exec

    while min_exec * (1+partitioning_constant)**multiplier < exec:
        multiplier += 1
    
    transformed_exec = min_exec * (1+partitioning_constant)**multiplier
    
    return multiplier, transformed_exec

def classificate_tasks(transform_multipliers):
    max_period_multiplier = max(multipliers[0] for multipliers in transform_multipliers)
    max_exec_multiplier = max(multipliers[1] for multipliers in transform_multipliers)
    
    # print(f'max_period = {max_period_multiplier}, max_exec = {max_exec_multiplier}')
    task_classificated = [[0 for _ in range(max_exec_multiplier+1)] for _ in range(max_period_multiplier+1)]

    for multiplier in transform_multipliers:
        period_mult, exec_mult, _ = multiplier
        task_classificated[period_mult][exec_mult] += 1

    return task_classificated, max_period_multiplier, max_exec_multiplier

def multipliers2tasks(transform_multipliers, min_period, min_exec, partitioning_constant):
    transformed_ls_tasks = []
    for pm, em, crit in transform_multipliers:
        transformed_ls_tasks.append((min_period * (1+partitioning_constant)**pm, min_exec*(1+partitioning_constant)**em, crit))
    return transformed_ls_tasks

def construct_all_sub_tasksets(task_classificated):
    
    options = []
    for period_mult, exec_counts in enumerate(task_classificated):
        for exec_mult, count in enumerate(exec_counts):
            options.append([(period_mult, exec_mult, num_tasks) for num_tasks in range(count + 1)])

    all_sub_tasksets = list(product(*options))

    return all_sub_tasksets

def check_sub_tasksets_match(all_sub_tasksets, i, k, l):
    dict_i = {(pm, em): count for pm, em, count in all_sub_tasksets[i]}
    dict_k = {(pm, em): count for pm, em, count in all_sub_tasksets[k]}
    dict_l = {(pm, em): count for pm, em, count in all_sub_tasksets[l]}
    
    for (pm, em), c_i_pmem in dict_i.items():
        c_k_pmem = dict_k.get((pm, em), 0)
        c_l_pmem = dict_l.get((pm, em), 0)
        
        if c_i_pmem != c_k_pmem + c_l_pmem:
            return False
    
    return True

def check_edf_schedulable(edf_schedulability_table, i):
    return all(edf_schedulability_table[i])  
#####################NOT Used below##########################

# def assign_critical_tda_reserve_rerun(core, c_tasks, delta):
#     mapped_tasks = [[] for _ in range(core)]
#     heuristic = 'wf'
#     assigned_cores = [0.0 for _ in range(core)]
#     index = 0

#     for task in c_tasks: 
#         #### get index
#         if heuristic == 'wf':
#             if min(assigned_cores) + task[1]/task[0] <= 1:
#                 index = argmin(assigned_cores)
#                 index_pair = index+1
#             else:
#                 return False, mapped_tasks, assigned_cores
#         elif heuristic == 'bf':
#             print('not implemented')
#         else:
#             raise ValueError("heuristic must be 'wf' or 'bf'")
        
#         #### tda_analysis
#         if tda_analysis(mapped_tasks[index] + [task], delta):
#             mapped_tasks[index].append(task)
#             mapped_tasks[index_pair].append(task)
#             utilization = task[1]/task[0]
#             assigned_cores[index] += utilization
#             assigned_cores[index_pair] += utilization
#         else:
#             return False, mapped_tasks, assigned_cores

#     ## reserve rerun
#     for i in range(core):
#         max_exec = 0
#         largest = None
#         for task in mapped_tasks[i]:
#             if task[2] == 1 and task[1] >= max_exec:
#                 ### always task[2] == 1  here
#                 max_exec = task[1]
#                 largest = task
#         if largest != None:
#             assigned_cores[i] += largest[1]/largest[0]            

#     # print("!!!!!!!!!!!!!!!!!!DS!!!!!!!!!!!!!")
#     # print(assigned_cores)

#     return True, mapped_tasks, assigned_cores

# def assign_critical_tda_reserve_rerun(core, c_tasks, delta):
#     mapped_tasks = [[] for _ in range(core)]
#     modified_list = []
#     for task in c_tasks: 
#         for i in range(core):
#             if tda_analysis(mapped_tasks[i] + [task], delta):
#                 mapped_tasks[i].append(task)
#                 modified_list.append((*task, i))
#                 break
#         else:
#             return False, [], []

#     assigned_utils = []
#     for i in range(core):
#         assigned_utils.append(0)
#         max_exec = 0
#         largest = mapped_tasks[i][0] if len(mapped_tasks[i]) > 0 else None
#         for task in mapped_tasks[i]:
#             utilization = task[1]/task[0]
#             assigned_utils[i] += utilization
#             if task[1] >= max_exec:
#                 max_exec = task[1]
#                 largest = task
#         if largest != None:
#             assigned_utils[i] += largest[1]/largest[0]

#     return True, modified_list, assigned_utils

# def get_num_core_dynamic_switching(tasks, delta=1.0, max_num_core=16, max_num_task=40):
#     num_core = 0
#     prms = []
#     mapped_tasks = []

#     is_schedulable = False

#     while not is_schedulable:
#         num_core += 2
        
#         if num_core > max_num_core:
#             num_core -= 2
#             break        
        
#         is_schedulable, prms, mapped_tasks = check_schedulable_dynamic_switching(tasks, delta, num_core)
        

#         # print(f'DEBUG_only_lockstep___3: {num_task}')

#     return num_core, prms, mapped_tasks
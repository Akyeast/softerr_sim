import math
from core.task_sche_check import lcm

def tda_analysis(tasks, delta=1.0, fault=True):
    max_t = lcm([t[0] for t in tasks])
    min_t = min([task[0] for task in tasks])
    rerun = 0

    ## rerun capacity
    # if fault:
    #     rerun = max([task[1] for task in tasks]) if fault else 0

    for t in range(0, max_t+1):
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        demand = sum(math.floor((t / task[0]))*task[1] for task in tasks) 
        if t >= min_t:
            demand += rerun
        if demand > t :
            return False                
        if demand+1000 < t :
            return True
    else:
        return True
    
def tda_analysis_onlyls(tasks, delta=1.0, fault=True):
    max_t = lcm([t[0] for t in tasks])
    min_t = min([task[0] for task in tasks])
    rerun = 0

    ## rerun capacity
    # if fault:
    #     for task in tasks:
    #         if task[2] == 1 and task[1] >= rerun:
    #             rerun = task[1]
    
    for t in range(0, max_t+1):
        # demand = sum(math.floor(((t - task[0]*delta) / task[0]) + 1)*task[1] for task in tasks) 
        demand = sum(math.floor((t / task[0]))*task[1] for task in tasks) 
        if t >= min_t:
            demand += rerun
        if demand > t :
            return False                
        if demand+1000 < t :
            return True
    else:
        return True

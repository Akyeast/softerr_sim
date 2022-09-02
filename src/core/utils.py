import math

def get_minimum_core(task_set):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: minimum number of core under LS/PF swtiching
    """
    utilization = 0.0
    for task in task_set:
        u = task[1] / task[0]
        utilization += u if task[2] == 1 else u / 2.0

    return math.ceil(utilization) * 2

def get_PRM_bound(core_utils) :
    """
        // only for single core EDF
        Input: 
            [core1_util, core2_util, ...]
        Output:
            PRM bound
    """
    return [1.0-core_util for core_util in core_utils]

def argmin(lst, array=False):
    srt_lst = sorted(range(len(lst)), key=lambda k: lst[k])
    
    if array:
        return srt_lst
    else :
        return srt_lst[0]

def argmax(lst, array=False):
    srt_lst = sorted(range(len(lst)), key=lambda k: lst[k], reverse=True)
    
    if array:
        return srt_lst
    else :
        return srt_lst[0]
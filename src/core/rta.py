import math
from urllib import response

def rta_all(task_set, num_core):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: boolean (True if all tasks are schedulable, False otherwise)
    """
    for i in range(len(task_set)):
        if not rta_task(task_set, i, num_core):
            return False
    else:
        return True


def rta_task(task_set, index, num_core):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...], task_index, number of core
        Output: boolean (True if task_set[index] is schedulable, False otherwise)
    """
    task = task_set[index]
    response_time = task[1]

    while response_time < task_set[index][0] :
        sum_interfere = 0.0
        for k, _tsk in enumerate(task_set) :
            if index == k :
                continue
            sum_interfere += min(workload_bound(response_time, _tsk), interference_bound(task, _tsk), response_time-task[1]+1)
        
        all_interfere = math.floor(sum_interfere/ num_core)
        new_rt = task[1] + math.floor(all_interfere / num_core)

        if response_time == new_rt & new_rt < task_set[index][0]:
            return True

        response_time = new_rt

    return False

def workload_bound(interval, task):
    """
        Input: interval => integer, task => (period, execution, critical)
        output: workload bound
    """
    period, exct, _ = task
    num_job = math.floor((interval + period - exct) / period)
    return num_job*exct + min(exct, interval+period-exct-num_job*period)

def interference_bound(task_i, task_k):
    """
        Input: task_i => (period, execution, critical), task_k => (period, execution, critical)
        output: interference bound of a task i on a task k
    """
    period_i, exct_i, _ = task_i
    period_k, _, _ = task_k
    dbf = exct_i * (math.floor((period_k - period_i) / period_i) + 1)
    return dbf + min(exct_i, max(0, period_k - dbf*(period_i/exct_i)))
import math
from xmlrpc.client import Fault

from core.task_sche_check import lcm


def rta_all_wo_drop(tasks, prm_tasks, num_core, fault=False):
    re_run = max([t[1] for t in tasks]+[0])
    task_set = [*tasks, *prm_tasks]
    
    for i in range(len(task_set)):
        if not rta_task(task_set, i, num_core, fault, re_run=re_run):
            return False
    else:
        return True

def rta_all(task_set, num_core, fault=False):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: boolean (True if all tasks are schedulable, False otherwise)
    """
    for i in range(len(task_set)):
        if not rta_task(task_set, i, num_core, fault):
            return False
    else:
        return True

def rta_all_single(task_set, fault=False):
    """
        Do schedulability check per core (iterate all critical task)
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: boolean (True if all tasks are schedulable, False otherwise)
    """
    for i in range(len(task_set)):
        if not rta_task_single(task_set, i, fault=fault):
            return False
    else:
        return True

def rta_all_single_wo_drop(task_set, prm, fault=False):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...], prm => (period, execution)
        Output: boolean (True if all tasks are schedulable, False otherwise)
    """
    for i in range(len(task_set)):
        if not rta_task_single(task_set, i, prm=prm, fault=fault):
            return False
    else:
        if prm is None:
            return True
        return rta_task_single(task_set, len(task_set), prm=prm, fault=fault)

def rta_all_baseline(task_set, nc, fault=False):
    """
        Do schedulability check per core (iterate all critical task)
        Input: [(period, execution, critical), (5, 3, 1), ...]
        Output: boolean (True if all tasks are schedulable, False otherwise)
    """
    for i in range(len(task_set)):
        if not rta_task_single(task_set, i, prm=nc, fault=fault):
            return False
    else:
        return True

def rta_task_single(task_set, index, prm=None, fault=False):
    re_run = max([t[1] for t in task_set]+[0])
    new_task_set = task_set
    if prm is not None:
        if type(prm) == list:
            new_task_set = new_task_set + prm
        else:
            new_task_set = new_task_set + [prm]
        

    task = new_task_set[index]
    interfere_tasks = new_task_set[:index] + new_task_set[index+1:]
    max_rt = 0.0

    if fault :
        max_rt += task[1] + re_run

    # TODO: fix this range
    for a in range(max([t[0] for t in interfere_tasks]+[0])):
    # for a in range(lcm([t[0] for t in interfere_tasks])):
        sum_interference = sum([t[1] for t in interfere_tasks if t[0] <= a+task[0]])
        response_time = sum_interference + (task[1] if s_i(a, task)==0 else 0)

        while response_time <= task[0]:
            new_rt = workload_bound_single(a, response_time, task, interfere_tasks)
            if fault:
                new_rt += re_run
            if new_rt == response_time:
                break
            response_time = new_rt

        if response_time-a > max_rt:
            max_rt = response_time-a

    # print("response time of task {} is {}".format(task, max(task[1], max_rt)))
    return max(task[1], max_rt) <= task[0]

def s_i(a, task) :
    return a - math.floor(a/task[0])*task[0]

def workload_bound_single(start, interval, task, interfere_tasks):
    """
        Input: start => integer, interval => integer, task => (period, execution, critical), interfere_tasks => [(period, execution, critical), (5, 3, 1), ...]
        output: workload bound
    """
    bound = 0.0
    for t in interfere_tasks :
        if t[0] <= start + task[0] :
            released = s_i(start, task)
            delta = min(math.ceil((interval-released)/task[0]), 1+math.floor(start/task[0])) if interval >= released else 0
            bound += min(math.ceil(interval/t[0]), 1+math.floor((start+task[0]-t[0])/t[0]))*t[1] + delta*task[1]
    return bound

def rta_task(task_set, index, num_core, fault=False, re_run=None):
    """
        Input: [(period, execution, critical), (5, 3, 1), ...], task_index, number of core
        Output: boolean (True if task_set[index] is schedulable, False otherwise)
    """
    task = task_set[index]
    response_time = task[1]
    if re_run == None:
        re_run = max([t[1] for t in task_set])

    while response_time < task_set[index][0] :
        sum_interfere = 0.0
        for k, _tsk in enumerate(task_set) :
            if index == k :
                continue
            sum_interfere += min(workload_bound(response_time, _tsk), interference_bound(task, _tsk), response_time-task[1]+1)
        
        all_interfere = math.floor(sum_interfere/ num_core)

        if fault:
            new_rt = task[1] + math.floor((all_interfere + re_run) / num_core)
        else :
            new_rt = task[1] + math.floor(all_interfere / num_core)

        if (response_time == new_rt) & (new_rt < task_set[index][0]):
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
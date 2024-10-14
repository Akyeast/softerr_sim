import util
import tda

def worst_fit(tasks, rerun_idx, core_num):
    core_U = [0] * core_num
    core_assignments = [[] for _ in range(core_num)]
    critical_tasks = [task for task in tasks if task["critical"]]
    non_critical_tasks = [task for task in tasks if not task["critical"]]

    for task_idx, task in enumerate(critical_tasks):
        task_U = task["execution_time"] / task["period"]
        worst_core = core_U.index(min(core_U))
        core_assignments[worst_core].append(task)
        core_U[worst_core] += task_U
        if core_U[worst_core]>1:
            # print("U already exceeded 1 in critical tasks")
            return -1
        busy_period=util.L_max(core_assignments[worst_core])
        if tda.check_deadline_miss(core_assignments[worst_core], busy_period, rerun_idx):
            return task_idx
        
    for task_idx, task in enumerate(non_critical_tasks):
        task_U = task["execution_time"] / task["period"]
        worst_core = core_U.index(min(core_U))
        core_assignments[worst_core].append(task)
        core_U[worst_core] += task_U
        if core_U[worst_core]>1:
            # print("U exceeded 1")
            return -1
        busy_period=util.L_max(core_assignments[worst_core])
        # print("busy period: ", busy_period)
        if tda.check_deadline_miss(core_assignments[worst_core], busy_period, rerun_idx):
            return task_idx
    return 0
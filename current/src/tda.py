import math

def s_i(phi, p_i):
    return phi - math.floor(phi / p_i) * p_i
def W_i_all(tasks, i, phi, t):
    total_workload=0
    for task_idx, task in enumerate(tasks):
        if task_idx==i:
            p_i = task["period"]
            e_i = task["execution_time"]
            d_i = task["deadline"]
            break
    else:
        print("Task idx error")
        return 0

    total_workload+=W_i(phi, t, p_i, e_i)

    for other_task_idx, other_task in enumerate(tasks):
        if other_task_idx != task_idx:
            p_j = other_task["period"]
            e_j = other_task["execution_time"]
            d_j = other_task["deadline"]
            total_workload += W_j(phi, t, p_j, e_j, d_i, d_j)
    
    return total_workload

def W_i(phi, t, p_i, e_i):
    s_i_phi = s_i(phi, p_i)
    if t > s_i_phi:
        return min(math.ceil((t - s_i_phi) / p_i), 1 + math.floor(phi / p_i))*e_i
    return 0

def W_j(phi, t, p_j, e_j, d_i, d_j):
    return min(math.ceil(t / p_j), 1 + math.floor((phi + d_i - d_j) / p_j)) * e_j 

def L_i(tasks, i, phi, rerun_e):
    L_prev=-1
    L_curr=W_i_all(tasks, i, phi, 1)+rerun_e
    while(L_prev!=L_curr):
        L_prev=L_curr
        L_curr=W_i_all(tasks, i, phi, L_prev)+rerun_e
    return L_curr



# 데드라인 미스 체크
def check_deadline_miss(tasks, busy_period, rerun_idx):
    rerun_e = 0

    for task in tasks:
        if task['index'] == rerun_idx:
            rerun_e = task["execution_time"]
            break
    
    for task_idx, task in enumerate(tasks):
        for phi in range(busy_period + 1):
            rerunX_workload=L_i(tasks, task_idx, phi, 0)
            rerunO_workload=L_i(tasks, task_idx, phi, rerun_e)
                
            # 데드라인 미스 발생 여부 판단
            # print(workload, phi+task["deadline"])
            if rerunX_workload > phi+task["vertual_deadline"] or rerunO_workload > phi+task["deadline"]:
                return True    
    return False
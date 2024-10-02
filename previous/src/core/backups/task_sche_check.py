import math
from core.utils import argmin, argmax
from prm.demand import Demand
from generator.task import Task, TaskSet

def assign_nc_bind(core, nc_tasks, mapped_c_tasks, assigned_utils):
    binded_tasks, sorted_tasks = bind_nc_tasks(nc_tasks)
    mapped_nc_tasks_real = [[] for _ in range(core)]
    mapped_nc_tasks_binded = [[] for _ in range(core)]
    assigned_utils_real = assigned_utils
    assigned_utils_binded = assigned_utils
    heuristic = 'wf'
    # print(f'binded_tasks = {binded_tasks}, sorted_taqsks = {sorted_tasks}')

    for task in binded_tasks:
        if heuristic == 'wf':
            # print(task)
            # print(task['period'])
            # print(task[1])
            if min(assigned_utils_binded) + task[1]/task[0] <= 1 :
                index = argmin(assigned_utils)
                index_pair = index+1
            else:
                return False, mapped_nc_tasks_real, mapped_nc_tasks_binded, assigned_utils_real, assigned_utils_binded
        elif heuristic == 'bf':
            print('not implemented')
        else:
            raise ValueError("heuristic must be 'wf' or 'bf'")

        mapped_nc_tasks_binded[index].append(task)
        mapped_nc_tasks_binded[index_pair].append(task)
        assigned_utils_binded[index] += task[1]/task[0]
        assigned_utils_binded[index_pair] += task[1]/task[0]
    
    # print(assigned_utils_binded)
    return True, mapped_nc_tasks_real, mapped_nc_tasks_binded, assigned_utils_real, assigned_utils_binded

def bind_nc_tasks(tasks):
    # make new virtual tasks(Heuristic)
    sorted_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)
    # period sorting
    num_tasks = len(sorted_tasks)
    
    binded_tasks = []
    for i in range(int(num_tasks/2)):
        task_1 = sorted_tasks[2*i]
        if 2*i+1 < num_tasks:
            task_2 = sorted_tasks[2*i+1]
        else:
            task_2 = sorted_tasks[2*i]

        util_original = task_1[1]/task_1[0] + task_2[1]/task_2[0]
        util_binded = max(task_1[1], task_2[1])/min(task_1[0], task_2[0])

        if 2*util_original < util_binded:
            binded_tasks.append(task_1)
            binded_tasks.append(task_2)
        else:
            binded_task = Task(min(task_1[0], task_2[0]), max(task_1[1], task_2[1]), [0])
            binded_tasks.append(binded_task.get_task())
        # binded_tasks.append(binded_task.get_task())
    
    
    return binded_tasks, sorted_tasks

def get_minimum_theta(t, pi, dbf):
    return (math.sqrt((t-2*pi)**2 + 4*pi*dbf) - (t - 2*pi)) / 4

def get_optimal_theta(pi, demand):
    maximum_theta = 0

    for i in range(len(demand.tasks)):
        for point in range(demand.tasks[i][0], lcm([task[0] for task in demand.tasks])+1):
            theta = get_minimum_theta(point, pi, demand.demand(point, i))
            # print(f'demand at {i} is {demand.demand(point, i)}, supply at {i} is {2*theta/pi*(point-2*(pi-theta))}')
            if theta > maximum_theta:
                maximum_theta = theta

            # print(r'points {} and maximum A_k {} by theta {}'.format(point, demand.maximum_A_k(i, maximum_theta, pi), maximum_theta))
            if demand.maximum_A_k(i, maximum_theta, pi) <= point:
                break
    return maximum_theta

def assign_nc2PRM(prm_bounds, tasks):
    """
        Input:
            prms: [prm1_max_util, prm2_max_util, ...]
            tasks: [(period, execution, critical), (5, 3, 0), ...]
        Output:
            prms: [core1_util, core2_util, ...]
            tasks: [(period, execution, critical, index), (5, 3, 0, 1), ...]
    """
    prms = [[] for _ in range(len(prm_bounds))] # assigned NC
    prm_params = [None for _ in range(len(prm_bounds))] # PRM parameters (pi, theta)
    remain_utils = prm_bounds.copy()
    mapped_tasks = []

    for task in tasks:
        indexs = argmax(remain_utils, array=True)
        # indexs = argmin(remain_utils, array=True)
       
        for index in indexs :
            groups = prms[index] + [task]

            ## schedulability check
            demand = Demand(groups)
            pi = int(min([(t[0]-t[1]) for t in groups])/2)
            theta = get_optimal_theta(pi, demand)
            # print("optimal parameters: {}, {}, {}\n\n\n".format(pi, theta, prm_bounds[index]))
            if theta / pi <= prm_bounds[index]:
                prms[index] = groups
                prm_params[index] = (pi, theta)
                remain_utils[index] -= task[1] / task[0]
                mapped_tasks.append((*task, index))
                break
            
            for t in range(10000):
                prt_demand = demand.demand(t, index)
                new_theta = remain_utils[index]*pi
                prt_supply = 2*(new_theta/pi)*(t-2*(pi-new_theta))
                print(f'demand and supply : {prt_demand}, {prt_supply}')

        else :
            # not schedulable
            mapped_tasks.append((*task, None))
            # print('remain util: ', remain_utils)
            # print('prm bounds: ', prm_bounds)
            # print('indexs: ', indexs, '\n')

    return prm_params, mapped_tasks

if __name__ == '__main__':
    tasks = [(10, 2, 0)]
    prm_bounds = [1.0]
    pi = 10
    prm_params, mapped_tasks = assign_nc2PRM(prm_bounds, tasks, pi)
    print(prm_params)
    print(mapped_tasks)
import random 
import json
import math
from generator.utils import UUniFastDiscard, SimpleRandom, SimpleFixed
from scipy.stats import loguniform
from generator.task import Task, TaskSet

def generate_tasksets(cfg):
    if "util_gen" not in cfg :
        tasksets_util = SimpleRandom(cfg['num_tasks'], cfg['num_task_sets'], cfg['task_max_utilization'])
    elif cfg["util_gen"] == 'random' : 
        tasksets_util = SimpleRandom(cfg['num_tasks'], cfg['num_task_sets'], cfg['task_max_utilization'])
    elif cfg["util_gen"] == 'fixed' : 
        tasksets_util = SimpleFixed(cfg['num_tasks'], cfg['num_task_sets'], cfg['task_max_utilization'])
    elif cfg["util_gen"] == 'uunifast':
        tasksets_util = UUniFastDiscard(cfg['num_tasks'], cfg['task_set_utilization'], cfg['num_task_sets'], cfg['task_max_utilization'])
    else :
        raise NotImplementedError

    # period_from, period_to = cfg['period']
    critical_prob = cfg['critical_prob']
    criticality_per_state = cfg['criticality_per_state']

    gen_taskset = []

    for task_set in tasksets_util:
        tasks = []
        for task_util in task_set :
            if cfg['period_gen'] == "sampling":
                period = random.sample(cfg['period'], k=1)[0]
                # random in list
            elif cfg['period_gen'] == "uniform" :
                period = random.randint(*cfg['period']) # both included
                # random in range - uniform dist
            elif cfg['period_gen'] == "log":
                period = round(loguniform.rvs(*cfg['period']))
            else :
                raise NotImplementedError
            
            execution = max(math.floor(task_util * period), 1)

            # TODO: Remove * cfg['num_states']
            critical_factor = 1 if random.random() < critical_prob else 0
            if criticality_per_state :
                if critical_factor == 1 : # if task is critical
                    criticality = [1 if random.random() < 0.3 else 0 for _ in range(cfg['num_states'])] 
                else :
                    criticality = [0] * cfg['num_states']
            else :
                criticality = [critical_factor]  * cfg['num_states']

            tasks.append(Task(period, execution, criticality))

        gen_taskset.append(TaskSet(tasks))

    return gen_taskset


def generate_example_taskset() :
    # (period, execution, criticality per state)
    tasks = [
        Task(70, 5, [0]),
        Task(90, 5, [0]),
    ]

    return TaskSet(tasks)

if __name__ == '__main__':
    cfg = {
        'num_tasks' : 5,
        'num_task_sets' : 1,
        'task_max_utilization' : 0.7,
        'period' : [10, 30],
        'critical_prob' : 0.5,
        'criticality_per_state' : True,
        'num_states' : 5,
    }
    tasks = generate_tasksets(cfg)
    print(tasks[0])
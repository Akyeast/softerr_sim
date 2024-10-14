import json
import random
import os
import math
import time

import viz
import util
import partition
import generate
import numtask
import bind

# JSON 파일에서 태스크 범위 정보 불러오기
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def main(config_file):
    start_time = time.time()
    config = load_config(config_file)
    
    num_tasks = config['num_tasks']
    period_range = config['period_range']
    utilization_range = config['utilization_range']

    critical_ratio_num=10
    exp_per_critical_ratio=50

    task_limits_default=[]
    task_limits_binded=[]
    for i in range(critical_ratio_num+1):
        critical_ratio=i/critical_ratio_num

        max_task_default=[]
        max_task_binded=[]
        for i in range(exp_per_critical_ratio):
            tasks = generate.random_task_set(num_tasks, period_range, utilization_range, critical_ratio)
            max_task_default.append(numtask.calculate_max_tasks_default(tasks, core_num=4))
            max_task_binded.append(numtask.calculate_max_tasks_binding(tasks, core_num=4))
        task_limit_default=sum(max_task_default)/len(max_task_default)
        task_limit_binded = sum(max_task_binded)/len(max_task_binded)
        print("critical ratio :", critical_ratio, "default task limit :", task_limit_default, "binded task limit :", task_limit_binded)
        task_limits_default.append(task_limit_default)
        task_limits_binded.append(task_limit_binded)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time cost : {elapsed_time:.5f}")
    viz.visualize_task_limit([task_limits_default, task_limits_binded], critical_ratio_num, period_range, utilization_range)
    # visualize_schedule(tasks, min(busy_period, 10*tasks[0]['period']))

if __name__ == "__main__":
    # config.json 파일 경로
    config_file = os.path.join(os.path.dirname(__file__), '..', 'cfg', 'config_hard.json')
    main(config_file)

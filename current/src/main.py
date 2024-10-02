import json
import random
import os
import math

# JSON 파일에서 태스크 범위 정보 불러오기
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# 랜덤 태스크 셋 생성 함수
def generate_random_task_set(num_tasks, period_range, exec_time_range):
    while True:
        tasks = []
        total_utilization = 0
        
        for i in range(num_tasks):
            period = random.randint(period_range[0], period_range[1])
            execution_time = random.randint(exec_time_range[0], exec_time_range[1])
            task_utilization = execution_time / period
            total_utilization += task_utilization
            tasks.append({
                "index": i,
                "period": period,
                "execution_time": execution_time
            })
        
        if total_utilization <= 1:
            break
        else:
            print(f"Total Utilization exceeded 1 ({total_utilization}), regenerating task set...")
    return tasks

# Busy Period 계산 함수 (EDF 기준)
def calculate_busy_period(tasks):
    busy_period = sum(task["execution_time"] for task in tasks)
    while True:
        workload = sum((busy_period // task["period"]+1) * task["execution_time"] for task in tasks)
        if workload == busy_period:
            break
        busy_period = workload
    return busy_period

def s_i(a, T_i):
    return a - math.floor(a / T_i) * T_i

def delta_i(a, t, T_i):
    s_i_a = s_i(a, T_i)
    if t > s_i_a:
        return min(math.ceil((t - s_i_a) / T_i), 1 + math.floor(a / T_i))
    return 0


# 데드라인 미스 체크 함수
def check_deadline_miss(tasks, busy_period):
    missed_deadline_tasks = []
    
    for task_idx, task in enumerate(tasks):
        T_i = task["period"]
        C_i = task["execution_time"]
        D_i=T_i
        
        for a in range(busy_period + 1):
            for t in range(a, busy_period + 1):
                workload = 0
                
                for other_task_idx, other_task in enumerate(tasks):
                    if other_task_idx != task_idx:
                        T_j = other_task["period"]
                        C_j = other_task["execution_time"]
                        D_j = T_j
                        
                        workload += min(
                            math.ceil(t / T_j),
                            1 + math.floor((a + D_i - D_j) / T_j)
                        ) * C_j
                
                # Task i의 워크로드 계산
                workload += delta_i(a, t, T_i) * C_i
                
            # 데드라인 미스 발생 여부 판단
            # print(workload, a+D_i)
            if workload > a+D_i:
                missed_deadline_tasks.append((task, a))
                break
                
    return missed_deadline_tasks


# 실행
def main(config_file):
    config = load_config(config_file)
    
    num_tasks = config['num_tasks']
    period_range = config['period_range']
    execution_time_range = config['execution_time_range']

    # 랜덤 태스크 셋 생성
    tasks = generate_random_task_set(num_tasks, period_range, execution_time_range)
    
    # 태스크 정보 출력
    for i, task in enumerate(tasks):
        print(f"Task {i+1} - Period: {task['period']}, Execution Time: {task['execution_time']}")

    # Max Busy Period 계산
    busy_period = calculate_busy_period(tasks)
    print(f"Calculated Maximum Busy Period: {busy_period}")

    missed_deadline_tasks=check_deadline_miss(tasks, busy_period)
    if missed_deadline_tasks==[]:
        print("Successed deadline check")
    else:
        print("Fail!")
        print(missed_deadline_tasks)

if __name__ == "__main__":
    # config.json 파일 경로
    config_file = os.path.join(os.path.dirname(__file__), '..', 'cfg', 'config.json')
    main(config_file)

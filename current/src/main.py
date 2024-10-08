import json
import random
import os
import math
import matplotlib.pyplot as plt

# JSON 파일에서 태스크 범위 정보 불러오기
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# 랜덤 태스크 셋 생성 함수
def generate_random_task_set(num_tasks, num_C_tasks, period_range, exec_time_range):
    if num_C_tasks>num_tasks: print("check task num")
    while True:
        tasks = []
        total_utilization = 0
        
        for i in range(num_tasks):
            period = random.randint(period_range[0], period_range[1])
            execution_time = random.randint(exec_time_range[0], exec_time_range[1])
            task_utilization = execution_time / period
            total_utilization += task_utilization
            taskinfo={
                "index": i,
                "period": period,
                "execution_time": execution_time,
                "diff" : 0
            }
            if num_C_tasks>0:
                taskinfo["critical_task"]=True
                num_C_tasks-=1
            else:
                taskinfo["critical_task"]=False
            tasks.append(taskinfo)
        
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
    missed_deadline_tasks=[]
    for task_idx, task in enumerate(tasks):
        miss_tasks=check_deadline_miss_single_task(tasks, task_idx, busy_period)
        if miss_tasks!=[]:
            missed_deadline_tasks.append(miss_tasks)
    return missed_deadline_tasks

def check_deadline_miss_single_task(tasks, rerun_task_idx, busy_period):
    missed_deadline_tasks = []
    for task_idx, task in enumerate(tasks):
        if rerun_task_idx == task_idx:
            task["diff"]=task["execution_time"]


    
    for task_idx, task in enumerate(tasks):
        T_i = task["period"]
        C_i = task["execution_time"]
        D_i=T_i-task["diff"]
        
        for a in range(busy_period + 1):
            for t in range(a, busy_period + 1):
                workload = 0
                
                for other_task_idx, other_task in enumerate(tasks):
                    if other_task_idx != task_idx:
                        T_j = other_task["period"]
                        C_j = other_task["execution_time"]
                        D_j = T_j-other_task["diff"]
                        
                        workload += min(
                            math.ceil(t / T_j),
                            1 + math.floor((a + D_i - D_j) / T_j)
                        ) * C_j
                
                # Task i의 워크로드 계산
                workload += delta_i(a, t, T_i) * C_i
                
            # 데드라인 미스 발생 여부 판단
            # print(workload, a+D_i)
            if workload > a+D_i:
                print(task)
                print(a)
                missed_deadline_tasks.append((task, a))
                break        
    return missed_deadline_tasks

def visualize_schedule(tasks, max_time):
    timeline = []  # 스케줄 타임라인 저장
    time = 0       # 현재 시간
    task_colors = {}  # 각 태스크의 색상 저장
    task_indices = {task["index"]: idx for idx, task in enumerate(tasks)}  # 태스크의 인덱스 저장
    original_tasks = {task["index"]: (task["period"], task["execution_time"], task["diff"]) for task in tasks}  # 주기와 데드라인 저장

    # 색상을 고유하게 지정하기 위한 기본 색상 리스트
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']

    while time <= max_time:
        if not tasks:  # 태스크가 모두 완료되면 종료
            break

        # 현재 시간에서 각 태스크의 다음 데드라인 계산 (EDF)
        deadlines = [(task["index"], (time // task["period"] + 1) * task["period"]) for task in tasks if time >= task.get("next_activation", 0)]
        if not deadlines:  # 실행할 태스크가 없으면 시간만 증가
            time += 1
            continue

        deadlines.sort(key=lambda x: x[1])  # 데드라인 기준으로 정렬

        for task in tasks:
            if task["index"] == deadlines[0][0]:
                timeline.append((task["index"], time))  # 태스크 인덱스와 시간을 함께 저장
                time += 1
                task["execution_time"] -= 1

                if task["execution_time"] <= 0:
                    # 실행이 끝난 태스크는 다음 주기까지 기다림
                    task["execution_time"] = original_tasks[task["index"]][1]
                    task["next_activation"] = (time // task["period"] + 1) * task["period"]  # 다음 주기 시작 시간 설정
                break
        else:
            # 태스크가 모두 완료된 경우에도 시간은 계속 증가하도록 함
            time += 1

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 5))

    for task_id, start_time in timeline:
        if task_id not in task_colors:
            task_colors[task_id] = colors[task_id % len(colors)]  # 태스크별 고유 색상 지정
        ax.broken_barh([(start_time, 1)], (task_indices[task_id] * 10, 9), facecolors=task_colors[task_id])

    # 데드라인 및 주기 정보 표시
    for task, (period, execution_time, diff) in original_tasks.items():
        ax.annotate(f'Period: {period}, Deadline: {period - diff}', (max_time + 1, task_indices[task] * 10), xycoords='data')

    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_title('EDF Scheduling Visualization')
    ax.set_xticks(range(0, max_time + 1, max(1, max_time//10)))
    ax.set_yticks([i * 10 + 4.5 for i in range(len(task_indices))])
    ax.set_yticklabels([f'Task {i}' for i in task_indices])
    ax.grid(True)

    plt.show()

# 실행
def main(config_file):
    config = load_config(config_file)
    
    num_tasks = config['num_tasks']
    num_C_tasks = config['num_C_tasks']
    period_range = config['period_range']
    execution_time_range = config['execution_time_range']

    # 랜덤 태스크 셋 생성
    tasks = generate_random_task_set(num_tasks, num_C_tasks, period_range, execution_time_range)
    # tasks= [{'index': 0, 'period': 80, 'execution_time': 13, 'diff': 5}, {'index': 1, 'period': 93, 'execution_time': 6, 'diff': 5}, {'index': 2, 'period': 99, 'execution_time': 7, 'diff': 5}, {'index': 3, 'period': 78, 'execution_time': 7, 'diff': 5}, {'index': 4, 'period': 100, 'execution_time': 7, 'diff': 5}, {'index': 5, 'period': 85, 'execution_time': 7, 'diff': 5}, {'index': 6, 'period': 78, 'execution_time': 8, 'diff': 5}, {'index': 7, 'period': 76, 'execution_time': 9, 'diff': 5}, {'index': 8, 'period': 77, 'execution_time': 9, 'diff': 5}, {'index': 9, 'period': 80, 'execution_time': 9, 'diff': 5}]
    # # 태스크 정보 출력
    for i, task in enumerate(tasks):
        print(f"Task {i+1} - Period: {task['period']}, Execution Time: {task['execution_time']}")
    
    # Max Busy Period 계산
    busy_period = calculate_busy_period(tasks)
    print(f"Calculated Maximum Busy Period: {busy_period}")

    visualize_schedule(tasks, min(busy_period, 10*tasks[0]['period']))

    missed_deadline_tasks=check_deadline_miss(tasks, busy_period)
    if missed_deadline_tasks==[]:
        print("Successed deadline check")
    else:
        print("Fail!")
        print(missed_deadline_tasks)

if __name__ == "__main__":
    # config.json 파일 경로
    config_file = os.path.join(os.path.dirname(__file__), '..', 'cfg', 'config_hard.json')
    main(config_file)

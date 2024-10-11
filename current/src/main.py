import json
import random
import os
import math
import matplotlib.pyplot as plt
import copy

# JSON 파일에서 태스크 범위 정보 불러오기
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

# 랜덤 태스크 셋 생성 함수
def generate_random_task_set(num_tasks, period_range, exec_time_range, critical_p):
    tasks = []
    for i in range(num_tasks):
        period = random.randint(period_range[0], period_range[1])
        execution_time = random.randint(exec_time_range[0], exec_time_range[1])
        critical = random.random() < critical_p
        task={
            "index": i,
            "period": period,
            "execution_time": execution_time,
            "deadline" : period,
            "critical" : critical
        }
        tasks.append(task)
    return tasks

def find_longest_critical_task_e(tasks):
    critical_tasks = [task for task in tasks if task["critical"]]
    if not critical_tasks:
        return 0
    longest_task = max(critical_tasks, key=lambda task: task["execution_time"])
    return longest_task["execution_time"]

# Busy Period 계산 함수 (EDF 기준)
def L_max(tasks):
    # longest_c_e=find_longest_critical_task_e(tasks)
    longest_c_e=0
    busy_period = sum(task["execution_time"] for task in tasks)+longest_c_e
    while(True):
        workload = sum(((busy_period//task["period"] +1) * task["execution_time"]) for task in tasks)+longest_c_e
        if workload == busy_period:
            break
        busy_period = workload
    print("busy_period", busy_period)
    return 30
    return busy_period
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
def L_i(tasks, i, phi):
    L_prev=-1
    L_curr=W_i_all(tasks, i, phi, 1)
    while(L_prev!=L_curr):
        L_prev=L_curr
        L_curr=W_i_all(tasks, i, phi, L_prev)
    return L_curr

        # if rerun_task_idx == task_idx:
        #     task["deadline"]=task["period"]-task["execution_time"]

# 데드라인 미스 체크
def check_deadline_miss(tasks, busy_period, rerun_idx):
    missed_deadline_tasks = []
    rerun_e = 0

    for task in tasks:
        if task['index'] == rerun_idx:
            rerun_e = task["execution_time"]
            break
    
    for task_idx, task in enumerate(tasks):
        for phi in range(busy_period + 1):
            workload=L_i(tasks, task_idx, phi)
                
            # 데드라인 미스 발생 여부 판단
            # print(workload, phi+task["deadline"])
            if workload+rerun_e > phi+task["deadline"]:
                print(task)
                print(phi)
                missed_deadline_tasks.append((task, phi))
                break        
    return missed_deadline_tasks

def calculate_max_tasks(tasks, rerun_idx): # tasks 받아서 크리티컬 먼저 넣고 논크리티컬 넣으면서 몇개까지 들어가나 세서 반환
    core_U=[0,0,0,0]
    core_assignments = [[],[],[],[]]
    critical_tasks = [task for task in tasks if task["critical"]]
    non_critical_tasks = [task for task in tasks if not task["critical"]]

    for task_idx, task in enumerate(critical_tasks):
        task_U = task["execution_time"] / task["period"]
        worst_core = core_U.index(min(core_U))
        core_assignments[worst_core].append(task)
        core_U[worst_core] += task_U
        if core_U[worst_core]>1:
            print("U already exceeded 1 in critical tasks")
            return -1
        
    for task_idx, task in enumerate(non_critical_tasks):
        task_U = task["execution_time"] / task["period"]
        worst_core = core_U.index(min(core_U))
        core_assignments[worst_core].append(task)
        core_U[worst_core] += task_U
        if core_U[worst_core]>1:
            print("U exceeded 1")
            return -1
        busy_period=L_max(core_assignments[worst_core])
        # print("busy period: ", busy_period)
        missed_deadline_tasks=check_deadline_miss(core_assignments[worst_core], busy_period, rerun_idx)
        if missed_deadline_tasks!=[]:
            print("Schedulability test fail! escape")
            print("U:", core_U)
            return task_idx
    return 0

def calculate_max_tasks_default(tasks):
    for i in range(len(tasks)):
        print("Task", i+1, "start")
        
        # rerun X
        result=calculate_max_tasks(tasks[:i+1], -1)
        if result==0:
            pass
        elif result==-1:
            print("Ubreak, Success until : ", i)
            break
        else:
            print("Success until : ", i)
            break

        # rerun O
        critical_tasks = [task for task in tasks[:i+1] if task["critical"]]
        for c_task in critical_tasks:
            rerun_idx=c_task["index"]

            result=calculate_max_tasks(tasks[:i+1], rerun_idx)
            if result==0:
                pass
            elif result==-1:
                print("Ubreak, Success until : ", result)
                return
            else:
                print("Our break, Success until : ", result)
                return

def visualize_schedule(tasks, max_time):
    timeline = []  # 스케줄 타임라인 저장
    time = 0       # 현재 시간
    task_colors = {}  # 각 태스크의 색상 저장
    task_indices = {task["index"]: idx for idx, task in enumerate(tasks)}  # 태스크의 인덱스 저장
    original_tasks = {task["index"]: (task["period"], task["execution_time"], task["deadline"]) for task in tasks}  # 주기와 데드라인 저장

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
    for task, (period, execution_time, deadline) in original_tasks.items():
        ax.annotate(f'Period: {period}, Deadline: {deadline}', (max_time + 1, task_indices[task] * 10), xycoords='data')

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
    period_range = config['period_range']
    execution_time_range = config['execution_time_range']

    # 랜덤 태스크 셋 생성
    tasks = generate_random_task_set(num_tasks, period_range, execution_time_range, 0.2)

    # for i, task in enumerate(tasks):
    #     print(f"Task {i+1} - Period: {task['period']}, Execution Time: {task['execution_time']}, Deadline: {task['deadline']}, Critical: {task['critical']}")

    calculate_max_tasks_default(tasks)
    
    # visualize_schedule(tasks, min(busy_period, 10*tasks[0]['period']))


if __name__ == "__main__":


    # config.json 파일 경로
    config_file = os.path.join(os.path.dirname(__file__), '..', 'cfg', 'config_hard.json')
    main(config_file)

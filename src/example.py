import numpy as np
import matplotlib.pyplot as plt
import math

# 태스크 구조를 위한 클래스 정의
class Task:
    def __init__(self, period, execution_time, criticality):
        self.period = period
        self.execution_time = execution_time
        self.criticality = criticality

    def __str__(self):
        return f"Task(period={self.period}, execution_time={self.execution_time}, criticality={self.criticality})"

def generate_random_periods(n, lower_bound=2, upper_bound=20, scale=25):
    periods = []
    while len(periods) < n:
        period = np.random.exponential(scale=scale)
        if lower_bound <= period <= upper_bound:
            periods.append(period)
    return np.array(periods)

# 태스크 생성 함수 (랜덤 태스크 생성)
def generate_random_tasks(n=20):
    tasks = []
    total_utilization = 0
    max_utilization_per_task = 1 / n

    # 지수분포로 Period 생성 (작은 값이 많음)
    periods = generate_random_periods(n, lower_bound=2, upper_bound=20, scale=25)
    periods = np.round(periods)
    
    # 각 태스크에 대해 Execution Time과 Criticality 설정
    for period in periods:
        criticality = np.random.choice([True, False])  # Criticality 랜덤 설정
        execution_time = np.random.uniform(1, max_utilization_per_task * period)  # 정수로 제한하고, 최소값 1로 설정
        total_utilization += execution_time / period
        
        tasks.append(Task(period=int(period), execution_time=execution_time, criticality=criticality))

    # 모든 태스크의 e/p 비율의 합이 1을 넘지 않도록 보정
    # if total_utilization >= 1:
    #     scaling_factor = 1 / total_utilization
    #     for task in tasks:
    #         task.execution_time *= scaling_factor

    return tasks

# Demand Bound Function 계산 함수
def dbf(task, time):
    return max(0, (math.floor((time - task.period) / task.period) + 1) * task.execution_time)

# 여러 태스크에 대한 DBF를 계산하고, 시각화하는 함수
def visualize_dbf(tasks, time_range=100, file_name='example.pdf'):
    time_values = np.arange(1, time_range + 1)

    # Criticality에 따라 각각 DBF 값을 계산
    critical_true_demand = np.zeros(time_range)
    critical_false_demand = np.zeros(time_range)
    cumulative_critical_execution = np.zeros(time_range)  # Rerun 데이터를 위한 배열
    
    for task in tasks:
        for t in time_values:
            if task.criticality:  # Criticality가 True인 태스크의 DBF
                critical_true_demand[t-1] += dbf(task, t)
                
                # Rerun 계산: Period가 지난 Critical Task들의 실행 시간
                if t >= task.period:
                    cumulative_critical_execution[t-1] += task.execution_time
            else:  # Criticality가 False인 태스크의 DBF
                critical_false_demand[t-1] += dbf(task, t)
    
    total_demand = critical_true_demand + critical_false_demand
    total_with_rerun = total_demand + cumulative_critical_execution  # Total DBF + Rerun 합

    # y축 범위는 통일하여 설정
    ymax = max(np.max(total_with_rerun), np.max(cumulative_critical_execution)) * 1.1

    plt.figure(figsize=(12, 12))

    # 1. "모든" 태스크의 dbf합 + Rerun + 합산된 그래프
    plt.subplot(5, 1, 1)
    plt.step(time_values, total_demand, label="Total DBF", color='red', where='post')
    plt.step(time_values, cumulative_critical_execution, label="Rerun", color='purple', where='post')
    plt.step(time_values, total_with_rerun, label="Total DBF + Rerun", color='black', where='post')
    plt.title("Total DBF for All Tasks + Rerun + Combined")
    plt.xlabel("Time")
    plt.ylabel("DBF")
    plt.ylim(0, ymax)
    plt.grid(True)
    plt.legend()

    # 2. Critical 태스크의 dbf합 + Non-Critical 태스크의 dbf합 + Rerun + 합산된 그래프
    total_critical_noncritical_rerun = critical_true_demand + critical_false_demand + cumulative_critical_execution
    plt.subplot(5, 1, 2)
    plt.step(time_values, critical_true_demand, label="Critical DBF", color='blue', where='post')
    plt.step(time_values, critical_false_demand, label="Non-Critical DBF", color='green', where='post')
    plt.step(time_values, cumulative_critical_execution, label="Rerun", color='purple', where='post')
    plt.step(time_values, total_critical_noncritical_rerun, label="Critical + Non-Critical + Rerun", color='black', where='post')
    plt.title("Critical + Non-Critical DBF + Rerun + Combined")
    plt.xlabel("Time")
    plt.ylabel("DBF")
    plt.ylim(0, ymax)
    plt.grid(True)
    plt.legend()

    # 3. Critical 태스크의 dbf합 + Non-Critical 태스크의 dbf합 + 합산된 그래프
    total_critical_noncritical = critical_true_demand + critical_false_demand
    plt.subplot(5, 1, 3)
    plt.step(time_values, critical_true_demand, label="Critical DBF", color='blue', where='post')
    plt.step(time_values, critical_false_demand, label="Non-Critical DBF", color='green', where='post')
    plt.step(time_values, total_critical_noncritical, label="Critical + Non-Critical DBF", color='black', where='post')
    plt.title("Critical + Non-Critical DBF + Combined")
    plt.xlabel("Time")
    plt.ylabel("DBF")
    plt.ylim(0, ymax)
    plt.grid(True)
    plt.legend()

    # 4. Critical 태스크의 dbf합 + Rerun + 합산된 그래프
    total_critical_rerun = critical_true_demand + cumulative_critical_execution
    plt.subplot(5, 1, 4)
    plt.step(time_values, critical_true_demand, label="Critical DBF", color='blue', where='post')
    plt.step(time_values, cumulative_critical_execution, label="Rerun", color='purple', where='post')
    plt.step(time_values, total_critical_rerun, label="Critical DBF + Rerun", color='black', where='post')
    plt.title("Critical DBF + Rerun + Combined")
    plt.xlabel("Time")
    plt.ylabel("DBF")
    plt.ylim(0, ymax)
    plt.grid(True)
    plt.legend()

    # 5. Non-Critical 태스크의 dbf합 + Rerun (합친 것은 필요 없음)
    plt.subplot(5, 1, 5)
    plt.step(time_values, critical_false_demand, label="Non-Critical DBF", color='green', where='post')
    plt.step(time_values, cumulative_critical_execution, label="Rerun", color='purple', where='post')
    plt.title("Non-Critical DBF + Rerun (No Sum)")
    plt.xlabel("Time")
    plt.ylabel("DBF")
    plt.ylim(0, ymax)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    # 파일로 저장 (png 또는 pdf)
    plt.savefig(file_name, format='pdf')
    plt.close()

# 태스크 갯수 설정
n = 20
# 랜덤 태스크 생성
tasks = generate_random_tasks(n=n)

# 시간 범위 설정 (1000으로 확대)
time_range = 20

# DBF 시각화 호출 (이미지 파일로 저장)
visualize_dbf(tasks, time_range, file_name='example.pdf')
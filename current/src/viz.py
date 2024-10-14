import matplotlib.pyplot as plt


def visualize_task_limit(data, critical_ratio_num, period_range, utilization_range):
    plt.figure(figsize=(8, 6))
    plt.plot([i / critical_ratio_num for i in range(critical_ratio_num + 1)], data[0], 'o-', label='Defualt')
    plt.plot([i / critical_ratio_num for i in range(critical_ratio_num + 1)], data[1], 'o-', label='Binding')
    plt.xlabel('Critical Ratio')
    plt.ylabel('Task Limit')
    plt.title('Task Limit Based on Critical Ratio')
    plt.grid(True)
    plt.legend()
    # 그래프 출력
    # plt.show()
    plt.savefig(f'current/fig/period_{period_range}_util_{utilization_range}.png')
    plt.show()


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
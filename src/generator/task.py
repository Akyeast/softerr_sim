class Task():
    def __init__(self, period, execution, criticality):
        self.period = period
        self.execution = execution
        self.utilization = execution / period
        self.criticality = criticality

    def __str__(self):
        return "Task(period={}, execution={}, criticality={})\n".format(self.period, self.execution, self.criticality)
    
    def __repr__(self):
        return self.__str__()

    def get_task(self, state_num=None):
        if state_num is None:
            critical = max(self.criticality)
        else:
            critical = self.criticality[state_num]

        return (self.period, self.execution, critical)


class TaskSet():
    def __init__(self, tasks):
        self.tasks = tasks

    def append(self, task):
        self.tasks.append(task)
    
    def get_tasks(self, state_num=None) :
        return [task.get_task(state_num) for task in self.tasks]

    def __str__(self):
        return "TaskSet:\n{}".format(self.tasks)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.tasks)
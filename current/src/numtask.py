import partition
import bind

def calculate_max_tasks_default(tasks, core_num): # tasks에서 개수 늘려가면서 넣어보며 몇개까지 들어가나 세서 반환
    for i in range(len(tasks)):
        # print("Task", i+1, "start")
        
        # rerun X
        result=partition.worst_fit(tasks[:i+1], -1, core_num)
        if result==0:
            pass
        else:
            # if result==-1:
            #     print("U break, Success until : ", i)
            # else:
            #     print("Our break, Success until : ", i)
            return i

        # rerun O
        critical_tasks = [task for task in tasks[:i+1] if task["critical"]]
        for c_task in critical_tasks:
            rerun_idx=c_task["index"]

            result=partition.worst_fit(tasks[:i+1], rerun_idx, core_num)
            if result==0:
                pass
            else:
                # if result==-1:
                #     print("U break, Success until : ", i)
                # else:
                #     print("Our break, Success until : ", i)
                return i
            
def calculate_max_tasks_binding(tasks, core_num): # tasks에서 개수 늘려가면서 넣어보며 몇개까지 들어가나 세서 반환
    
    for i in range(len(tasks)):
        critical_tasks = [task for task in tasks[:i+1] if task["critical"]]
        non_critical_tasks = [task for task in tasks[:i+1] if not task["critical"]]

        binded_tasks=bind.bind_nc_tasks(non_critical_tasks)
        
        # rerun X
        result=partition.worst_fit(critical_tasks+binded_tasks, -1, core_num)
        if result==0:
            pass
        else:
            # if result==-1:
            #     print("U break, Success until : ", i)
            # else:
            #     print("Our break, Success until : ", i)
            # print('tasks:', i)
            # print('c:', critical_tasks)
            # print('nc:', non_critical_tasks)
            # print('b:', binded_tasks)
            return i

        # rerun O
        for c_task in critical_tasks:
            rerun_idx=c_task["index"]

            result=partition.worst_fit(critical_tasks+binded_tasks, rerun_idx, core_num)
            if result==0:
                pass
            else:
                # if result==-1:
                #     print("U break, Success until : ", i)
                # else:
                #     print("Our break, Success until : ", i)
                return i
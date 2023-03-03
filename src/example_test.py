from generator.generator import generate_example_taskset
from core.ours import get_num_core_ours

def main():   
    tasks = generate_example_taskset().get_tasks(sort=True, desc=True)
    print(tasks)
    core, prms, mapped_tasks = get_num_core_ours(tasks)
    print('core: ', core)
    print('prms: ', prms)
    print('mapped_tasks: ')
    for i in range(max([t[3] for t in mapped_tasks])+1):
        print(f"core {2*i},{2*i+1}: ", [t[:3] for t in filter(lambda x: x[3]==i, mapped_tasks)])

if __name__ == '__main__':
    main()
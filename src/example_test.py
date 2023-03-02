from generator.generator import generate_example_taskset
from core.ours import get_num_core_ours

def main():   
    tasks = generate_example_taskset().get_tasks(sort=True, desc=True)
    print(tasks)
    core, prms, mapped_tasks = get_num_core_ours(tasks)
    print('core: ', core)
    print('prms: ', prms)
    print('mapped_tasks: ', mapped_tasks)

if __name__ == '__main__':
    main()
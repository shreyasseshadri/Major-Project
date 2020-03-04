import util_extractor as ue
import analyzer as analyzer

# A table with vm_id as key and vm usage list as value. The current usage of VM
vm_table = {}

# Sorted Arrays of all usages each element is a tuple of (value,vm_id)
# mem -  Available free Memory , comp - percentage available , net - Available bandwidth
sorted_usage_list = [[], [], []]
vm_initial_characteristics = {}
vm_queue = {}  # Task Queue for all VMs

chars = ["mem", "comp", "net"]


def index2name(index):
    return chars[index]


def name2index(name):
    return chars.index(name)


def initilise_vm_characteristics():
    pass


def insert_sort(sorted_array, tuple):
    flag = 0
    for ind, elem in enumerate(sorted_array):
        val, _ = elem
        if val >= tuple[0]:
            flag = 1
            break
    if flag == 0:
        sorted_array.append(tuple)
    else:
        sorted_array.insert(ind, tuple)


def update_sorted_lists(mem_usage, comp_usage, network_usage, vm_id):
    # Assumes that three lists are sorted
    # Updates the sorted list for each characteristic

    insert_sort(sorted_usage_list[0], (mem_usage, vm_id))
    insert_sort(sorted_usage_list[2],
                (100000 - network_usage, vm_id))  # Bandwidth assumed to be 100KB/s
    insert_sort(sorted_usage_list[1], (100-comp_usage, vm_id))


def insert_new_vm(util_file):
    # Inserts a new VM into Vm table, updates sorted lists

    mem_usage, comp_usage, network_usage, vm_id = ue.read_vm_characteristics(
        util_file)
    vm_queue[vm_id] = []
    print("VM ID: ",vm_id,"Memory Usage: ",mem_usage,"Comute Usage: ",comp_usage,"Netork Usage: ",network_usage)
    # vm_table[vm_id] = [mem_usage, comp_usage, network_usage]
    update_sorted_lists(mem_usage, comp_usage, network_usage, vm_id)


def update_vm(vm_id, usage_list):
    # Updates usage list of already present VMs

    if vm_id in vm_table.keys():
        vm_table[vm_id] = usage_list
    else:
        print('Vm not found in the table')


def get_highest(mem_score, com_score, net_score):
    temp = [(mem_score, "mem"), (com_score, "comp"), (net_score, "net")]
    temp.sort(key=lambda x: x[0], reverse=True)
    return temp[0][1]


def best_vm_for_char(char):
    # for a given charecteristic it gives best VM from sorted VM list

    return sorted_usage_list[name2index(char)][-1][1]


def independent_Task2Vm(task_scores, task_name="default"):
    # Two algorithms in use. One Task2VM allocation independent of the other Tasks, one dependent on other tasks
    # Input is a sorted list each for mem,comp,net of task names in ascending order of scores

    (mem_score, com_score, net_score, _, _, _) = task_scores
    highest_characteristic = get_highest(mem_score, com_score, net_score)
    allocated_vm = best_vm_for_char(highest_characteristic)
    vm_queue[allocated_vm].append(task_name)
    # print("Allocated VM is : ", allocated_vm)


def occurence(array):
    temp_dict = {}
    for ind, task in enumerate(array):
        if task in temp_dict.keys():
            temp_dict[task].append(index2name(ind))
        else:
            temp_dict[task] = [index2name(ind)]
    return temp_dict


def dependent_Task2Vm(task_scores, sorted_task_names):
    # Input is task scores a dict, sorted task names a 2d list.
    index = len(sorted_task_names[0])-1
    unallocated_vms = {k: 0 for k in task_scores}
    while index >= 0 and len(unallocated_vms) > 0:
        temp_array = [a[index] for a in sorted_task_names]
        occurence_dict = occurence(temp_array)
        for k in occurence_dict:
            if k not in unallocated_vms.keys():
                continue
            l = occurence_dict[k]
            if len(l) == 1:
                vm_queue[best_vm_for_char(l[0])].append(k)
                # print("Allocated VM is : ", best_vm_for_char(l[0]))
            else:
                independent_Task2Vm(task_scores[k], k)
            del unallocated_vms[k]
        index -= 1


def poll_vm(vm_id):
    # Supposed to poll and retirieve the util file as of now flask will be used
    pass


def create_sorted_task_names(task_scores):
    # Given a dict of task scores, it gives the sorted_task_name 2d matrix used in dependent task2Vm

    sorted_task_names = []
    to_sort = [[], [], []]

    for t in task_scores:
        for ind, score in enumerate(task_scores[t][:3]):
            to_sort[ind].append((score, t))

    for l in to_sort:
        sorted_task_names.append([t[1] for t in sorted(l, key=lambda x: x[0])])
    return sorted_task_names


def clear_queue():
    for k in vm_queue:
        vm_queue[k].clear()


if __name__ == "__main__":

    print('Parsing util file')
    insert_new_vm("util0.txt")
    insert_new_vm("util1.txt")
    insert_new_vm("util2.txt")

    print('\n','='*90,'\n')

    print('Sorted List of available resources')
    for i, l in enumerate(sorted_usage_list):
        print(index2name(i)+" : "+str(l))

    print('\n','='*90,'\n')

    print('Testing dependent task2Vm')
    # Testing dependent task2Vm
    independent_Task2Vm(analyzer.analyze(
        file_name='programs/memory.py'), 'memory.py')
    independent_Task2Vm(analyzer.analyze(
        file_name='programs/compute.py'), 'compute.py')
    independent_Task2Vm(analyzer.analyze(
        file_name='programs/network.py'), 'network.py')

    print(vm_queue)

    print('\n','='*90,'\n')
    clear_queue()

    print('Testing Dependent task2Vm by example 1')
    
    # Testing Dependent task2Vm

    sorted_task_names = [
        ['t1', 't2', 't3'],
        ['t2', 't1', 't3'],
        ['t3', 't2', 't1']
    ]
    task_scores = {
        't1': (0.2, 0.3, 0.5, None, None, None),
        't2': (0.3, 0.2, 0.4, None, None, None),
        't3': (0.5, 0.49, 0.01, None, None, None)
    }

    print(task_scores)
    dependent_Task2Vm(task_scores, sorted_task_names)
    print(vm_queue)

    print('\n','='*90,'\n')
    clear_queue()

    print('Testing Dependent task2Vm by memory.py, compute.py, network.py')

    file_names = ['memory.py', 'compute.py', 'network.py']
    task_scores = {f: analyzer.analyze(
        file_name='programs/'+f) for f in file_names}

    print(task_scores)
    sorted_task_names = create_sorted_task_names(task_scores)

    dependent_Task2Vm(task_scores, sorted_task_names)

    print(vm_queue)

    clear_queue()

    print('\n','='*90,'\n')
    # Another example

    print('Testing Dependent Task2Vm by example 2')
    task_scores = {
        't1': (0.2, 0.3, 0.5, None, None, None),
        't2': (0.3, 0.49, 0.01, None, None, None),
        't3': (0.5, 0.2, 0.3, None, None, None)
    }
    print(task_scores)
    dependent_Task2Vm(task_scores, create_sorted_task_names(task_scores))
    print(vm_queue)

    print('\n','='*90,'\n')

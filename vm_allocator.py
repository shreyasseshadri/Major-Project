import util_extractor as ue
import analyzer as analyzer

# A table with vm_id as key and vm usage list as value. The current usage of VM
vm_table = {}

# Sorted Arrays of all usages each element is a tuple of (value,vm_id)
# comp_usage_list = [(1, '0'), (2, '1'), (3, '2')]
# mem_usage_list = []
# network_usage_list = []

# mem,comp,net
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


# Assumes that three lists are sorted

# Updates the sorted list for each characteristic
def update_sorted_lists(mem_usage, comp_usage, network_usage, vm_id):
    insert_sort(sorted_usage_list[0],
                (vm_initial_characteristics[vm_id][1] - mem_usage, vm_id))
    insert_sort(sorted_usage_list[2],
                (vm_initial_characteristics[vm_id][2] - network_usage, vm_id))
    insert_sort(sorted_usage_list[1], (comp_usage, vm_id))

# Inserts a new VM into Vm table, updates sorted lists


def insert_new_vm(util_file):
    mem_usage, comp_usage, network_usage, vm_id = ue.read_vm_characteristics(
        util_file)
    print(mem_usage, comp_usage, network_usage, vm_id)
    vm_table[vm_id] = [mem_usage, comp_usage, network_usage]
    update_sorted_lists(mem_usage, comp_usage, network_usage, vm_id)

# Updates usage list of already present VMs


def update_vm(vm_id, usage_list):
    if vm_id in vm_table.keys():
        vm_table[vm_id] = usage_list
    else:
        print('Vm not found in the table')


def get_highest(mem_score, com_score, net_score):
    temp = [(mem_score, "mem"), (com_score, "comp"), (net_score, "net")]
    temp.sort(key=lambda x: x[0], reverse=True)
    return temp[0][1]

# Two algorithms in use. One Task2VM allocation independent of the other Tasks, one dependent on other tasks


def independent_Task2Vm(task_scores, task_name="default"):
    (mem_score, com_score, net_score, _, _, _) = task_scores
    highest_characteristic = get_highest(mem_score, com_score, net_score)
    allocated_vm = sorted_usage_list[name2index(highest_characteristic)][-1][1]
    # if highest_characteristic == "mem":
    #     allocated_vm = mem_usage_list[-1][1]
    # elif highest_characteristic == "comp":
    #     allocated_vm = comp_usage_list[-1][1]
    # elif highest_characteristic == "net":
    #     allocated_vm = network_usage_list[-1][1]
    vm_queue[allocated_vm].append(task_name)
    print("Allocated VM is : ", allocated_vm)

# Input is a sorted list each for mem,comp,net of task names in ascending order of scores


def occurence(array):
    temp_dict = {}
    for ind, task in enumerate(array):
        if task in temp_dict.keys():
            temp_dict[task].append(index2name(ind))
        else:
            temp_dict[task] = [index2name(ind)]
    return temp_dict

# for a given charecteristic it gives best VM from sorted VM list


def best_vm_for_char(char):
    return sorted_usage_list[index2name(char)][-1][0]
# Input is task scores a dict, sorted task names a 2d list.


def dependent_Task2Vm(task_scores, sorted_task_names):
    index = len(sorted_task_names[0])
    allocated_vms = {k: 0 for k, v in task_scores}
    while index >= 0 and len(allocated_vms) > 0:
        temp_array = [a[index] for a in sorted_task_names]
        occurence_dict = occurence(temp_array)
        for k, l in occurence_dict:
            if len(l) == 1:
                vm_queue[best_vm_for_char(l[0])].append(k)
            else:
                independent_Task2Vm(task_scores, k)
            del allocated_vms[k]
        index -= 1


    # task_scores is a tuple (mem_score, com_score, net_score, mem_tokens, com_tokens, net_tokens)
tasks_scores = analyzer.analyze(file_name='programs/compute.py')
# insert_new_vm('util0.txt') # This will be asked by VM allocator algorithm to all VMs on allocating new VM.

import util_extractor as ue
import analyzer as analyzer

# A table with vm_id as key and vm usage list as value. The current usage of VM
vm_table = {}

# Sorted Arrays of all usages each element is a tuple of (value,vm_id)
comp_usage_list = [(1, '0'), (2, '1'), (3, '2')]
mem_usage_list = []
network_usage_list = []

vm_initial_characteristics = {}

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


# insert_sort(comp_usage_list, (0, 'new'))
# print(comp_usage_list)
# Assumes that three lists are sorted

# Updates the sorted list for each characteristic
def update_sorted_lists(mem_usage, comp_usage, network_usage, vm_id):
    insert_sort(mem_usage_list, (mem_usage, vm_id))
    insert_sort(network_usage_list, (network_usage, vm_id))
    insert_sort(comp_usage_list, (comp_usage, vm_id))

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


# Two algorithms in use. One Task2VM allocation independent of the other Tasks, one dependent on other tasks
def get_highest(mem_score, com_score, net_score):
    temp = [(mem_score,"mem"),(com_score,"comp"),(net_score,"net")]
    temp.sort(key=lambda x: x[0],reverse=True)
    return temp[0][1]

def independent_Task2Vm(task_scores):
    (mem_score, com_score, net_score, _ , _,_ ) = task_scores
    highest_characteristic = get_highest(mem_score,com_score,net_score)
    allocated_vm = None
    if highest_characteristic == "mem":
        pass
    elif highest_characteristic == "comp":
        pass
    elif highest_characteristic == "net":
        pass
    print("Allocated VM is : ",allocated_vm)



def dependent_Task2Vm(tasks_scores):
    pass


# task_scores is a tuple (mem_score, com_score, net_score, mem_tokens, com_tokens, net_tokens)
tasks_scores = analyzer.analyze(file_name='programs/compute.py')
# insert_new_vm('util0.txt') # This will be asked by VM allocator algorithm to all VMs on allocating new VM.

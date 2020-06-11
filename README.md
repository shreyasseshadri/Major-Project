<h1> <center>Task Scheduling in cloud environment </center></h1>
Classifying the task based based  on the requirements and prioritizing task executions on VMs based on the their current workload.

## Instructions to run

### Lexical Anaysis
- A lexical analyzer `analyzer.py` is used for classifing the task into n categories and a list of scores is generated for each categories.

- To run the analyzer use `python3 analyzer.py`. The main function analyze's syntax is as follows.

    ```
    analyze(directory=False, directory_name=None, output=False, 
    output_file_name=None, file_name=None)
    ```
    Arguements:

    `directory (boolean)` : If set to `True` it analyzes all the programs in the directory, `directory_name` argument must be given

    `directory_name (string)` : If `directory` is set to `True`, the name of the directory must be given.

    `output (boolean)` : Set to `True` if output is needed, `False` otherwise.

    `output_file_name (string)` : File name of output if output flag is set to True.

    `file_name (string)` : If `directory` is set to `False`, then a file name must be given. 

- The programs outputs two lists of scores. One is a task specific score for different resources such as (memory, compute, network, etc..), and the other is a resource specific score comparing all programs (if multiple exits).

### VM utilisation
The utilsation of each resources in a VM running a task is obtained and is used in the schediling of task. A live state of resources are used for scheduling.

- A bash script `utilization.sh` is used to get the current resource usage of the VM running the program. A `vm_id` is assigned to each VM and in this case is the Machine's username obtained using `whoami` command. 
    - `top` command is used to get the CPU and memory usage.
    - `bwm-ng` command is used to get the network usage.
- The output of the previous script is parsed with `util_extractor.py`. `read_vm_characteristics` is exposed by this file and is used to parse the output from the previous script, given the output file name as input.

### Task Allocation

This task allocationn requires a live table of resource usage(or available free resource) of each VMs to which tasks needed to be scheduled. It also requires each task to be analyzed using the lexical analyzer as mentioned before

`vm_allocator.py` is used for task allocation to VMs. This program exposes the following main functions

- `insert_new_vm` : Given a utilization file as the one generated by `utilization.sh` it extracts the usage characteristics and inserts it into the `vm_table` using `update_sorted_lists`
- `update_sorted_lists` : This is used internally by the above function to sort the VMs based on each characteristic and is inserted.
-  `update_vm` : This is used to update the usage characteristic of an existing VM in the VM table.
-  `independent_Task2Vm` : This function schedules a single task and needs two inputs one is a list of `task_scores` for the task, and the `task_name` to be put in queue.
- `dependent_Task2Vm` : This functions allocates VMs for multiple tasks. It requires two inputs. `task_scores` list for all the tasks and a `sorted_task_names` which is 2d list that is generated by the function given below.
- `create_sorted_task_names` : This function given a 2d list of task scores  for multiple tasks, genrates a sorted list of task names to be used in `dependent_Task2Vm`.


### Other files
- Sample Programs have been given under `/programs` directory.
- Three files `util0.txt`, `util1.txt`, `util2.txt` have been generated.

## VM Setup

Each VM should have its util file after generating it from the VM_utilisation part. 

The `server.py` file will be running on the master VM, (the VM that runs the allocation algorithm). 

Now from each VM run the following command
```
curl -i -X POST http://<master_ip_address>:5000/util --data-binary "@util_file.txt"

```
> NOTE: '@' in the above command is neccessary.
### Team
```
Shreyas Seshadri - 16IT135 
Akhil N kashyap  - 16IT104 
GS Dhanush       - 16IT219 
```
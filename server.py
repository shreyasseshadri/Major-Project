from flask import Flask, request
import util_extractor as ue
import tempfile
import os
import vm_allocator as allocator
import analyzer
app = Flask(__name__)
total_VMs = 0
import threading

@app.route('/util', methods=['POST'])
def handle_util_submit():
	if request.method == "POST":
		file_data = list(request.form.to_dict().keys())[0]

	with open('temp.txt', 'w') as f:
		f.write(file_data)

	allocator.insert_new_vm('temp.txt')
	os.remove('temp.txt')
	return 'Done'


if __name__ == "__main__":
	t1 = threading.Thread(target=app.run)
	t1.start()
	try:
		while True:
			if(len(allocator.sorted_usage_list[0]) == 3):
				print('\n','='*90,'\n')
				print('Sorted List of available resources')
				for i, l in enumerate(allocator.sorted_usage_list):
					print(allocator.index2name(i)+" : "+str(l))
				print('Testing independent task2Vm')

				# Testing dependent task2Vm
				allocator.independent_Task2Vm(analyzer.analyze(
					file_name='programs/memory.py'), 'memory.py')
				allocator.independent_Task2Vm(analyzer.analyze(
					file_name='programs/compute.py'), 'compute.py')
				allocator.independent_Task2Vm(analyzer.analyze(
					file_name='programs/network.py'), 'network.py')

				# print(allocator.vm_queue)
				allocator.print_queue()
				print('\n','='*90,'\n')
				allocator.clear_queue()
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

				# print(task_scores)
				allocator.print_task_scores(task_scores)
				allocator.dependent_Task2Vm(task_scores, sorted_task_names)
				# print(allocator.vm_queue)
				allocator.print_queue()

				print('\n','='*90,'\n')
				allocator.clear_queue()

				print('Testing Dependent task2Vm by memory.py, compute.py, network.py')

				file_names = ['memory.py', 'compute.py', 'network.py']
				task_scores = {f: analyzer.analyze(
					file_name='programs/'+f) for f in file_names}

				# print(task_scores)
				allocator.print_task_scores(task_scores)
				sorted_task_names = allocator.create_sorted_task_names(task_scores)

				allocator.dependent_Task2Vm(task_scores, sorted_task_names)

				# print(allocator.vm_queue)
				allocator.print_queue()

				allocator.clear_queue()

				print('\n','='*90,'\n')
				# Another example

				print('Testing Dependent Task2Vm by example 2')
				task_scores = {
					't1': (0.2, 0.3, 0.5, None, None, None),
					't2': (0.3, 0.49, 0.01, None, None, None),
					't3': (0.5, 0.2, 0.3, None, None, None)
				}
				# print(task_scores)
				allocator.print_task_scores(task_scores)
				allocator.dependent_Task2Vm(task_scores, allocator.create_sorted_task_names(task_scores))
				# print(allocator.vm_queue)
				allocator.print_queue()

				print('\n','='*90,'\n')
				t1.join()
				exit()
				break
	except KeyboardInterrupt:
		exit()

import Queue
from collections import defaultdict
from systemcall import SystemCall


class Scheduler:
	def __init__(self):
		self.tasks= Queue.Queue()
		self.id_2_task = {}
		self.id_2_exitwating_task = defaultdict(list)
		

	def loop(self):
		while not self.tasks.empty():
			task = self.tasks.get()
			print "switch to ", task.id
			try:
				result = task.run()
				if isinstance(result, SystemCall):
					result.scheduler = self
					result.task = task
					result.handle()
					continue
				
				self.schedule_task(task)
			except StopIteration:
				self.exit_task(task.id)
	
	def get_task(self, task_id):
		return self.id_2_task.get(task_id, None)

	def new_task(self, target):
		task = Task(target)
		self.id_2_task[task.id] = task
		print self.id_2_task
		self.schedule_task(task)
		return task

	def schedule_task(self, task):
		#import traceback
		#traceback.print_stack()
		#print "schedule task ", task.id
		self.tasks.put(task)
	
	def exit_task(self, task_id):
		print "task ", task_id, " exit"
		print self.id_2_task
		self.id_2_task.pop(task_id)

		waiting_tasks = self.id_2_exitwating_task.pop(task_id, [])
		for task in waiting_tasks:
			self.schedule_task(task)
	
	def wait_for_exit(self, task, wait_task_id):
		if wait_task_id not in self.id_2_task:
			return False

		self.id_2_exitwating_task[wait_task_id].append(task)
		return True


class Task(object):
	ID = 0
	def __init__(self, target):
		Task.ID += 1
		self.id = Task.ID
		self.target = target 
		self.send_val = None

	def run(self):
		return self.target.send(self.send_val)


		


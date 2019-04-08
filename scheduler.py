import Queue
import select
from collections import defaultdict
from systemcall import SystemCall


class Scheduler:
	def __init__(self):
		self.tasks= Queue.Queue()
		self.id_2_task = {}
		self.id_2_exitwating_task = defaultdict(list)

		self.fd_2_reading_tasks = {}
		self.fd_2_writing_tasks = {}
		
		self.id_2_fds = {}
		self.new_task(self.io_task())

	def io_loop(self, timeout):
		if not self.fd_2_reading_tasks and not self.fd_2_writing_tasks:
			return

		r, w, e = select.select(self.fd_2_reading_tasks, self.fd_2_writing_tasks, [], timeout)
		for fd in r:
			self.schedule_task(self.fd_2_reading_tasks.pop(fd))

		for fd in w:
			self.schedule_task(self.fd_2_writing_tasks.pop(fd))

	def io_task(self):
		while True:
			if not self.tasks:
				self.io_loop(None)
			else:
				self.io_loop(0)
			
			yield

	def loop(self):
		while not self.tasks.empty():
			task = self.tasks.get()
			if task.id != 1:
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
		
		fd = self.id_2_fds.pop(task_id, None)
		if fd:
			self.fd_2_reading_tasks.pop(fd, None)
			self.fd_2_writing_tasks.pop(fd, None)

		waiting_tasks = self.id_2_exitwating_task.pop(task_id, [])
		for task in waiting_tasks:
			self.schedule_task(task)
	
	def wait_for_exit(self, task, wait_task_id):
		if wait_task_id not in self.id_2_task:
			return False

		self.id_2_exitwating_task[wait_task_id].append(task)
		return True

	def add_read_wait_task(self, fd, task):
		self.fd_2_reading_tasks[fd] = task
		self.id_2_fds[task.id] = fd

	def add_write_wait_task(self, fd, task):
		self.fd_2_writing_tasks[fd] = task
		self.id_2_fds[task.id] = fd


class Task(object):
	ID = 0
	def __init__(self, target):
		Task.ID += 1
		self.id = Task.ID
		self.target = target 
		self.send_val = None

	def run(self):
		return self.target.send(self.send_val)


		


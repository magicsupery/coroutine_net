class SystemCall(object):
	def __init__(self):
		self.task = None
		self.scheduler = None
		return

	def handle(self):
		pass

class NewTaskSC(SystemCall):
	def __init__(self, target):
		super(NewTaskSC, self).__init__()
		self.target = target
		return

	def handle(self):
		# add new task
		task = self.scheduler.new_task(self.target)

		# continue the task
		self.task.send_val = task.id
		self.scheduler.schedule_task(self.task)


class KillTaskSC(SystemCall):
	def __init__(self, task_id):
		super(KillTaskSC, self).__init__()
		self.task_id = task_id

	def handle(self):
		task = self.scheduler.get_task(self.task_id)
		if task:
			task.target.close()
			self.task.send_val = True
		else:
			self.task.send_val = False

		self.scheduler.schedule_task(self.task)

class ExitWaitTaskSC(SystemCall):
	def __init__(self, target):
		super(ExitWaitTaskSC, self).__init__()
		self.target = target

	def handle(self):
		# add new task
		new_task = self.scheduler.new_task(self.target)

		# add current_task to wait
		self.scheduler.wait_for_exit(self.task, new_task.id)
		return

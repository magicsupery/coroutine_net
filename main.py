from scheduler import Scheduler
from systemcall import *


def task1():
	print "do tasking 0"
	yield

	print "do tasking 1"

	yield

	print "do tasking end"



def test():
	task_id = yield NewTaskSC(task1())
	print "generate a new task ", task_id

	ret = yield KillTaskSC(task_id)
	print "kill task ", task_id, " ret ", ret

	yield ExitWaitTaskSC(task1())
	print "generate task done"


s = Scheduler()
s.new_task(test())
s.loop()

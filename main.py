from scheduler import Scheduler
from systemcall import *
from net import Server


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


def close_client(client):
	client.close()
	print "close client ", client
	yield

def handle_client(client, addr):
	print "get connection from ", addr, client

	yield ReadWaitSC(client.fileno())
	c = client.recv(1024)
	print "recv data is ", c

	yield WriteWaitSC(client.fileno())
	client.send(c)
	
	print "send data is ", c
	yield ExitWaitTaskSC(close_client(client))
	print "handle_client done"

s = Scheduler()
server = Server("localhost", 1234, handle_client)
s.new_task(server.start())
s.loop()

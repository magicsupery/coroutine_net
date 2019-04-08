import socket
from systemcall import *

class Server(object):
	def __init__(self, ip, port, handle_func):
		self.ip = ip
		self.port = port
		self.handle_func= handle_func 

	
	def start(self):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((self.ip, self.port))
			s.listen(10)
			while True:
				yield ReadWaitSC(s.fileno())
				conn, addr = s.accept()
				yield NewTaskSC(self.handle_func(conn, addr))


# -*- coding: utf-8 -*-

import socket
from threading import Thread

from UDP_Pull import *
from UDP_Push import *

##############
# SOCKET SERVER UDP
##############
class SocketServer_UDP:
	
	def __init__(self,video_info,type_socket):
		self.video_info = video_info
		self.type_socket = type_socket

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind((video_info.adress, int(video_info.port)))
		self.thread_read = Thread(target = self.handle_read)
		self.thread_read.daemon = True
		self.thread_read.start()

		if self.type_socket == "PUSH":
			self.objet = UDP_Push(self)
		elif self.type_socket == "PULL":
			self.objet = UDP_Pull(self)
	

	def handle_read(self):
		while True:
			data, host_client = self.sock.recvfrom(1024)
			#print data.replace('\r','\\r').replace('\n','\\n')
			self.objet.receiveLine(data,host_client)

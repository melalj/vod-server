# -*- coding: utf-8 -*-
import socket
from threading import Thread

from TCP_Pull import *
from TCP_Push import *

##############
# SOCKET SERVER TCP
##############

class SocketServer_TCP:
	def __init__(self,video_info,type_socket='HTTP',sendCatalogue=''):
		self.video_info = video_info
		self.sendCatalogue = sendCatalogue
		self.type_socket = type_socket
		self.clients = {}	
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if type_socket == 'HTTP':
			self.sock.bind(video_info)
		else:
			self.sock.bind((video_info.adress, int(video_info.port)))
		self.sock.listen(5)
		self.thread_accept = Thread(target = self.handle_accept)
		self.thread_accept.daemon = True
		self.thread_accept.start()

	def handle_accept(self):
		while True:
			pair = self.sock.accept()
			if pair is None:
				pass
			else:
				sock, addr = pair
				#print 'Connexion TCP d\'un client : %s' % repr(addr)
				self.host_client = addr;
				self.sock_client = sock;
	
				if not addr[0]+":%s" % addr[1] in self.clients:
					if self.type_socket == "PUSH":
						self.clients[addr[0]+":%s" % addr[1]] = TCP_Push(self.video_info)
					elif self.type_socket == "PULL":
						self.clients[addr[0]+":%s" % addr[1]] = TCP_Pull(self.video_info)
	
				thread_read = Thread(target = self.handle_read)
				thread_read.daemon = True
				thread_read.start()
	
	def handle_read(self):
		while True:
			data = self.sock_client.recv(1024)
			if data:
				#print data.replace('\r','\\r').replace('\n','\\n')
				if self.type_socket != "HTTP":
					self.clients[self.host_client[0]+":%s" % self.host_client[1]].receiveLine(data,self.host_client[0])
				else:
					self.sock_client.send(self.sendCatalogue)
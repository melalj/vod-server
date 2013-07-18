# -*- coding: utf-8 -*-
import socket
from Timer import *

class TCP_Push:
	def __init__(self,video_info):
		self.video_info = video_info
		self.reset()

	def reset(self):
		self.current_image_id = 1
		self.sock_client = ''
		self.port_client = ''
		self.streaming = ''

	def nextImage(self):
		# on boucle une fois arrivé à la fin de la vidéo
		if self.current_image_id == (len(self.video_info.images)-1):
			self.current_image_id = 0

		self.current_image_id += 1

	def sendImage(self):
		message = "%s%s%s%s%s" % (self.current_image_id, '\r\n', len(self.video_info.images[self.current_image_id]), '\r\n',  self.video_info.images[self.current_image_id])
		self.sock_client.send(message)
		self.nextImage()
			 
	def receiveLine(self,data,host_client):
		for line in data.split('\r\n'):
			# LISTEN PORT
			if (line.find("LISTEN_PORT") == 0):
				self.port_client = line.split(" ")[1]
	
			# START
			elif (line.find("START") == 0 and self.port_client != ''):
				# On crée la connexion avec le client si elle n'est pas déjà faite
				if self.sock_client == '':
					self.sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.sock_client.connect((host_client, int(self.port_client)))

				if self.streaming == '':
					# On fait une pause de 1/IPS secondes
					attente = 1/float(self.video_info.ips)
					self.streaming = MyTimer(attente, self.sendImage)
				
				self.streaming.start()
	
			# PAUSE
			elif (line.find("PAUSE") == 0):
				self.streaming.stop()

			# END
			elif (line.find("END") == 0):
				self.streaming.stop()
				self.sock_client.close();
				self.reset()
				return

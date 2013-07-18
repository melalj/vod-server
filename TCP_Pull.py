# -*- coding: utf-8 -*-
import socket

class TCP_Pull:
	def __init__(self,video_info):
		self.video_info = video_info
		self.reset()

	def reset(self):
		self.current_image_id = 1
		self.sock_client = ''
		self.port_client = ''

	def nextImage(self):
		# on boucle une fois arrivé à la fin de la vidéo
		if self.current_image_id == (len(self.video_info.images)-1):
			self.current_image_id = 0

		self.current_image_id += 1

	def receiveLine(self,data,host_client):	
		print "receive"	
		for line in data.split('\r\n'):
			# LISTEN PORT
			if (line.find("LISTEN_PORT") == 0):
				self.port_client = line.split(" ")[1]

			# GET IMAGE
			elif (line.find("GET") == 0 and self.port_client != ''):
				image_id = line.split(" ")[1]
				# SI IMAGE_ID == -1 le serveur envoi l'image en cours
				if int(image_id) == -1:
					image_id = self.current_image_id
				# On verifie si on a déjà créé une connexion client avec 
				if self.sock_client == '':
					self.sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					self.sock_client.connect((host_client, int(self.port_client)))

				message = "%s%s%s%s%s" % (image_id, '\r\n', len(self.video_info.images[image_id]), '\r\n',  self.video_info.images[image_id])
				self.sock_client.send(message)

				# On incrémente l'image ID pour le prochain visionnage
				self.nextImage()

			# END
			elif (line.find("END") == 0):
				self.sock_client.close()
				self.reset()
				return

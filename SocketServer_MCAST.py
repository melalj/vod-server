# -*- coding: utf-8 -*-

import os.path, glob,socket
from Timer import *


##############
# SOCKET SERVER MCAST
##############

class SocketServer_MCAST:
	def __init__(self,serveur_info):
		self.addrinfo = socket.getaddrinfo(serveur_info.adress, None)[0]
		self.port = serveur_info.port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.fragmentSize = 512
		self.streaming = ''
		self.ips = serveur_info.ips
		self.current_image_id = 1
		self.images = serveur_info.images
		# On lance le live
		self.sendCurrentImage(self.current_image_id)

	def sendCurrentImage(self, image, fragmentNum = 0):
		tailleImage = len(self.images[image])
		fragmentPos = fragmentNum * self.fragmentSize

		if fragmentPos + self.fragmentSize > tailleImage:
			# on envoie le dernier fragment de l'image et donc la taille du fragment est <= fragmentSize
			finImage = True
			tailleFragment = tailleImage - fragmentPos
		else:
			finImage = False
			tailleFragment = self.fragmentSize

		# génère un message en correspondance avec le format voulu dans le protocole
		message = "%s%s%s%s%s%s%s%s%s" % (image, '\r\n', tailleImage,'\r\n', fragmentPos, '\r\n', tailleFragment, '\r\n', self.images[image][fragmentPos:fragmentPos + tailleFragment])

		self.sock.sendto(message,(self.addrinfo[4][0],int(self.port)))
		fragmentNum += 1 # on passe au fragment suivant

		if not finImage:
			self.sendCurrentImage(image, fragmentNum)
		else:
			# on boucle une fois arrivé à la fin de la vidéo
			if self.current_image_id == (len(self.images)-1):
				self.current_image_id = 0
				
			# On incrémente l'image ID pour le prochain visionnage
			self.current_image_id += 1

			# On arrete le timeout precedent si il existe
			if(self.streaming != ''):
				self.streaming.stop()
			self.streaming = ''

			# On fait une pause de 1/IPS secondes
			attente = 1/float(self.ips)
			self.streaming = MyTimer(attente, self.sendCurrentImage,[self.current_image_id])			
			self.streaming.start()

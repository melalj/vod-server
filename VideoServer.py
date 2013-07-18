# -*- coding: utf-8 -*-
from config import *
from SocketServer_TCP import *
from SocketServer_UDP import *
from SocketServer_MCAST import *

class VideoServer:
	def __init__(self,objet):
		self.id = objet[0]
		self.name = objet[1]
		self.type = objet[2]
		self.adress = objet[3]
		self.port = objet[4]
		self.protocol = objet[5]
		self.ips = objet[6]

		# On charge les images
		self.images = []
		self.images.append("") # car un tableau commence à 0 et la première image à l'index 1

		countImages = len(objet[7])
		for i in range(0, (countImages-1)):
			imagePath = os.path.join(IMAGES_DOSSIER,os.path.normpath(objet[7][i].replace('\\','/'))) 
			if os.path.isfile(imagePath):				
				f = open( imagePath, "rb")
				self.images.append(f.read())
				f.close()
		#print "Chargement de %d images pour %s" % (countImages, self.name)


	def connect(self):
		print ""
		print "Création du serveur video: %s " % (self.id)
		print "Serveur %s : %s:%s" % (self.protocol,self.adress,self.port)

		if self.protocol == "TCP_PULL":
			self.sock = SocketServer_TCP(self,"PULL");

		elif self.protocol == "TCP_PUSH":
			self.sock = SocketServer_TCP(self,"PUSH");

		elif self.protocol == "UDP_PULL":
			self.sock = SocketServer_UDP(self,"PULL");
	
		elif self.protocol == "UDP_PUSH":
			self.sock = SocketServer_UDP(self,"PUSH");

		elif self.protocol == "MCAST_PUSH":
			self.sock = SocketServer_MCAST(self);
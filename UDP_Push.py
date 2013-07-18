# -*- coding: utf-8 -*-
from Timer import *

class UDP_Push:
	def __init__(self,serveur_udp):
		self.serveur_udp = serveur_udp
		self.video_info = serveur_udp.video_info

		# Contrairement à TCP où l'on utilise un mode connecté et donc un objet par client, ici il n'y a qu'un objet pour tous les clients et il doit donc jongler pour savoir si c'est un client qu'il a déjà vu ou pas
		self.clients = {}

	def receiveLine(self,data,host_client):
		host = host_client[0]
		port = host_client[1]

		# Vérification de l 'existance du client
		if not host+":%s" % port in self.clients:
			# On le crée !
			self.clients[host+":%s" % port]= {}
			client = self.clients[host+":%s" % port]
			client["current_image_id"] = 1
			client["streaming"] = ''
		else:
			# on récupère un pointeur sur ce client
			client = self.clients[host+":%s" % port]

		for line in data.split('\r\n'):
			# LISTEN PORT
			if (line.find("LISTEN_PORT") == 0):
				client["port"] = line.split(" ")[1]

			# FRAGMENT SIZE
			elif (line.find("FRAGMENT_SIZE") == 0 and client["port"] != ''):
				client["fragmentSize"]= int(line.split(" ")[1])-30 # On supprime 30 pour prendre en compte le header

			# START
			elif (line.find("START") == 0):
				self.clients[host+":%s" % port] = client
				self.sendCurrentImage(host,port,client["current_image_id"])

			# PAUSE
			elif (line.find("PAUSE") == 0):
				client['streaming'].stop()

			# END
			elif (line.find("END") == 0):
				client['streaming'].stop()
				del self.clients[host+":%s" % port]
				return

	def sendCurrentImage(self, host, port, image, fragmentNum = 0):
		if not host+":%s" % port in self.clients:
			return

		client = self.clients[host+":%s" % port] # récupère un pointeur vers le client
		tailleImage = len(self.video_info.images[image])
		# si fragmentSize = 1024, le fragment 0 est à l'adresse @0, le fragment 1 à @1024, le 2 @2048...
		fragmentPos = fragmentNum * client["fragmentSize"]

		if fragmentPos + client["fragmentSize"] > tailleImage:
			# on envoie le dernier fragment de l'image et donc la taille du fragment est <= fragmentSize
			finImage = True
			tailleFragment = tailleImage - fragmentPos
		else:
			finImage = False
			tailleFragment = client["fragmentSize"]

		# génère un message en correspondance avec le format voulu dans le protocole
		message = "%s%s%s%s%s%s%s%s%s" % (image, '\r\n', tailleImage,'\r\n', fragmentPos, '\r\n', tailleFragment, '\r\n', self.video_info.images[image][fragmentPos:fragmentPos + tailleFragment])

		self.serveur_udp.sock.sendto(message,(host,int(client['port'])))
		fragmentNum += 1 # on passe au fragment suivant

		if not finImage:
			self.sendCurrentImage(host, port, image, fragmentNum)
		else:
			# on boucle une fois arrivé à la fin de la vidéo
			if client["current_image_id"] == (len(self.video_info.images)-1):
				client["current_image_id"] = 0

			# On incrémente l'image ID pour le prochain visionnage
			client["current_image_id"] += 1
			self.clients[host+":%s" % port] = client

			# On arrete le timeout precedent si il existe
			if(client["streaming"] != ''):
				client["streaming"].stop()
			client["streaming"] = ''

			# On fait une pause de 1/IPS secondes
			attente = 1/float(self.video_info.ips)
			client["streaming"] = MyTimer(attente, self.sendCurrentImage,[host,port,client["current_image_id"]])			
			self.clients[host+":%s" % port] = client
			client["streaming"].start()

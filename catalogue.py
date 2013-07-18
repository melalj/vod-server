# -*- coding: utf-8 -*-
from config import *
from VideoServer import *

class Catalogue:
	def __init__(self, chemin_fichier):
		self.videos = []
		self.serveur_AdresseIP = ''
		self.serveur_Port = 8081

		print "Chargement du fichier "+chemin_fichier

		# On traite le contenu du fichier startup
		fichier = open(chemin_fichier).read()
		toutes_lignes = fichier.replace("\r","").split("\n")
		l = 0				
		for ligne in toutes_lignes:

			## Premiere ligne
			if l==0:
				# Adresse IP du serveur
				self.serveur_AdresseIP = ligne.split("ServerAddress: ")[1]

			## Deuxieme ligne
			elif l==1:
				# Port du serveur
				self.serveur_Port = int(ligne.split("ServerPort: ")[1])

			## Le reste
			else:

				# Traitement de l'ensemble des fichiers sous la forme flux[0-9].txt
				dataFlux = open(os.path.join(CONFIG_DOSSIER,os.path.normpath(ligne))).read()
				print("Chargement du fichier "+ligne)

				# On recupere les informations convernant la video
				Images = []
				for line in dataFlux.replace("\r","").split("\n"):					
					if (line.find("ID:") == 0):
						ID = line.split(" ")[1]

					elif (line.find("Port:") == 0):
						Port = line.split(" ")[1]

					elif (line.find("Address:") == 0):
						Address = line.split(" ")[1]

					elif (line.find("Protocol:") == 0):
						Protocol = line.split(" ")[1]

					elif (line.find("Name:") == 0):
						Name = line.split(" ")[1]

					elif (line.find("Type:") == 0):
						Type = line.split(" ")[1]

					elif (line.find("IPS:") == 0):
						Ips = line.split(" ")[1]

					else:
						Images.append(line)

				#On remplit le tableau 
				self.videos.append((ID, Name, Type, Address, Port, Protocol, Ips, Images))
			l+=1

	def buildCatalogue(self):
		catalogue = "ServerAddress: "+ self.serveur_AdresseIP + "\r\n"
		catalogue += "ServerPort: "+str(self.serveur_Port)+"\r\n"

		for video in self.videos:
			# On remplit le catalogue a communiquer au client
			catalogue += "Object ID="+video[0]
			catalogue += " name="+video[1]
			catalogue += " type="+video[2]
			catalogue += " address="+video[3]
			catalogue += " port="+video[4]
			catalogue += " protocol="+video[5]
			catalogue += " ips="+video[6]
			catalogue += "\r\n"
		catalogue += "\r\n"

		cat_len = len(catalogue)
		cat_header = "HTTP/1.1 200 OK\r\nServer: TP_3IF_MediaServer\r\nConnection: Keep-Alive\r\nContent-Type: text/txt\r\nContent-Length: "+str(cat_len)+"\r\n\r\n"

		return (cat_header+catalogue)		

	def getInfo(self):
		return (self.serveur_AdresseIP , self.serveur_Port)

	def createSockets(self):	
		# pour chaque vidéo du catalogue, on regarde son protocole et on crée un objet qui correspond
		retour = []
		for video in self.videos:
			tmp_serveur = VideoServer(video);
			tmp_serveur.connect();
			retour.append(tmp_serveur)
		return retour

# -*- coding: utf-8 -*-
from catalogue import *
from config import *
from SocketServer_TCP import *
import threading

print ""
print "#########################################################"
print " Serveur VOD de Mohammed Elalj et Josselin Dugue (B3411)"
print "#########################################################"
print ""

# Construction du catalogue
cat = Catalogue(os.path.join(CONFIG_DOSSIER,CONFIG_FILE))

# Envoi du catalogue
print ""
print "Création du serveur pour le catalogue : %s:%s" % (cat.serveur_AdresseIP, cat.serveur_Port)

serveur_catalogue = SocketServer_TCP(cat.getInfo(),'HTTP',cat.buildCatalogue())

# Creation des sockets pour chaque video
SOCKETS = cat.createSockets()

# Garder le programme allume
try:
	while True:
		pass

except KeyboardInterrupt, e:
	print ""
	print "Fermeture de l'ensemble des connexion"
	print "#########################################################"
	print ""
	

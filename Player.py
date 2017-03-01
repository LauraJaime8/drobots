#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots

class PlayerI(drobots.Player):
	def __init__(self, adapter):
		self.adapter = adapter
	
	#Funcion factoria con la que el juego le pide al jugador que cree un controlador
	#para el robot robot
	#def makeController(self, robot, current=None):
	
		
		def win(self, current=None):
	   	 print("Has ganado")
	   	 current.adapter.getCommunicator().shutdown()
	
	def lose(self, current=None):
		print("Has perdido")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("La partida ha abortado")
		current.adapter.getCommunicator().shutdown()



class Client(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		sirviente = PlayerI(adapter)

		adapter=broker.createObjectAdapter("PlayerAdapter")
		#proxy container
		proxyC = broker.stringToProxy("container")
		container=Services.ContainerPrx.checkedCast(proxyCon)
		#Proxy servidor
		proxyS=adapter.add(sirviente, broker.stringToIdentity("player1"))
		
		print(proxy)
		#proxies


		#funcion cliente
		#proxyC=self.communicator().stringToProxy("player1 -t -e 1.1:tcp -h 192.168.1.107 -p 9090 -t 60000")
		
		game=drobots.PlayerPrx.uncheckedCast(proxyC)
		if not game:
			raise RuntimeError('invalid proxy')
		
		
		return 0

		sys.stdout.flush()

		
		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()


sys.exit(Client().main(sys.argv))				
	

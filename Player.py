#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all FactoryAdapter.ice')
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import drobots
import Container

from drobots import (
	Player)


class PlayerI(drobots.Player):
	def __init__(self, adapter, sirviente, sirviente2):
		self.adaptador = adapter
		self.con=sirviente
		self.con1=sirviente2
		self.contadorCreados = 0
		self.contadorRobots = 0
	
	def makeController(self, bot, current):
		print("Recibo el bot {}".format(str(bot)))
		sys.stdout.flush()


		proxy, key=self.con.list()

		#proxy_player = adapter.add(sirviente, broker.stringToIdentity("player"))
		#proxy_player = drobots.PlayerPrx.uncheckedCast(proxy_player)
		
		#factory = adapter.add(sirviente, broker.stringToIdentity("factory1"))
		factory = drobots.FactoryPrx.uncheckedCast(proxy[key[self.contadorCreados]])
		if self.contadorCreados<2:
			self.contadorCreados = self.contadorCreados+1
		self.contadorRobots = self.contadorRobots+1
		# hacer casting de tipo
		#factory = drobots.FactoryPrx.uncheckedCast(factory)
		#print("make")
		robot = factory.make(bot, self.contadorRobots)
		self.con1.link(str(self.contadorRobots), robot)
	
		

		# devolver lo que devuelva la factoría
		return robot
		#return drobots.FactoryPrx.make(bot)
		#return drobots.FactoryPrx.checkedCast(factory)
	def makeDetectorController(self, current):
		pass
	
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

		adapterContainer = broker.createObjectAdapter("ContainerAdapter")
		adapterPlayer = broker.createObjectAdapter("PlayerAdapter")
		
		sirvienteContainer=Container.ContainerI()
		sirvienteContainer2 = Container.ContainerI()
		
		servantPlayer = PlayerI(adapterPlayer, sirvienteContainer, sirvienteContainer2)
		
		adapterContainer.add(sirvienteContainer, broker.stringToIdentity("Container"))
		adapterContainer.add(sirvienteContainer2, broker.stringToIdentity("Robot"))


		adapterPlayer.activate()
		adapterContainer.activate()
		
		proxy_player = adapterPlayer.add(servantPlayer, broker.stringToIdentity("player"))
		proxy_player = drobots.PlayerPrx.uncheckedCast(proxy_player)

		print(proxy_player)
		sys.stdout.flush()
		
		proxy_game = broker.propertyToProxy("GamePrx")
		proxy_game = drobots.GamePrx.checkedCast(proxy_game)
		
			
		if not proxy_game:
			raise RuntimeError('Invalid proxy')

		proxy_game.login(proxy_player, "Lauraa")
		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0

sys.exit(Client().main(sys.argv))
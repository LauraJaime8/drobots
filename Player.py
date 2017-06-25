#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import Ice
Ice.loadSlice('-I. --all drobots.ice')
Ice.loadSlice('-I. --all interfazAdicional.ice')

import drobots
import Services
import Container
import random


class PlayerI(drobots.Player):
	def __init__(self, broker, adapterPlayer):
		self.adaptador = adapterPlayer
		self.broker = broker
		self.contadorMK = 0
		self.contenedorFactorias = self.crearFactorias()
		self.contenedorRobots = self.crearRobots()
		
		
	def crearRobots(self):
		print("Crando el contenedor de los robots...")
		
		containerRobot_proxy = self.broker.stringToProxy('containerRobot -t -e 1.1:tcp -h localhost -p 9100 -t 60000')
		containerRobot = Services.ContainerPrx.checkedCast(containerRobot_proxy)			
		containerRobot.setType("ContainerRobotUno")
		

		return containerRobot


	def crearFactorias(self):
		container_proxy = self.broker.stringToProxy('containerFactoria -t -e 1.1:tcp -h localhost -p 9100 -t 60000')
		containerFactorias = Services.ContainerPrx.checkedCast(container_proxy)
		containerFactorias.setType("ContainerFactoryUno")
		
		print("Creando las tres factorías...")

		contadorF= 0
		while contadorF < 3:
			factory_proxy = self.broker.stringToProxy('factory -t -e 1.1:tcp -h localhost -p 900'+str(contadorF)+' -t 60000')
			factory = Services.FactoryPrx.checkedCast(factory_proxy)
			containerFactorias.link(contadorF, factory_proxy)
			contadorF += 1

		return containerFactorias




	def makeController(self, bot, current=None):
		print('Robot creado: %s' % bot)
		if self.contadorMK == 0:
			print("Entra en makeController...")

		contadorF= self.contadorMK % 3

		
		factory_proxy2 = self.contenedorFactorias.getElement(contadorF)
		
		factoriaFinal = Services.FactoryPrx.checkedCast(factory_proxy2)
		robots = factoriaFinal.make(bot, self.contenedorRobots, self.contadorMK)
			
		self.contadorMK += 1
		return robots

	def win(self, current=None):
		print("El jugador 1 ha ganado :D")
		current.adapter.getCommunicator().shutdown()
	
	def lose(self, current=None):
		print("El jugador 1 ha perdido :(")
		current.adapter.getCommunicator().shutdown()

	def gameAbort(self, current=None):
		print("La partida ha abortado")
		current.adapter.getCommunicator().shutdown()



class Client(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		
		adapterPlayer = broker.createObjectAdapter("PlayerAdapter")
	
		
		adapterPlayer.activate()
		servantPlayer = PlayerI(broker, adapterPlayer)

		proxy_player = adapterPlayer.add(servantPlayer, broker.stringToIdentity(str(os.getpid())))
		player = drobots.PlayerPrx.checkedCast(proxy_player)


		proxy_game = broker.propertyToProxy("GamePrx")
		game = drobots.GamePrx.checkedCast(proxy_game)


			
		if not game:
			raise RuntimeError('Invalid proxy')
		

		game.login(player, "Laura1")

		print("Se ha logueado el Jugador1")
		print("Esperando conexion...")

		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0

sys.exit(Client().main(sys.argv))
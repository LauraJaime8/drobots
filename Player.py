#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import Ice
Ice.loadSlice('-I. --all drobots.ice')
#Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
Ice.loadSlice('-I. --all interfazAdicional.ice')

import drobots

import Services
import Container
import random


class PlayerI(drobots.Player):
	def __init__(self, broker, adapterPlayer):
		self.adaptador = adapterPlayer
		#Cuenta las factorias
		self.broker = broker
		self.contadorMK = 0

		self.contenedorFactorias = self.crearFactorias()
		self.contenedorRobots = self.crearRobots()
		
	
	

	
	def crearRobots(self):
		#CREACION CONTAINER/////////////////////////////
		print("CREAMOS LOS CONTENEDORES DE LOS ROBOT CONTROLLER")

		containerRobot_proxy = self.broker.stringToProxy('containerRobot -t -e 1.1:tcp -h localhost -p 9100 -t 60000')

		containerRobot = Services.ContainerPrx.checkedCast(containerRobot_proxy)			
		containerRobot.setType("ContainerRobotUno")
		print ("contenedor de robot")
		print containerRobot
		#////////////////////////////////////////

		return containerRobot




	def crearFactorias(self):
		#FACTORIAS/////////////////////////////////////
		container_proxy = self.broker.stringToProxy('containerFactoria -t -e 1.1:tcp -h localhost -p 9100 -t 60000')

		
		containerFactorias = Services.ContainerPrx.checkedCast(container_proxy)
		#Escogemos el tipo que le queremos pasar al link
		containerFactorias.setType("ContainerFactoryUno")
		print("creamos las 3 factorias")
		print("--------------------------------------------------")
		#Contador factorias
		#Creador de factorias hasta 4
		contadorF= 0
		
		while contadorF < 3:
			#Crea un objeto por cada incremento de contadorFactorias
			factory_proxy = self.broker.stringToProxy('factory -t -e 1.1:tcp -h localhost -p 900'+str(contadorF)+' -t 60000')
			factory = Services.FactoryPrx.checkedCast(factory_proxy)
			print factory
			#variable que lleva la clave
			containerFactorias.link(contadorF, factory_proxy)
			contadorF += 1
		print ("contenedor factorias")
		print containerFactorias
		return containerFactorias

		#	fin creacion de factorias/////////////////////////////////

	def makeController(self, bot, current=None):
		#contadorF = 0
		#	creamos los robot controller
		if self.contadorMK == 0:
			print("entra en para crear los robot controller")

		#while self.contadorMK <3:
		contadorF= self.contadorMK % 3

		print("veces que entra en makecontroller")
		

		print contadorF
		#if self.contadorMK == 3:
		#	import pdb; pdb.set_trace()

		factory_proxy2 = self.contenedorFactorias.getElement(contadorF)
		#COGE EL CONTADOR
		
		factoriaFinal = Services.FactoryPrx.checkedCast(factory_proxy2)
		#Tiene que hacer 3 veces esto!!!!
		robots = factoriaFinal.make(bot, self.contenedorRobots, self.contadorMK)
			
		self.contadorMK += 1
		return robots

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
		
		adapterPlayer = broker.createObjectAdapter("PlayerAdapter")
		#adapterContainer = broker.createObjectAdapter("ContainerAdapter")
		
		#sirvienteContainer=Container.ContainerI()
		#robotContainer = Container.ContainerI()
		
		adapterPlayer.activate()
		servantPlayer = PlayerI(broker, adapterPlayer)



		#adapterContainer.add(sirvienteContainer, broker.stringToIdentity("Container"))
		#adapterContainer.add(robotContainer, broker.stringToIdentity("Robots"))


		proxy_player = adapterPlayer.add(servantPlayer, broker.stringToIdentity(str(os.getpid())))
		player = drobots.PlayerPrx.checkedCast(proxy_player)



		#adapterPlayer.activate()
		#adapterContainer.activate()
		

		proxy_game = broker.propertyToProxy("GamePrx")
		game = drobots.GamePrx.checkedCast(proxy_game)


			
		if not game:
			raise RuntimeError('Invalid proxy')
		

		game.login(player, "Lauri1")

		print("se loguea player1")
		print("esperando conexion......")

		

		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0

sys.exit(Client().main(sys.argv))
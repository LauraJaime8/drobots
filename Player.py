#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all drobots.ice')
#Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
Ice.loadSlice('-I. --all interfazAdicional.ice')

import drobots

import Services
import Container



from drobots import (
	Player)


class PlayerI(drobots.Player):
	def __init__(self, broker, adapterPlayer):
		self.adaptador = adapterPlayer
		#Cuenta las factorias
		self.contadorF = 0
		self.broker = broker
		
	
	def makeController(self, bot, current):
		contadorMK = 0
		print("Esprando el bot.....")

		print("Recibo el bot {}".format(str(bot)))
		sys.stdout.flush()
		print("entra en make controller")
		#broker = self.communicator()

		
		print("CREANDO LOS ROBOTS CONTROLLER")
		print("CREAMOS EL CONTENEDOR QUE GUARDARA LAS FACTORIAS")
		
		#container_proxy = self.broker.propertyToProxy("ContainerPrx")
		container_proxy = self.broker.stringToProxy('container -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
		containerFactorias = Services.ContainerPrx.checkedCast(container_proxy)



		#Escogemos el tipo que le queremos pasar al link
		containerFactorias.setType("ContainerFactr")
		print("creamos las 4 factorias")
		print("--------------------------------------------------")


		#Contador factorias
		
		contadorF= 0
		
		while contadorF < 3:
			#Crea un objeto por cada incremento de contadorFactorias
			factory_proxy = self.broker.stringToProxy('factory -t -e 1.1:tcp -h localhost -p 900'+str(contadorF)+' -t 60000')
			factory = Services.FactoryPrx.checkedCast(factory_proxy)
			print factory


			#variable que lleva la clave
			containerFactorias.link(contadorF, factory_proxy)
			


			contadorF += 1

		#Devuelve el contenedor de factorias (CONTAINERFACTORIAS)
		#que lo guarda la variable factory_proxy2
		if contadorMK == 0:
			print("creamos robots")
		contadorF = contadorMK % 3
		print("CONTADOR DE FACTORIAS")
		print contadorF
		factory_proxy2 = containerFactorias.getElement(contadorF)
		#COGE EL CONTADOR
		print("EL CONTADOR DEL PROXY ESSSSS:")
		print factory_proxy2


		#SEQUEDA AQUI
		print("CREAMOS LOS CONTENEDORES DE LOS ROBOT CONTROLLER")

		containerRobot_proxy= self.broker.stringToProxy('container -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
		containerRobot = Services.ContainerPrx.checkedCast(containerRobot_proxy)			
		containerRobot.setType("ContainerRobot")




		factoriaFinal = Services.FactoryPrx.checkedCast(factory_proxy2)
		


		print("ESTE ES EL BOT")
		print bot
		robots = factoriaFinal.make(bot, containerRobot, contadorMK)







		contadorMK += 1
		

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
		
		servantPlayer = PlayerI(broker, adapterPlayer)



		#adapterContainer.add(sirvienteContainer, broker.stringToIdentity("Container"))
		#adapterContainer.add(robotContainer, broker.stringToIdentity("Robots"))


		proxy_player = adapterPlayer.add(servantPlayer, broker.stringToIdentity("reo1"))
		player = drobots.PlayerPrx.checkedCast(proxy_player)



		adapterPlayer.activate()
		#adapterContainer.activate()
		

		proxy_game = broker.propertyToProxy("GamePrx")
		game = drobots.GamePrx.checkedCast(proxy_game)


			
		if not game:
			raise RuntimeError('Invalid proxy')
		

		game.login(player, "toli1")

		print("se loguea player1")
		print("esperando conexion......")

		

		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()
		return 0

sys.exit(Client().main(sys.argv))
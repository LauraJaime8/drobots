#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all FactoryAdapter.ice')
import drobots

class FactoryI(drobots.Application):

	def make(self, bot, current):
		if(bot.ice_isA("::drobots::Attacker")):
			print("Robot atacante")
			#sirviente = PlayerI(bot)
			sirviente = RobotControllerAttacker(bot)
		elif (bot.ice_isA("::drobots::Defender")):
			print("Robot defensor")
			sirviente = RobotControllerDefender(bot)

		print(bot)


		proxy = current.adapter.addWithUUID(sirviente)
		proxyId = proxy.ice_getIdentity()
		proxyDirecto = current.adapter.createDirectProxy(proxyDirecto)

		#return drobots.PlayerPrx.checkedCast(proxy)
		return bot



class RobotControllerAttacker(controller.RobotControllerAttacker):
	





class RobotControllerDefender(controller.RobotControllerDefender):
	def __init__(self, bot):
		self.bot = bot
		self.energia = 100
		self.velocidad = 40
		self.estadoActual = "Moviendose"
		self.turnos = 0
		self.angulo = 0
		self.coordenadas = []
		print("Se ha creado un robot defensor")


		def turn(self, current=None):
			print("Turno del defensor")
			proxy = current.adapter.getCommunicator().stringtoProxy("Container")			
			self.energia = 100

			if(self.estadoActual=='Escaneando'):
				self.turnos = turnos+1
				robotsEnemigos = self.bot.scan(self.angulo, 15)
				if((self.turnos==20)):
					self.estadoActual="Moviendose"
				elif(robotsEnemigos>0):
					print("Se han encontrado enemigos")
					if((self.turnos==10)):
						self.angulo = self.angulo + 10
					else:
						self.angulo = self.angulo + 15

				elif(robotsEnemigos==0):
					self.angulo = self.angulo+15
			
			elif(self.estadoActual=='Moviendose'):
				print("El robot cambia de rumbo")
				xDestino = random.randint(10,990)
				yDestino = random.randint(10,990)

				posicion = self.bot.location()
				x = posicion.x
				y = posicion.y
				
















class Server(Ice.Application):
	def run(self,argv):
		broker = self.communicator()
		sirviente = FactoryI()

		adapter = broker.createObjectAdapter("FactoryAdapter")
		proxy = adapter.addWithUUID(sirviente)

		print(proxy)
		sys.stdout.flush()

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


sys.exit(server.main(sys.argv))



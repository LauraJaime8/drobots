#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all interfazAdicional.ice')
import Services
import drobots


class FactoryI(Services.Factory):
	def __init__(self):
		pass

	def make(self, bot, containerRobot, contador, current=None):
		print("Creando los tipos de robots..............................................")
		
	

		if bot.ice_isA("::drobots::Attacker"):
			#print("Robot atacante")
			robot_servant = RobotControllerAttacker(bot, containerRobot)
			#p#rint("sirviente del robot")
			#print(robot_servant)

			#sirviente = PlayerI(bot)
			#sirviente = RobotControllerAttacker(bot)
			robot_proxy = current.adapter.addWithUUID(robot_servant)
			containerRobot.link(contador, robot_proxy)
			robot = drobots.RobotControllerPrx.checkedCast(robot_proxy)


		elif bot.ice_isA("::drobots::Defender"):
			#print("Robot defensor")

			#robot_servant = RobotController(bot, containerRobot)
			robot_servant = RobotControllerDefender(bot, containerRobot)
			robot_proxy = current.adapter.addWithUUID(robot_servant)
			
			containerRobot.link(contador, robot_proxy)
			print containerRobot
			
			try:
				robot = drobots.RobotControllerPrx.checkedCast(robot_proxy)
			except Exception as e:
				print(e)
				raise e
			
		#print(robot)


		return robot



class RobotControllerAttacker(drobots.RobotController):
	def __init__(self, bot, containerRobot):
		self.bot = bot
		self.containerRobot = containerRobot
		self.velocidad = 40
		self.estadoActual = "Moviendose"
		self.turnos = 0
		self.angulo = 0
		self.coordenadas = []
		print("Se ha creado un robot ATACANTE:")
		print bot

	def turn(self, current):
		if(self.estadoActual == "Atacando"):
			self.turnos = self.turnos+1
			print("El robot esta disparando")

			distancia = random.randint(100,620)
			self.bot.cannon(self.angulo, distancia)
			distancia = random.randint(100,620)
			self.bot.cannon(self.angulo, distancia)
			if((self.turnos==20)):
				self.estadoActual="Moviendose"

		elif(self.estadoActual=="Moviendose"):
			print("El robot esta cambiando de rumbo")
			xDestino = random.randint(10,990)
			yDestino = random.randint(10,990)

			posicion = self.bot.location()
			x = posicion.x
			y = posicion.y

			distancia = int(math.sqrt((x-xDestino)**2+(y-yDestino)**2))
			datoAngulo = math.degrees(math.atan2(xDestino-y, yDestino-x))
			if(distancia>4):
				self.bot.drive(datoAngulo,100)

			self.angulo = 0
			self.turnos = 0

	def definirContainer(self, container, current):
		self.containerRobot = container

	def robotDestroyed(self, current):
		print("Robot destruido")

	def EnemigoDetectado(sel, angulo2, current):
		print("Se ha detectado un enemigo")
		self.angulo = 360-angulo2
		self.estadoActual = "Disparando"


	def NoEnemy(self, current):
		print("No hay enemigos")
		self.estadoActual = "Moviendose"


class RobotControllerDefender(drobots.RobotController):
	def __init__(self, bot, containerRobot):
		self.bot = bot
		self.containerRobot = containerRobot
		self.energia = 100
		self.velocidad = 40
		self.estadoActual = "Moviendose"
		self.turnos = 0
		self.angulo = 0
		self.coordenadas = []
		print("Se ha creado un robot DEFENSOR:")
		print bot

		def turn(self, current=None):
			print("Turno del defensor")
			proxy = current.adapter.getCommunicator().stringtoProxy("container")			
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

				distancia = int(math.sqrt((x-xDestino)**2+(y-yDestino)**2))
				datoAngulo = math.degrees(math.atan2(xDestino-y, yDestino-x))
				if(distancia>4):
					self.bot.drive(datoAngulo,100)

				self.angulo = 0
				self.turnos = 0
				self.estadoActual = "Escaneando"






class Server(Ice.Application):
	def run(self,argv):
		broker = self.communicator()
		sirviente = FactoryI()


		adapter = broker.createObjectAdapter("FactoryAdapter")

		proxy = adapter.add(sirviente, broker.stringToIdentity("factory"))

		
		print(proxy)
		sys.stdout.flush()

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0


Server().main(sys.argv)



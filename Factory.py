#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all interfazAdicional.ice')
Ice.loadSlice('-I. --all partida.ice')

import Services
import drobots
import random
import math
import Partida


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
		self.energia = 0
		self.coordenadas = []
		self.distanciaMisil = 200 #metros
		self.velocidadMisil = 100 #m/s
		self.anguloLanzaMisil = 0 #de 0-359
		self.anguloDis = 0
		self.localizacion = 0
		self.x = 10
		self.y = 10
		self.contadorDisparos = 0
		self.daño=0
		print("Se ha creado un robot ATACANTE:")


	def turn(self, current):
		print("Turno del atacante")
		self.energia = 100
		self.localizacion = self.bot.location()
		print("Posicion del robot:")
		print(str(self.localizacion.x)+","+str(self.localizacion.y))

		if(self.energia>50):
			distancia = random.randint(1,39)*10
			self.angulo=random.randint(0,359)
			
			#Dispara///////////////////////
			if(self.contadorDisparos <= 15):
				anguloD = self.anguloDis + random.randint(0,359)
				distancia = random.randint(0,300)-self.localizacion.y-self.localizacion.x
				
				if(distancia<21):
					distancia = random.randint(21,100)

					self.bot.cannon(anguloD, distancia)
					print("Se ha disparado hacia" +str(anguloD) +" a una distancia de " + str(distancia))
				
					self.contadorDisparos += 1
					self.estadoActual = "Disparando"

			else:
				self.contadorDisparos = 0
				self.estadoActual="Moviendose"
			#///////////////////////////

			self.energia -= 50
		if(self.energia>60):

			#//SE MUEVE//////////////////////
			localizacion = self.bot.location()
			if(self.velocidad == 0):
				self.bot.drive(random.randint(0,360),100)
				self.velocidad = 100
			elif(localizacion.x > 390):
				self.bot.drive(225, 100)
				self.velocidad = 100
			elif(localizacion.x < 100):
				self.bot.drive(45, 100)
				self.velocidad = 100
			elif(localizacion.y > 390):
				self.bot.drive(315, 100)
				self.velocidad = 100
			elif(localizacion.y < 100):
				self.bot.drive(135, 100)
				self.velocidad = 100
			#////////////////////////////////
			self.energia -= 60


	def robotDestroyed(self, current):
		print("Robot ATACANTE destruido")


	def EnemigoDetectado(sel, angulo2, current):
		print("Se ha detectado un enemigo")
		self.angulo = 360-angulo2
		self.estadoActual = "Disparando"


	def NoEnemigo(self, current):
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
		self.todosAngulos = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
		self.angulosEscaneados = self.todosAngulos[:]
		random.shuffle(self.angulosEscaneados)
		print("Se ha creado un robot DEFENSOR:")
		#print bot

		def turn(self, current=None):
			print("Turno del defensor")
			self.energia = 100
			self.localizacion = self.bot.location()
			self.angulo =random.randint(0,359)
			if(self.energia>10):
				#//ESCANEAR
				amplitud = 20
				try:
					anguloS = self.angulosEscaneados.pop()
				except IndexError:
					self.angulosEscaneados = self.todosAngulos[:]
					random.shuffle(self.angulosEscaneados)
					anguloS = self.angulosEscaneados.pop()            
				
				enemigosDetectados = self.bot.scan(anguloS, amplitud)
				if enemigosDetectados <> 0:
					self.bot.drive(0, 0)
					self.anguloDis = anguloS
					self.estadoActual = "Disparando"
				#/////////////////////////

			if(self.energia>60):
				#//MOVERSE	
				localizacion = self.bot.location()
			if(self.velocidad == 0):
				self.bot.drive(random.randint(0,360),100)
				self.velocidad = 100
			elif(localizacion.x > 390):
				self.bot.drive(225, 100)
				self.velocidad = 100
			elif(localizacion.x < 100):
				self.bot.drive(45, 100)
				self.velocidad = 100
			elif(localizacion.y > 390):
				self.bot.drive(315, 100)
				self.velocidad = 100
			elif(localizacion.y < 100):
				self.bot.drive(135, 100)
				self.velocidad = 100
			#////////////////////////////////


		def robotDestroyed(self, current):
			print("Robot DEFENSOR destruido")



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
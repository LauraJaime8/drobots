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
		if bot.ice_isA("::drobots::Attacker"):
			robot_servant = RobotControllerAttacker(bot, containerRobot)
			robot_proxy = current.adapter.addWithUUID(robot_servant)
			containerRobot.link(contador, robot_proxy)
			robot = drobots.RobotControllerPrx.checkedCast(robot_proxy)

		else:
			robot_servant = RobotControllerDefender(bot, containerRobot)
			robot_proxy = current.adapter.addWithUUID(robot_servant)
			containerRobot.link(contador, robot_proxy)
			robot = drobots.RobotControllerPrx.checkedCast(robot_proxy)
			
		return robot



class RobotControllerDefender(drobots.RobotController):
	def __init__(self, bot, containerRobot):
		self.bot = bot
		self.containerRobot = containerRobot
		self.energia = 100
		self.velocidad = 40
		self.estadoActual = "Moviendose"
		self.listaAmigos= dict()
		self.listaEnemigos = dict()
		self.turnos = 0
		self.x = 290
		self.y = 290
		self.amplitud=20
		self.turno = 0
		self.coordenadas = []
		self.todosAngulos = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340]
		self.angulosEscaneados = self.todosAngulos[:]
		random.shuffle(self.angulosEscaneados)

		print("Se ha creado un robot DEFENSOR")
		print("Esperando por el turno(defensor)....")

		def turn(self, current=None):
			print("Turno del DEFENSOR")
			turno += 1
			self.energia = 100
			localizacion = self.bot.location() #punto
			self.angulo =random.randint(0,359)

			if(self.energia>10):
				self.escanear()
			if(self.energia>60):
				self.moverse(localizacion)
			

			#DEVOLVER MI POSICION EN EL MAPA
			self.MiPosicion()
			self.posicionAmigosPrint(self.localizacion,contadorAtacantes)
			print("Turno: " + str(self.turno))
			print("Daño: " + str(self.damage))
		
		

		def moverse(self, localizacion):
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

		def escanear(self):
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
				self.anguloDisparo = anguloS
				self.estadoActual = "Disparando"
			#/////////////////////////


		def robotDestroyed(self, current):
			print("Robot DEFENSOR destruido")

		def posicionAmigosPrint(self, point, identificador, current=None):
			self.posicionAmigos[identificador] = point
			print("El atacante " + str(identificador)+ " tiene la posicion: " +str(point.x)+ ' ' + str(point.y))


		def MiPosicion(self):
			miLocalizacion = self.bot.location()
			print("Mi posicion es:")
			print(miLocalizacion)
	




class RobotControllerAttacker(drobots.RobotController):
	def __init__(self, bot, containerRobot):
		self.bot = bot

		self.containerRobot = containerRobot
		self.velocidad = 40
		self.estadoActual = "Moviendose"
		self.turno = 0
		self.angulo = 0
		self.energia = 0
		self.posicionAmigos = dict()
		self.anguloDis = 0
		self.localizacion = 0
		self.x = 10
		self.y = 10
		self.contadorDisparos = 0
		self.damage=0

		print("Se ha creado un robot ATACANTE")
		print("Esperando por el turno(atacante)....")



	def turn(self, current):
		try:		
			contadorDefensores = 0
		
			print("Turno del atacante")
			self.turno += 1
			self.energia = 100
			self.localizacion = self.bot.location() #Coordenadas
			#print("Posicion del robot:")
			#print(str(self.localizacion.x)+","+str(self.localizacion.y)


			if(self.energia>50):
				distancia = random.randint(1,39)*10
				self.angulo=random.randint(0,360)
				self.disparar()
				self.energia -= 50

			if(self.energia>60):
				self.mover(self.localizacion, self.energia)
				self.energia -= 60
		
			if(self.bot.damage()>self.damage):
				self.damage = self.bot.damage()
				self.mover(self.energia)

		except drobots.NoEnoughEnergy:
			pass


		#TODA LA INFORMACION DEL TURNO
		self.MiPosicion()
		self.posicionAmigosPrint(self.localizacion,contadorDefensores)
		print("Turno: " + str(self.turno))
		print("Daño: " + str(self.damage))
		if(contadorDefensores<=3):
			contadorDefensores += 1


	def mover(self, energia):
		localizacion = self.bot.location()
		if(self.velocidad == 0):
			self.bot.drive(random.randint(0,360),100)
			self.velocidad = 100
			energia -= 1
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
		
	def disparar(self):
		if(self.contadorDisparos <= 15):
			anguloD = self.anguloDis + random.randint(0,360)
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


	def robotDestroyed(self, current):
		print("Robot ATACANTE destruido")

	def posicionAmigosPrint(self, point, identificador, current=None):
		self.posicionAmigos[identificador] = point
		print("El defensor " + str(identificador)+ " tiene la posicion: " +str(point.x)+ ' ' + str(point.y))



	def EnemigoDetectado(sel, x,y, current):
		print("Se ha detectado un enemigo")
		Point=[]
		Point.append(x)
		Point.append(y)
		self.posicionEnemigos.append(Point)
		print("El enemigo esta en el punto:")
		print(x,y)

	def MiPosicion(self):
		miLocalizacion = self.bot.location()
		print("Mi posicion es:")
		print(miLocalizacion)

	
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
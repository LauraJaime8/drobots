#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('-I. --all FactoryAdapter.ice')
import drobots

class FactoryI(drobots.Application):

	def make(self, bot, current):
		sirviente = PlayerI(bot)
		proxy = current.adapter.addWithUUID(sirviente)
		return drobots.PlayerPrx.checkedCast(proxy)


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



#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('I. --all FactoryAdapter.ice')
import drobots

class PlayerI(drobots.Application):
	def __init__(self, current):
		pass


class FactoryAdapterI(drobots.FactoryAdapter):
	def make(self, bot, current):
		
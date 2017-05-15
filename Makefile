#!/usr/bin/make -f
# -*- mode:makefile -*-

make:
	./Player.py --Ice.Config=player.config

run-all: run-container run-factory

run-container:
	python Container.py --Ice.Config=player.config

run-factory:
	python Factory.py --Ice.Config=player.config
	

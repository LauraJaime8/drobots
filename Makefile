#!/usr/bin/make -f
# -*- mode:makefile -*-

make:
	./Player.py --Ice.Config=player.config

run-all: run-container run-factory run-player run-player2

run-container:
	gnome-terminal -x python ./Container.py --Ice.Config=player.config

run-factory:
	gnome-terminal -x python ./Factory.py --Ice.Config=player.config

run-player:
	gnome-terminal -x python ./Player.py --Ice.Config=player.config

run-player2:
	gnome-terminal -x python ./Player2.py --Ice.Config=player.config

#!/usr/bin/make -f
# -*- mode:makefile -*-


all: run-factory1 run-factory2 run-factory3 run-factory4 run-container run-player run-player2

run-container:
	gnome-terminal -x python ./Container.py --Ice.Config=container.config

run-factory1:
	gnome-terminal -x python ./Factory.py --Ice.Config=factory1.config

run-factory2:
	gnome-terminal -x python ./Factory.py --Ice.Config=factory2.config

run-factory3:
	gnome-terminal -x python ./Factory.py --Ice.Config=factory3.config

run-factory4:
	gnome-terminal -x python ./Factory.py --Ice.Config=factory4.config


run-player:
	gnome-terminal -x python ./Player.py --Ice.Config=player.config

run-player2:
	gnome-terminal -x python ./Player2.py --Ice.Config=player.config

clean:
	rm *.pyc

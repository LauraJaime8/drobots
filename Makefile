#!/usr/bin/make -f
# -*- mode:makefile -*-


all:
	gnome-terminal -e "make run-factorias"
	gnome-terminal -e "make run-container"
	gnome-terminal -e "make run-player2"
	gnome-terminal -e "make run-player"
run-factorias:
	make -j run-factory1 run-factory2 run-factory3

run-container:
	 python ./Container.py --Ice.Config=container.config

run-factory1:
	 python ./Factory.py --Ice.Config=factory1.config

run-factory2:
	python ./Factory.py --Ice.Config=factory2.config

run-factory3:
	 python ./Factory.py --Ice.Config=factory3.config

run-player:
	python ./Player.py --Ice.Config=player.config

run-player2:
	 python ./Player2.py --Ice.Config=player.config
	
clean:
	rm *.pyc

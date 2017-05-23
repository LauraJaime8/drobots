// -*- mode:c++ -*-
#include "drobots.ice"

module Services {

  dictionary<string, Object*> ObjectPrxDict;

  interface Container {
  	void link(int key, Object* proxy);
        void unlink(int key);
        ObjectPrxDict list();
        Object* getElement(int key);
        void setType(string type);
        string getType();
  };

	
  interface Factory {
     drobots::RobotController* make(drobots::Robot* bot, Container* container, int key);
  };

	interface RobotControllerAttacker extends drobots::RobotController{
		void definirContainer(Container* containerRobot);
	};
	interface RobotControllerDefender extends drobots::RobotController{
		void definirContainer(Container* containerRobot);
	};
};

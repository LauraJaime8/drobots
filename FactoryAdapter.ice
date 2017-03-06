// -*- mode:c++ -*-

#include "drobots.ice"

module drobots {
  interface FactoryAdapter{
   drobots::RobotController* make(drobots::Robot* bot);
  };
};

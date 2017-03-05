#include <drobots.ice>

module drobots {
  interface FactoryAdapter {
    Player* makeController(Robot* bot);
  };
};

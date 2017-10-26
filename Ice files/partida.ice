#include "drobots.ice"

module Partida {

  interface Coordinacion {
	void EnemigoDetectado(int x, int y);
	void MiPosicion(int x, int y);
	
  };
};

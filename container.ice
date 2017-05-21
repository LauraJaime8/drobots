// -*- mode:c++ -*-

module Services {
  

 struct Point {
    int x;
    int y;
  };

  exception NoEnoughEnergy{};
  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };

  dictionary<string, Object*> ObjectPrxDict;

  interface Container {
  	void link(int key, Object* proxy);
        void unlink(int key);
        ObjectPrxDict list();
        Object* getElement(int key);
        void setType(string type);
        string getType();
  };

 

  interface RobotBase {
    void drive(int angle, int speed) throws NoEnoughEnergy;
    short damage() throws NoEnoughEnergy;
    short speed() throws NoEnoughEnergy;
    Point location() throws NoEnoughEnergy;
    short energy() throws NoEnoughEnergy;
  };

  interface RobotController {
    void turn();
    void robotDestroyed();
  };

  interface Attacker extends RobotBase {
    bool cannon(int angle, int distance) throws NoEnoughEnergy;
  };

  interface Defender extends RobotBase {
    int scan(int angle, int wide) throws NoEnoughEnergy;
  };

  interface Robot extends Attacker, Defender {};
	
 interface Factory {
     RobotController* make(Robot* bot, Container* container, int key);
  };
};

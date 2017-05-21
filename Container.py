#!/usr/bin/python -u
# -*- coding:utf-8; tab-width:4; mode:python -*-

import sys
import Ice
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services
#Ice.loadSlice('-I. --all container.ice')


class ContainerI(Services.Container):
    def __init__(self):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            raise Services.AlreadyExists(key)

        print("link: {0} -> {1}".format(self.type,key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise Services.NoSuchKey(key)

        print("unlink: {0}".format(self.type,key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies, list(self.proxies.keys())

    def setType(self, t, current=None):
        self.type = t
        
    def getType(self, current=None):
        return self.type


    def getElement(self, key, current=None):
       return self.proxies[key]
    

class Server(Ice.Application):
  def run(self, argv):
    broker = self.communicator()
    servant = ContainerI()
#
    adapter = broker.createObjectAdapter("ContainerAdapter")
    proxy = adapter.add(servant, broker.stringToIdentity("container1"))

   #     print(proxy)
    #    print("EJECUTA")
    adapter.activate()
    self.shutdownOnInterrupt()
    broker.waitForShutdown()

    return 0

if __name__ == '__main__':
  sys.exit(Server().main(sys.argv))
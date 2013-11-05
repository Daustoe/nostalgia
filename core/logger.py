'''
Created on Oct 29, 2013

@author: Claymore
'''

from singleton import Singleton
import io


class logger(Singleton):

    def __init__(self):
        super(logger, self).__init__()
        self.app = io.open('app.log', 'w')
        self.client = io.open('client.log', 'w')
        self.server = io.open('server.log', 'w')

    def write(self, target, message):
        if target is "app":
            self.app.write(message)
            self.app.flush()
        elif target is "client":
            self.client.write(message)
            self.client.flush()
        elif target is "server":
            self.server.write(message)
            self.server.flush()
        else:
            print message

    def close(self):
        self.app.close()
        self.client.close()
        self.server.close()

from multiprocessing.sharedctypes import Value
from socket import *
import pickle
import sys

class server(object):
    CACHE = {}
    def __init__(self, connections = 5, bind_port = 27700, bind_ip = 'localhost'):
        object.__init__(self)
        self.filename = 'memcache.pickle'
        self.file = open(self.filename, 'wb')
        self.start_server(bind_ip, bind_port, connections)

    def set(self, key, value):
        self.CACHE[key] = value

    def get(self, key):
        return self.CACHE.get(key)

    def delete(self, key):
        if key in self.CACHE:
            del self.CACHE[key]
        return True

    def flush(self):
        self.CACHE.clear()
        return True

    def start_server(self, bind_ip, bind_port, connections):
        # Set up a TCP/IP server
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.bind((bind_ip, bind_port))
        tcp_socket.listen(connections)
        
        while True:
            connection, addr = tcp_socket.accept()
            try:
                print("Connected to client IP: {}".format(addr))
                
                # Receive and print data 32 bytes at a time, as long as the client is sending something
                while True:
                    dat = connection.recv(1024)
                    print("Received data: {}".format(dat))
                    # set(addr[1], dat)
                    if not dat:
                        break
                    key_value = dat.decode()
                    key_value = key_value.split('=')
                    # print(key_value)
                    # print(myval)
                    if self.get(key_value[0]) == None:
                        self.set(key_value[0], key_value[1])
                        connection.send(b'stored' + key_value[0])
                    else:
                        connection.send(b'not stored')        
            finally:
                connection.close()

if __name__ == "__main__":
    test_server = server()
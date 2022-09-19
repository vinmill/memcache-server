from multiprocessing.sharedctypes import Value
from socket import *
import pickle
import sys, os

class server(object):
    def __init__(self, connections = 5, bind_port = 27700, bind_ip = 'localhost'):
        object.__init__(self)
        self.filename = 'memcache.pickle'
        self.local_dict = {}
        if not os.path.isfile(self.filename):
            with open(self.filename,"wb") as f:
                pickle.dump(self.local_dict, f)
        self.start_server(bind_ip, bind_port, connections)

    def set(self, key, value):
        self.local_dict = {key:value}
        with open(self.filename, 'rb') as f:
            self.local_dict.update(pickle.load(f))
        with open(self.filename, 'wb') as f:
            pickle.dump(self.local_dict, f)

    def get(self, key):
        with open(self.filename, 'rb') as f:
            self.local_dict = pickle.load(f)
        return self.local_dict.get(key)

    def delete(self, key):
        if self.get(key) != None:
            with open(self.filename, 'rb') as f:
                full = pickle.load(f)
            del self.local_dict[key]
            with open(self.filename, 'wb') as f:
                pickle.dump(self.local_dict, f)
        return True

    def flush(self):
        with open(self.filename, 'rb') as f:
            self.local_dict = pickle.load(f)
        self.local_dict.clear()
        with open(self.filename, 'wb') as f:
            pickle.dump(self.local_dict, f)
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

                    if not dat:
                        break
                    key_value = dat.decode()
                    key_value = key_value.split('=')
                    print(self.get(key_value[0]))
                    if self.get(key_value[0]) == None:
                        self.set(key_value[0], key_value[1])
                        connection.send(b'stored')
                    else:
                        connection.send(b'not stored')
                    with open(self.filename, 'rb') as f:
                        self.local_dict = pickle.load(f)
                    print(self.local_dict)
            finally:
                connection.close()

if __name__ == "__main__":
    test_server = server()
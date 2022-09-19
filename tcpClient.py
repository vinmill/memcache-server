import sys
from socket import *
import argparse
parser = argparse.ArgumentParser(description='parse key pairs into a dictionary')

class client(object):
    def __init__(self, num_clients = 3, target_port = 27700, target_host = 'localhost', **kwargs):
        object.__init__(self)
        self.__dict__.update(kwargs)
        self.connection(target_host, target_port, kwargs)

    # Create a connection to the server application on port 27700
    def connection(self, target_host, target_port, kwargs):
        try:
            if len(sys.argv) > 1:
                target_host = sys.argv[1]

            tcp_socket = socket(AF_INET, SOCK_STREAM)
            tcp_socket.connect((target_host, target_port))
            # Receive and print data 32 bytes at a time, as long as the client is sending something
            for key, value in kwargs.items():
                keymod = key + "=" + value
                tcp_socket.send(keymod.encode())
                data = tcp_socket.recv(1024)
                print('Recieved:', data)

                # print("client received: {}".format(dat))
    
        finally:
            tcp_socket.close()

if __name__ == "__main__":
    test_client = client(pam='spam is for me', lamb='asfd', cam='123453453')
from socket import *
import pickle
import os, time

class server(object):
    def __init__(self, connections = 5, bind_port = 27700, data_size=1024, bind_ip = 'localhost'):
        object.__init__(self)
        self.filename = 'memcache.pickle'
        self.data_size = data_size
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
    
    def now(self):
        return time.ctime(time.time())
    
    def threaded(self, connection, addr):
        try:
            while True:
                dat = connection.recv(self.data_size)

                if not dat:
                    break
                key_value = dat.decode()
                key_value = key_value.split('=')
                if self.get(key_value[0]) == None:
                    self.set(key_value[0], key_value[1])
                    keystoremsg = 'STORED\r\n'
                    connection.send(keystoremsg.encode())
                else:
                    keystoremsg = 'NOT-STORED\r\n'
                    connection.send(keystoremsg.encode())
                with open(self.filename, 'rb') as f:
                    self.local_dict = pickle.load(f)
                getvalue = self.get(key_value[0])
                bytes_obj = bytes(getvalue , "UTF-8")
                print('VALUE {} {} {} bytes\r\n'.format(getvalue, key_value[0], len(bytes_obj)))
                print('{} \r\n'.format(bytes_obj))
        finally:
            connection.close()
    
        # connection closed
        connection.close()

    def start_server(self, bind_ip, bind_port, connections):
        # Set up a TCP/IP server
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.bind((bind_ip, bind_port))
        tcp_socket.listen(connections)
        
        while True:
            connection, addr = tcp_socket.accept()
            print('SERVER: Connected to: ' + addr[0] + ':' + str(addr[1]))
            self.threaded(connection, addr)
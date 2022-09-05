from multiprocessing.sharedctypes import Value
import socket
import sys
# from webbrowser import get

CACHE = {}
bind_ip = 'localhost'
bind_port = 27700

def set(key, value):
    CACHE[key] = Value
    return True

def get(key):
    return print(CACHE.get(key))

def delete(key):
    if key in CACHE:
        del CACHE[key]

def flush():
    CACHE.clear()

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Bind the socket to server address and port 27700
server_address = (bind_ip, bind_port)
tcp_socket.bind(server_address)
 
# Listen on port 27700
tcp_socket.listen(1)
 
while True:
    print("Waiting for connection")
    connection, client = tcp_socket.accept()
 
    try:
        print("Connected to client IP: {}".format(client))
         
        # Receive and print data 32 bytes at a time, as long as the client is sending something
        while True:
            data = connection.recv(128)
            print("Received data: {}".format(data))
            set(client[1], data)
            print(client[1])
            get(client[1])
            if not data:
                break
 
    finally:
        connection.close()
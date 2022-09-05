import socket

target_host = 'localhost'
target_port = 27700
# Create a connection to the server application on port 27700
tcp_socket = socket.create_connection((target_host, target_port))
 
try:
    print('welcome')
    data = 'Hi. I am a TCP client sending data to the server'
    tcp_socket.sendto(data.encode(),(target_host, target_port))
 
finally:
    print("Closing socket")
    tcp_socket.close()
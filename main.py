from multiprocessing.connection import Client
# from tcpClient import client
# from tcpServer import server
import os, sys

for i in range(10):
    if sys.platform[:3] == 'win':
        pypath = sys.executable
        os.spawnv(os.P_NOWAIT, pypath, ('python', 'tcpClient.py', str(i)))
    else:
        pid = os.fork()
        if pid != 0:
            print('Process %d spawned' % pid)
        else:
            os.execlp('python', 'python', 'tcpClient.py', str(i))
print('Main process exiting.')

# if __name__ == "__main__":
#     test_server = server()
#     test_client = client()
#     test_server.run()
#     test_client.run()
import socket
from time import sleep

HOST = 'localhost'
PORT = 8000

server = (HOST, PORT)

TCP_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCP_client.connect(server)

sleep(5)

TCP_client.send(socket.gethostname().encode())
message = TCP_client.recv(1024)
print(message)
TCP_client.close()

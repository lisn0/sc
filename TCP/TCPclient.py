import socket

HOST = 'localhost'
PORT = 8001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCP_client:
    TCP_client.connect((HOST, PORT))
    TCP_client.send(socket.gethostname().encode())
    message = TCP_client.recv(1024)
    print(message)
    TCP_client.close()

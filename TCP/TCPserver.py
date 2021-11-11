import socket

HOST = ''
PORT = 8001

address = (HOST, PORT)


tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(address)
tcp_server.listen()


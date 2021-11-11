import socket

HOST = ''
PORT = 8001

address = (HOST, PORT)

try:
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind(address)
except socket.error as err_msg:  # 4
    print('Error code: %d, Error message: %s' % (err_msg[0], err_msg[1]))
    exit(1)

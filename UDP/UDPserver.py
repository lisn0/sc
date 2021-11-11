import socket

HOST = ''
#PORT = 23 # 2: PermissionError: [Errno 13] Permission denied
PORT = 9875
address = (HOST, PORT)

try:
    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServer.bind(address)
except socket.error as err_msg:  # 4
    print('Error code: %d, Error message: %s' % (err_msg[0], err_msg[1]))
    exit(1)

try:
    while 1:
        message, client = udpServer.recvfrom(1024)
        print("Message :", message, " from address : ", client[0])  # 6
except socket.error as err_msg:
    print('Error code: %d, Error message: %s' % (err_msg[0], err_msg[1]))
    udpServer.close()

# 3 : the program exit on its own
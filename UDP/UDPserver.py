import socket

HOST = ''
PORT = 9898

try:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))
except socket.error as error:  # 4
    print('Error code: %d, Error message: %s' % (error[0], error[1]))
    exit(1)

try:
    while True:
        message, client = udp.recvfrom(1024)
        print("Message :", message, " from address : ", client[0])  # 6
except socket.error as error:
    print('Error code: %d, Error message: %s' % (error[0], error[1]))
    udp.close()


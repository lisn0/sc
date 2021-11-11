import socket

SERVER = ('127.0.0.1', 9875)
UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDP_client.sendto(('Test message').encode(), SERVER)

# 3.1.2.8: Message : b'Test message'  from address :  127.0.0.1
# 3.1.2.9: TODO

import socket


if __name__ == "__main__":
    SERVER = ('127.0.0.1', 9898)
    UDP_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_client.sendto('Hello udp World!'.encode(), SERVER)


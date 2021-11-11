import socket

HOST = ''
PORT = 8001

address = (HOST, PORT)


tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(address)
tcp_server.listen(0)

while True:
    conn, address_client = tcp_server.accept()
    with conn:
        print('Accepted connection from {}:{}'.format(address_client[0], address_client[1]))
        while True:
            data = conn.recv(1024)
            if not data:
                break

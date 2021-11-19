import socket

HOST = ''
PORT = 8000

address = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
    tcp_server.bind(address)
    tcp_server.listen(0)  # listen for incoming connections, listen put the socket on server mode
    # the argument the number of clients waiting for connection that can be queued
    while True:
        conn, address_client = tcp_server.accept()  # wait for a connection
        with conn:
            print('Accepted connection from {}:{}'.format(address_client[0], address_client[1]))
            while 1:
                data = conn.recv(1024)
                if len(data) > 0:
                    conn.send(b"OK")
                else:
                    conn.close()
                    print("client disconnected")
                    break

        print("connection ended")

#  https://realpython.com/python-sockets/#echo-server

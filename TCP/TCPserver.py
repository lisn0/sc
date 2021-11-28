import socket

HOST = ''
PORT = 8001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
    tcp_server.bind((HOST, PORT))
    tcp_server.listen(0)
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


# 2: i don't have it in my system, i use systemd
# 3 : /etc/init.d/service start|stop|restart
# 4 : *.pid files
# 5 : ...


import socket
import subprocess
import os
import logging

# https://docs.python.org/3/howto/logging.html
logging.basicConfig(filename='/tmp/finger.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def write_pid():
    outputFile = open('/tmp/finger.pid', "w")  # https://stackoverflow.com/a/66367904
    pid = str(os.getpid())
    outputFile.write(pid)
    outputFile.close()


HOST = ''
PORT = 7979
address = (HOST, PORT)


def main():
    finger_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    finger_server.bind(address)
    finger_server.listen(0)

    while True:  # TODO handle errors
        conn, address_client = finger_server.accept()
        with conn:
            print('Accepted connection from {}:{}'.format(address_client[0], address_client[1]))
            data = str(conn.recv(1024))
            if len(data) > 0:
                command = 'finger {}'.format(data[1:])
                output = subprocess.getoutput([command])  # the commands module is deprecated since Python 2.6
                conn.send(str.encode(output))
                logging.info(f'nom de login demandé : {data}, adresse du client: {address_client[0]}')
            else:
                conn.close()
                print("client disconnected")
    finger_server.close()


write_pid()
main()

import argparse
from socket import *


FINGER_PORT = 7979


def finger(host, args):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, FINGER_PORT))
    s.send(str.encode(args))
    while True:
        buf = s.recv(1024)
        if not buf: break
        print(buf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finger client')
    parser.add_argument('-l', '--login', help='enter username to check', required=True)
    parser.add_argument('-o', '--host', help='enter the server ip', required=True)
    args = vars(parser.parse_args())
    finger(args['host'], args['login'])

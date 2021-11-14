import string
from socket import *
import getopt, sys


def usage():
    print("Usage : %s --login <login > --host <hostname > " % (sys.argv[0]))
    exit()


FINGER_PORT = 7979


def finger(host, args):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, FINGER_PORT))
    s.send(str.encode(args))
    while 1:
        buf = s.recv(1024)
        if not buf:
            break
        print(buf)




def main():
    login = gethostname()
    host = ""

    options, args = getopt.getopt(sys.argv[1:], 'l:o:h', ['login=', 'host='])
    for opt, arg in options:
        if opt in ('-l', '--login'):
            login = arg
        elif opt in ('-o', '--host'):
            host = arg
        elif opt in ('-h', '--help'):
            usage()

    if not login:
        print('login required')
        usage()
    if not host:
        print('host required')
        usage()

    finger(host, login)


main()

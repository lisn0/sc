# simple FTP server
# use multi-threading so it can handle multi FTP request
# commands
#   LIST <path>, information of a directory or file,
#   						 or information of current remote directory if not specified
#   STOR <file_name>, copy file to current remote directory
#   RETR <file_name>, retrieve file from current remote directory
# additional commands
#	QUIT, quit connection
#	PWD, get current remote directory
#   CDUP, change to parent remote directory
#   CWD <path>, change current remote directory
#   MKD, make a directory in remote server
#   RMD <dir_name>, remove a directory in remote server
#   DELE <file_name>, delete a file in remote server

import socket
import os
import sys
import threading
import time


class FTPThreadServer(threading.Thread):
    def __init__(self, client, client_address, local_ip, data_port):
        self.client = client
        self.client_address = client_address
        self.cwd = os.getcwd()
        self.data_address = (local_ip, data_port)


        threading.Thread.__init__(self)

    def start_datasock(self):
        try:
            print('Creating data socket on' + str(self.data_address) + '...')

            # create TCP for data socket
            self.datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.datasock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.datasock.bind(self.data_address)
            self.datasock.listen(5)

            print('Data socket is started. Listening to' + str(self.data_address) + '...')
            self.client.send('125 Data connection already open; transfer starting.\r\n'.encode())

            return self.datasock.accept()
        except Exception as e:
            print('ERROR: test ' + str(self.client_address) + ': ' + str(e))
            self.close_datasock()
            self.client.send('425 Cannot open data connection.\r\n')

    def close_datasock(self):
        print('Closing data socket connection...')
        try:
            self.datasock.close()
        except:
            pass

    def run(self):
        try:
            print('client connected: ' + str(self.client_address) + '\n')

            while True:
                cmd = str(self.client.recv(1024))[2:-1]
                if not cmd: break
                print('commands from ' + str(self.client_address) + ': ' + str(cmd))
                try:
                    func = getattr(self, cmd[:4].strip().upper())
                    func(cmd)
                except AttributeError as e:
                    print('ERROR: ' + str(self.client_address) + ': Invalid Command.')
                    self.client.send('550 Invalid Command\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.QUIT('')

    def QUIT(self, cmd):
        try:
            self.client.send('221 Goodbye.\r\n')
        except:
            pass
        finally:
            print('Closing connection from ' + str(self.client_address) + '...')
            self.close_datasock()
            self.client.close()
            quit()

    def LIST(self, cmd):
        print('LIST', self.cwd)
        (client_data, client_address) = self.start_datasock()

        try:
            listdir = os.listdir(self.cwd)
            if not len(listdir):
                max_length = 0
            else:
                max_length = len(max(listdir, key=len))

            header = '| %*s | %9s | %12s | %20s | %11s | %12s |' % (
            max_length, 'Name', 'Filetype', 'Filesize', 'Last Modified', 'Permission', 'User/Group')
            table = '%s\n%s\n%s\n' % ('-' * len(header), header, '-' * len(header))
            client_data.send(table.encode())

            for i in listdir:
                path = os.path.join(self.cwd, i)
                stat = os.stat(path)
                data = '| %*s | %9s | %12s | %20s | %11s | %12s |\n' % (max_length, i, 'Directory' if os.path.isdir(path) else 'File', str(stat.st_size) + 'B',time.strftime('%b %d, %Y %H:%M', time.localtime(stat.st_mtime)), oct(stat.st_mode)[-4:], str(stat.st_uid) + '/' + str(stat.st_gid))
                client_data.send(data.encode())

            table = '%s\n' % ('-' * len(header))
            client_data.send(table.encode())

            self.client.send('\r\n226 Directory send OK.\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.client.send('426 Connection closed; transfer aborted.\r\n')
        finally:
            client_data.close()
            self.close_datasock()

    def PWD(self, cmd):
        self.client.send('257 \"%s\".\r\n' % self.cwd)

    def CWD(self, cmd):
        dest = os.path.join(self.cwd, cmd[4:].strip())
        if (os.path.isdir(dest)):
            self.cwd = dest
            self.client.send('250 OK \"%s\".\r\n' % self.cwd)
        else:
            print('ERROR: ' + str(self.client_address) + ': No such file or directory.')
            self.client.send('550 \"' + dest + '\": No such file or directory.\r\n')

    def CDUP(self, cmd):
        dest = os.path.abspath(os.path.join(self.cwd, '..'))
        if (os.path.isdir(dest)):
            self.cwd = dest
            self.client.send('250 OK \"%s\".\r\n' % self.cwd)
        else:
            print('ERROR: ' + str(self.client_address) + ': No such file or directory.')
            self.client.send('550 \"' + dest + '\": No such file or directory.\r\n')

    def MKD(self, cmd):
        path = cmd[4:].strip()
        dirname = os.path.join(self.cwd, path)
        try:
            if not path:
                self.client.send('501 Missing arguments <dirname>.\r\n')
            else:
                os.mkdir(dirname)
                self.client.send('250 Directory created: ' + dirname + '.\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.client.send('550 Failed to create directory ' + dirname + '.')

    def RMD(self, cmd):
        path = cmd[4:].strip()
        dirname = os.path.join(self.cwd, path)
        try:
            if not path:
                self.client.send('501 Missing arguments <dirname>.\r\n')
            else:
                os.rmdir(dirname)
                self.client.send('250 Directory deleted: ' + dirname + '.\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.client.send('550 Failed to delete directory ' + dirname + '.')

    def DELE(self, cmd):
        path = cmd[4:].strip()
        filename = os.path.join(self.cwd, path)
        try:
            if not path:
                self.client.send('501 Missing arguments <filename>.\r\n')
            else:
                os.remove(filename)
                self.client.send('250 File deleted: ' + filename + '.\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.client.send('550 Failed to delete file ' + filename + '.')

    def STOR(self, cmd):
        path = cmd[4:].strip()
        if not path:
            self.client.send('501 Missing arguments <filename>.\r\n')
            return

        fname = os.path.join(self.cwd, path)
        (client_data, client_address) = self.start_datasock()

        try:
            file_write = open(fname, 'w')
            while True:
                data = client_data.recv(1024)
                if not data:
                    break
                file_write.write(data)

            self.client.send('226 Transfer complete.\r\n')
        except Exception as e:
            print('ERROR: ' + str(self.client_address) + ': ' + str(e))
            self.client.send('425 Error writing file.\r\n')
        finally:
            client_data.close()
            self.close_datasock()
            file_write.close()

    def RETR(self, cmd):
        path = cmd[4:].strip()
        if not path:
            self.client.send('501 Missing arguments <filename>.\r\n')
            return

        fname = os.path.join(self.cwd, path)
        (client_data, client_address) = self.start_datasock()
        if not os.path.isfile(fname):
            self.client.send('550 File not found.\r\n')
        else:
            try:
                file_read = open(fname, "r")
                data = file_read.read(1024)

                while data:
                    client_data.send(data)
                    data = file_read.read(1024)

                self.client.send('226 Transfer complete.\r\n')
            except Exception as e:
                print('ERROR: ' + str(self.client_address) + ': ' + str(e))
                self.client.send('426 Connection closed; transfer aborted.\r\n')
            finally:
                client_data.close()
                self.close_datasock()
                file_read.close()


class FTPserver:
    def __init__(self, port, data_port):
        # server address at localhost
        self.address = '0.0.0.0'

        self.port = int(port)
        self.data_port = int(data_port)

    def start_sock(self):
        # create TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (self.address, self.port)

        try:
            print('Creating data socket on', self.address, ':', self.port, '...')
            self.sock.bind(server_address)
            self.sock.listen(5)
            print('Server is up. Listening to', self.address, ':', self.port)
        except Exception as e:
            print('Failed to create server on', self.address, ':', self.port, 'because', str(e.strerror))
            quit()

    def start(self):
        self.start_sock()

        try:
            while True:
                print('Waiting for a connection')
                (client, client_address) = self.sock.accept()
                thread = FTPThreadServer(client, client_address, self.address, self.data_port)
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print('Closing socket connection')
            self.sock.close()
            quit()


# Main
port = input("Port - if left empty, default port is 10021: ")
if not port:
    port = 10021

data_port = input("Data port - if left empty, default port is 10020: ")
if not data_port:
    data_port = 10020

server = FTPserver(port, data_port)
server.start()

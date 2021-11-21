import socket
import sys
import time
import os
import struct

print("\nWelcome to the FTP server.\n\nTo get started, connect a client.")

# Initialise socket stuff
TCP_IP = "127.0.0.1" # Only a local server
TCP_PORT = 4321 # Just a random choice
BUFFER_SIZE = 1024 # Standard size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print("\nConnected to by address: {}".format(addr))


def list_files():
    print("Listing files...")
    # Get list of files inlist_files directory
    listing = os.listdir(os.getcwd())
    # Send over the number of files, so the client knows what to expect (and avoid some errors)
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    # Send over the file names and sizes whilst totaling the directory size
    for i in listing:
        # File name size
        conn.send(struct.pack("i", sys.getsizeof(i)))
        # File name
        conn.send(i.encode())
        # File content size
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        # Make sure that the client and server are syncronised
        conn.recv(BUFFER_SIZE)
    # Sum of file sizes in directory
    conn.send(struct.pack("i", total_directory_size))
    #Final check
    conn.recv(BUFFER_SIZE)
    print("Successfully sent file listing")
    return

def dwld():
    conn.send("1".encode())
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    print(file_name_length)
    file_name = conn.recv(file_name_length)
    print(file_name)
    if os.path.isfile(file_name):
        # Then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        # Then the file doesn't exist, and send error code
        print("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    # Wait for ok to send file
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    start_time = time.time()
    print("Sending file...")
    content = open(file_name, "rb")
    # Again, break into chunks defined by BUFFER_SIZE
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l.encode())
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return




def quit():
    # Send quit conformation
    conn.send("1".encode())
    # Close and restart the server
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

while True:
    # Enter into a while loop to recieve commands from client
    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE)
    print("\nRecieved instruction: {}".format(data))
    # Check the command and respond correctly
    if data == b"LIST":
        list_files()
    elif data == b"DWLD":
        dwld()
    elif data == b"QUIT":
        quit()
    # Reset the data to loop
    data = None

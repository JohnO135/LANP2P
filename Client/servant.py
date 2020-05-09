import socket, errno
import threading #Allowing for clients not to be waiting for other code
import os.path
from os import path

#from twisted.internet.protocol import Protocol

class Server:
    PORT = 5000 #Port thats not being used
    SERVER = '0.0.0.0' #This will get the IP address of local network
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    BUFFER_SIZE = 1024

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.listen()
        print(f"[Listening] Server is running on {self.SERVER}")
        while True:
            conn , addr = sock.accept() #This will wait until a new connection comes in and then stores it in connection socket variable as well as its address
            thread = threading.Thread(target=self.handle_client, args = (conn, addr)) #when a new connection occurs will creat a new thread with target function and (conn, addr) as args
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") #shows how many threads there are

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION {addr} connected")
        connected = True
        confirmation = conn.recv(self.BUFFER_SIZE).decode(self.FORMAT)
        if(confirmation.strip() == self.DISCONNECT_MESSAGE):
            print("[DISCONNECTING CLIENT]")
        else:
            print(f"[TRANSACTION WITH {addr}] File transfer initiated")
            header = conn.recv(self.BUFFER_SIZE).decode(self.FORMAT)
            filename = header.strip()
            download = open(filename, 'wb')
            while connected:
                data = conn.recv(self.BUFFER_SIZE)
                if len(data) > 0:
                    download.write(data)
                else:
                    break
            download.close()
            print(f"[TRANSACTION WITH {addr}] Download complete")
            print("[DISCONNECTING CLIENT]")
        #connection with client is closed
        conn.close()

class Client:

    HEADER = 64 #This will tell us the length of the message being sent so we can adjust our receiving quantity based off the message
    PORT = 5000 #Port thats not being used
    FORMAT = 'utf-8'

    SERVER = socket.gethostbyname(socket.gethostname()) #This will get the IP address of local network
    ADDR = (SERVER, PORT)
    BUFFER_SIZE = 1024

    #This will tell server node there will be no further packets and to close connection
    DISCONNECT_MESSAGE = "!DISCONNECT".encode(FORMAT)
    DISCONNECT_MESSAGE += b' ' * (BUFFER_SIZE - len(DISCONNECT_MESSAGE))

    #this will allow the server to know if a file is being sent over
    CONFIRMATION = "!SENDINGMSG".encode(FORMAT)
    CONFIRMATION += b' '  * (BUFFER_SIZE - len(CONFIRMATION))
    
    def __init__(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.ADDR)
        fileName = input("Enter a file please: ")
        if(path.exists(fileName)):
            client.send(self.CONFIRMATION) #this will send the confirmation custom fit to the buffer

            #This section will generate a header in to help with file creation on receiving end
            header = fileName
            header = header.encode(self.FORMAT)
            header += b' ' * (self.BUFFER_SIZE - len(header))

            #Send the header in order for proper file naming
            client.send(header)

            file = open(fileName, 'rb')
            data = file.read(self.BUFFER_SIZE)
            while data:
                print("Sending...")
                client.send(data)
                data = file.read(1024)
            file.close()
            print("Done Sending")
        #if the file was not found it will simply send the disconnect message
        else:
            print("file not found")
            client.send(self.DISCONNECT_MESSAGE)
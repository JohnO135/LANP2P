import socket
import os.path
from os import path

HEADER = 64 #This will tell us the length of the message being sent so we can adjust our receiving quantity based off the message
PORT = 5000 #Port thats not being used
FORMAT = 'utf-8'

SERVER = "192.168.1.180" #This will get the IP address of local network
ADDR = (SERVER, PORT)
BUFFER_SIZE = 1024

#This will tell server node there will be no further packets and to close connection
DISCONNECT_MESSAGE = "!DISCONNECT".encode(FORMAT)
DISCONNECT_MESSAGE += b' ' * (BUFFER_SIZE - len(DISCONNECT_MESSAGE))

#this will allow the server to know if a file is being sent over
CONFIRMATION = "!SENDINGMSG".encode(FORMAT)
CONFIRMATION += b' '  * (BUFFER_SIZE - len(CONFIRMATION))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(fileName):
    #if the file exists within the current directory it will enter loop
    if(path.exists(fileName)):
        client.send(CONFIRMATION) #this will send the confirmation custom fit to the buffer

        #This section will generate a header in to help with file creation on receiving end
        header = fileName
        header = header.encode(FORMAT)
        header += b' ' * (BUFFER_SIZE - len(header))

        #Send the header in order for proper file naming
        client.send(header)

        file = open(fileName, 'rb')
        data = file.read(BUFFER_SIZE)
        while data:
            print("Sending...")
            client.send(data)
            data = file.read(1024)
        file.close()
        print("Done Sending")
    #if the file was not found it will simply send the disconnect message
    else:
        print("file not found")
        client.send(DISCONNECT_MESSAGE)

userin = str(input("Please enter the file name you wish to send: "))
send(userin)
client.close()
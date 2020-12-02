import socket
import os
import shutil

#Creating a socket with IPv4 protocol and TCP transport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Will bind the socket to a port number
s.bind(('10.0.0.2', 9992))

#If server is overloaded, can have a queue of 5
s.listen(5)

#If a connection comes in, accept the client
clientsocket, address = s.accept()


#Sending bytes to the server, text of data type utf-8
clientsocket.send(bytes("Welcome to the server!", "utf-8"))



while True:
    #Will obtain the option number from the menu found in client
    opRaw = clientsocket.recv(1024)
    op = opRaw.decode("utf-8")

    #Case 1: Will list the files in the directory
    if(op == '1'):
        dir_name = r'/home/mininet/Server'
        fileList = ""

        #will send list of files found in the directory
        for file in os.listdir(dir_name):
            fileList += ("\n" + file)

        clientsocket.send(bytes(fileList, "utf-8"))

    #Case 2: A specified file will be copied in the same directory
    if(op == '2'):
        dir_name = r'/home/mininet/Server'
        suffix = ".txt"

        #Will send the prompt to the client
        clientsocket.send(bytes("Which file would you like to copy?", "utf-8"))
        fileRaw = clientsocket.recv(1024)
        file = fileRaw.decode("utf-8")
        location1 = os.path.join(dir_name, file)

        #If the file exists, then create the copy, else inform user that file does not exist
        if(os.path.exists(location1)):
            fileSplit = file.split(".")
            copy = fileSplit[0] + "_copy." + fileSplit[1]
            location2 = os.path.join(dir_name, copy)
            shutil.copyfile(location1, location2)
            clientsocket.send(bytes(copy, "utf-8"))
        else:
            clientsocket.send(bytes("File does not exist", "utf-8"))

    #Case 3: Will rename a speicified file
    if(op == '3'):
        dir_name = r'/home/mininet/Server'

        #Will prompt to the client and store the response
        clientsocket.send(bytes("Which file would you like to rename?", "utf-8"))
        fileRaw = clientsocket.recv(1024)
        file = fileRaw.decode("utf-8")
        location1 = os.path.join(dir_name, file)

        #If the file exists, then prompt for the new file name and change the name.
        # If the file does not exist, let the user know
        if(os.path.exists(location1)):
            clientsocket.send(bytes("What would you like the new name of the file to be?", "utf-8"))
            nameRaw = clientsocket.recv(1024)
            name = nameRaw.decode("utf-8")
            location2 = os.path.join(dir_name, name)
            os.rename(location1, location2)
        else:
            clientsocket.send(bytes("File does not exist", "utf-8"))

    #Case 4: Will delete a file found in the directory
    if(op == '4'):

        #Will prompt the client for the file to be removed and store the input
        clientsocket.send(bytes("Which file would you like to remove?", "utf-8"))
        fileRaw = clientsocket.recv(1024)
        file = fileRaw.decode("utf-8")

        #If file exists, then remove the file and let user know it was Successful
        # if not, then let the user know that the file did not exist
        if os.path.exists(file):
            os.remove(file)
            clientsocket.send(bytes("Successfully removed file", "utf-8"))
        else:
            clientsocket.send(bytes("File does not exist", "utf-8"))


s.close()

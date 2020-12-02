import socket

#Creating a socket with IPv4 protocol and TCP transport
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Will connect to the local host name and port
s.connect(('10.0.0.2', 9992))

#Buffer, will receive 1024 bytes at a time
msg = s.recv(1024)

#Data is received as bytes so have to decode them.
print(msg.decode("utf-8"))

#Setting a continous while loop will allow the client to send consecutive commands
#rather than a one command per client scenario.
while True:
    print("\nWhat operation would you like to do?\n")
    print("0 EXIT")
    print("1 Files in directory")
    print("2 Copy a File")
    print("3 Rename a File")
    print("4 Delete a File")

    #Obtains mmenu option and will send to server
    op = input()
    s.send(bytes(op, "utf-8"))

    #Case 0: Quit the client, will exit the while loop
    if(op == '0'):
        break

    #Case 1: Will list the files in the directory
    if(op == '1'):
        print("\nList of files found in directory: ")

        #Will receive a list of all the files in the directory
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

    #Case 2: A specified file will be copied in the same directory
    if(op == '2'):

        #Prompt asking for the file wanted to be copied
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

        #Will send the file nmae that is to be copied
        file = input()
        s.send(bytes(file, "utf-8"))

        #The response from the server, will either receive the copy name or
        # error when file does not exist
        responseMsgRaw = s.recv(1024)
        responseMsg = responseMsgRaw.decode("utf-8")
        if(responseMsg == "File does not exist"):
            print("\nFile does not exist")
        else:
            print("\nCopied File Named as: " + responseMsg)

    #Case 3: Will rename a speicified file
    if(op == '3'):
        #Will receive prompt asking for the file to be renamed
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

        #WIll send the file name that needs to be renamed
        file = input()
        s.send(bytes(file, "utf-8"))

        #The response from the server, will either confirm that the file exists and ask
        # for the new name of the file, or will inform the user that the file does not exist
        responseMsgRaw = s.recv(1024)
        responseMsg = responseMsgRaw.decode("utf-8")
        if(responseMsg == "File does not exist"):
            print("\nFile does not exist")
        else:
            print(responseMsg)
            name = input()
            s.send(bytes(name, "utf-8"))

    #Case 4: Will delete a file found in the directory
    if(op == '4'):
        #Will receive the prompt asking for file to be deleted
        msg = s.recv(1024)
        print(msg.decode("utf-8"))

        #Will send the name of the file to be removed.
        file = input()
        s.send(bytes(file, "utf-8"))

        #Will either show that the file was Successfully deleted or the file does not exist
        responseMsgRaw = s.recv(1024)
        print(responseMsgRaw.decode("utf-8"))

s.close()

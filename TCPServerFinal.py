from socket import *


def main():
    # Prepare a sever socket This is on page 167
    serverSocket = socket(AF_INET, SOCK_STREAM)         # create socket
    # associate port with socket
    serverSocket.bind(('', 31001))
    # listen for 1 connection
    serverSocket.listen(1)
# ——
    while True:
        # Establish the connection
        # DEBUG: proof server is ready
        print('Ready to serve…')
        # create connection socket for accepted client
        connectionSocket, addr = serverSocket.accept()
# ———-
        try:
            message = connectionSocket.recv(1024)       # recieve messg
            # DEBUG: proof connection is made
            print('I am message!>>', message)

            filename = message.split()[1]               # determine filename
            # DEBUG: to check filename
            print('I am filename!>>', filename)
            f = open(filename[1:])                      # open the file

            # outputdata = data in the file requested
            outputdata = f.read()
            # DEBUG: to check outputdata
            print(outputdata)

            # Send one HTTP header line into socket
            connectionSocket.send('\n'.encode())
            connectionSocket.send('HTTP/1.1 200 OK\n'.encode())
            connectionSocket.send('Connection: close\n'.encode())
            # I need to put in the right size and send it out
            LengthString = 'Content-Length: '+str(len(outputdata))+'\n'
            connectionSocket.send(LengthString.encode())
            connectionSocket.send('Content-Type: text/html\n'.encode())
            connectionSocket.send('\n'.encode())
            connectionSocket.send('\n'.encode())

            # Send the content of the requested file to the client
            for i in range(0, len(outputdata)):         # for all the output data
                connectionSocket.send(
                    outputdata[i].encode())    # send the data
            connectionSocket.close()                    # close connection
        except IOError:                                 # if IOError
            print('IOERROR')                             # DEBUG: signal error
            # Send response message for file not found
            connectionSocket.send('\n'.encode())
            error404 = '404 Not Found: Requested document not found'
            connectionSocket.send(error404.encode())
            connectionSocket.close()                    # close connection

    serverSocket.close()
    pass


if __name__ == '__main__':
    main()

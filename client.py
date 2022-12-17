# Create a socket and connect to the server
import socket
import os

def sendData(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.29.201.238", 4338))
        
        # Send the name of the file
        data = data[2].replace("/",'\\')
        filename = os.getcwd() +"\\" +data
        file = filename.split("\\")[-1]+"\0"
        s.send(file.encode())

        # Send the file
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.send(data)
            
        # Close the connection
        s.close()
        print("Done")
        return("Success")
    except Exception as e:
        return e

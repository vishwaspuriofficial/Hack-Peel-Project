# send data to the server

import socket
import os
import zeroconf
import zeroconf.asyncio

# # Get the ip address of the server using zeroconf
# instance = zeroconf.Zeroconf()
# # listen for all services
# browser = zeroconf.ServiceBrowser(instance, "_http._tcp.local.", handlers=[service_state_change])
# # print all service names
# for service in instance.services_by_type("_http._tcp.local."):
#     print(service)

# info = instance.get_service_info("_http._tcp.local.", "CameraServer._http._tcp.local.")
# address = socket.inet_ntoa(info.address)
# port = info.port

address = "localhost"
port = 4338


# Create a socket and connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))

# Send the name of the file
filename = "test.jpg"
s.send(filename.encode())

# Send the file
with open(filename, 'rb') as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        s.send(data)
    
# Close the connection
s.close()


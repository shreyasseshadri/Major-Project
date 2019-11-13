import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with" + err)
port = 80

try:
    host_ip = socket.gethostbyname('www.google.com')
except socket.gaierror:
    print("there was an error resolving the host")
    sys.exit()

s.connect((host_ip, port))
print("the socket has successfully connected to google on port  " + host_ip)

a = ["1","2"] #TOK str
b = [i for i in range(3)] #TOK num
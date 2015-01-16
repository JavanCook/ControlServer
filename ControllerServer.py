#Import socket and time
import socket
import itertools
from time import gmtime, strftime

#Create control binaries
binaries = list(itertools.product(range(2), repeat = 8))

#Allows multiple connects/disconnects
while True:
 #Setup TCP server
 bindIP = '192.168.1.70'
 bindport = 9235
 connectIP = '192.168.1.66'
 connectport = 9234
 packetsize = 70
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.bind((bindIP, bindport))
 #s.connect((connectIP, connectport))
 s.listen(1)

 #Receive and acknowledge remote connection
 conn, addr = s.accept()
 print(addr , 'connected', strftime("%a, %d, %b %Y %H:%M:%S", gmtime()))
 ackn = conn.recv(packetsize)
 conn.send(ackn)

 #Control input loop
 while True:
  try:
   data = conn.recv(packetsize)
   conn.send(data)
   #Translate into callable list
   decoded = data.decode()
   print(decoded)
   listed = data.split()
   #for x in range(1,257):
    #Start, back, d-pad and analogue clicks
    #if listed[0].decode() == str(x):
     #print(binaries[x])
    #Xbox button, shoulder buttons, A, B, X and Y
    #if listed[1].decode() == str(x):
     #print(binaries[x])
   #Left trigger
   #if int(listed[2].decode()) >= 150:
    #print('left trigger') 
   #Right trigger
   #if int(listed[3].decode()) >= 150:
    #print('right trigger')
  #Handles shutdown by peer error
  except socket.error as e:
   if e.errno == 104:
    print(addr , 'disconnected', strftime("%a, %d, %b %Y %H:%M:%S", gmtime()))
    break

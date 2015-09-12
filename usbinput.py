#Import PyUSB, sys, array, socket, re and time
import usb.core
import usb.util
import sys
import array
import socket
import re
import time

#Find device
dev = usb.core.find(idVendor=0x045e, idProduct=0x028e)
#Is the controller there or not?
if dev is None:
 sys.exit('Controller not present, please insert and try again.')
else:
 print('Controller present.')

#Configure device
dev.set_configuration()

#Controller light status
packet1 = dev.read(0x81, 32, 100)
#Misc packets
packet2 = dev.read(0x81, 32, 100)
packet3 = dev.read(0x81, 32, 100)
#Headset present?
packet4 = dev.read(0x81, 32, 100)
#Controls status
packet5 = dev.read(0x81, 32, 100)

#Converts packet5 to send over TCP
blank = []
for filler in range(1,20):
 initialiser = blank.append(packet5[filler])
stringed = str(initialiser).strip('[]')

#Is the mic there or not?
if packet4 == array.array('B', [8, 3, 0]):
 print('Mic not present at start.')
else:
 print('Mic present.')

#Setup TCP communication
bindIP = '192.168.1.66'
bindport = 9234
connectIP = '192.168.1.70'
connectport = 9235
packetsize = 32
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
attemptlist = []

#Check connection to server
for x in range(1,6):
 try:
  s.connect((connectIP, connectport))
  s.send(stringed.encode())
  ack = s.recv(packetsize)
  if len(ack) > 1:
   #Player one light flash then on
   dev.write(0x1, [1, 3, 2], 100)
   print('Connected to server.')
  break
 #Handles refused connection error
 except socket.error as d:
  if d.errno == 111:
   print('No connection to server, attempt number.', x)
   #attempt connection five times with two second intervals
   time.sleep(2)
   attemptlist.append(x)

#Closes program and turns off controller light if connection fails five times
if len(attemptlist) == 5:
 dev.write(0x1, [1, 3, 0], 100)
 sys.exit('Connection failed, please try again.')

print('To exit press: LB+RB+Back.')

#Control loop
while True:
 #Controller packets
 try:
  cstatus = dev.read(0x81, 32, 100)
  #Identifies, encodes and transmits controller report
  if cstatus[0] == 0:
   transmission = []
   try:
    for x in range(2, 6):
     transmission.append(cstatus[x])
    #Combines the four analogue stick bytes into two bytes, x and y
    bihte1 = cstatus[6]
    bihte2 = cstatus[7]
    combit1 = 256*int(bihte1) + int(bihte2)
    transmission.append(combit1)
    bihte3 = cstatus[8]
    bihte4 = cstatus[9]
    combit2 = 256*int(bihte3) + int(bihte4)
    transmission.append(combit2)
    bihte5 = cstatus[10]
    bihte6 = cstatus[11]
    combit3 = 256*int(bihte5) + int(bihte6)
    transmission.append(combit3)
    bihte7 = cstatus[12]
    bihte8 = cstatus[13]
    combit4 = 256*int(bihte7) + int(bihte8)
    transmission.append(combit4)
    strung = str(transmission).strip('[]')
    stung = re.sub(',', '', strung)
    s.send(stung.encode())
    #Exit button combo
    if cstatus[2] == 32 and cstatus[3] == 3:
     time.sleep(1)
     s.close()
     dev.write(0x1, [1, 3, 0], 100)
     sys.exit('Exit combo used.')
   #Handles bad file descriptor on exit
   except socket.error as f:
    if f.errno == 9:
     dev.write(0x1, [1, 3, 0], 100)
     sys.exit('Exit combo used.')
  #Handles change in mic status
  if cstatus == array.array('B', [8, 3, 0]):
   print('Mic removed.')
  if cstatus == array.array('B', [8, 3, 2]):
   print('Mic attached.')
 #Handles the timeout exception
 except usb.core.USBError as e:
  if e.errno == 110:
   nothing = 'matters'
 #How often it scans for changes
 time.sleep(0.5)

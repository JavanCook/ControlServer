#Import socket, itertools, GPIO and time
import socket
import itertools
import RPi.GPIO as GPIO
from time import gmtime, strftime

#Setup GPIO and control values
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
lsb = 7
rsb = 12
xbb = 11
bl = 13
Ab = 35
Bb = 36
Xb = 37
Yb = 38
du = 7
dd = 12
dl = 11
dr = 13
st = 35
ba = 36
las = 37
ras = 38
rtr = 36
ltr = 11
buttonset1 = (ras, las, ba, st, dr, dl, dd, du)
buttonset2 = (Yb, Xb, Bb, Ab, bl, xbb, rsb, lsb)

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
   listed = data.split()
   #for x in range(0,256):
    #Start, back, d-pad and analogue clicks
    #if listed[0].decode() == str(x):
     #GPIO.setup(buttonset1, GPIO.OUT)
     #GPIO.output(buttonset1, binaries[x])
    #Xbox button, shoulder buttons, A, B, X and Y
    #if listed[1].decode() == str(x):
     #GPIO.setup(buttonset2, GPIO.OUT)
     #GPIO.output(buttonset2, binaries[x])
   #Left trigger
   if int(listed[2].decode()) >= 150:
    GPIO.setup(ltr, GPIO.OUT)
    GPIO.output(ltr, 1)
   else:
    GPIO.setup(ltr, GPIO.OUT)
    GPIO.output(ltr, 0)
   #Right trigger
   if int(listed[3].decode()) >= 150:
    GPIO.setup(rtr, GPIO.OUT)
    GPIO.output(rtr, 1)
   else:
    GPIO.setup(rtr, GPIO.OUT)
    GPIO.output(rtr, 0)
   #Left analogue stick
   #Right analogue stick
  #Handles shutdown by peer error
  except socket.error as e:
   if e.errno == 104:
    GPIO.cleanup()
    print(addr , 'disconnected', strftime("%a, %d, %b %Y %H:%M:%S", gmtime()))
    break

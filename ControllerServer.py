import socket

BIND_IP = '192.168.1.70'
BIND_PORT = 9235
CONNECT_IP = '192.168.1.66'
CONNECT_PORT = 9234
BUFFER_SIZE = 70

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((BIND_IP, BIND_PORT))
#s.connect((CONNECT_IP, CONNECT_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
while 1:
 data = conn.recv(BUFFER_SIZE)
 if not data: break
 print('recieved data:', data.decode())
 list = data.split()
 print(list)
 conn.send(data)
#conn.close
#s.close()

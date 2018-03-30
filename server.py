import socket
import pickle
import time

host = ''        # Symbolic name meaning all available interfaces
port = 12347     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print (host, port)
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    
    kontrolcu = pickle.loads(data)

    if kontrolcu[0] == 1:
        print("ileri")
    
    print (pickle.loads(data))
    conn.sendall(data)
    

conn.close()

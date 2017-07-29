import socket
import RPi.GPIO as GPIO
from threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.1.9"
port = 8000
print (host)
print (port)

serversocket.bind((host, port))

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            data = self.sock.recv(1024).decode()
            print(data)
            self.sock.send(b'Oi you sent something to me')
            if data == 'w':
                GPIO.output(27, GPIO.HIGH)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                GPIO.output(10, GPIO.LOW)
            elif data == 's':
                GPIO.output(23, GPIO.HIGH)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(10, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
            elif data == 'a':
                GPIO.output(22, GPIO.HIGH)
                GPIO.output(10, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)
            elif data == 'd':
                GPIO.output(10, GPIO.HIGH)
                GPIO.output(22, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                GPIO.output(27, GPIO.LOW)

            GPIO.cleanup()

serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)

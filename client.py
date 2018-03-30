import socket
import pickle
import pygame
import time

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print('Initialized Joystick : %s' % j.get_name())

host = "localhost"
port = 12347                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))


def get():
    out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    it = 0  # iterator
    pygame.event.pump()
    #Read input jo
    for i in range(0, j.get_numaxes()):
        out[it] = int(round(j.get_axis(i) * 100))
        it += 1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out



while True:
    print('Sending',get())
    s.sendall(pickle.dumps(get()))
    data = s.recv(1024)
    print('Received', repr(pickle.loads(data)))
    time.sleep(0.1)


import socket
import pickle
import time
import sys
import pygame

argc = len(sys.argv)
if argc < 2:
    print("Eksik arguman girisi! \n Kullanim: \n python tcp_client.py ip_adresi \n")
    exit()


#####################################################################
host = sys.argv[1]
port = 666                   # Sunucuda kullanılan port ile aynı
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
########################### pygame joystick init ##########################################

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print('Initialized Joystick : %s' % j.get_name())

#####################################################################


def get():
    out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    it = 0  
    pygame.event.pump()
    #stick okuma
    for i in range(0, j.get_numaxes()):
        out[it] = int(round(j.get_axis(i) * 400))
        it += 1
    #Butından okuma
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it += 1
    return out

try:
    while True:
        try:
            print('Sending', get())
            s.sendall(pickle.dumps(get()))
        except s.error:
            connected = False
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Bağlantı kaybedildi... yeniden bağlanılıyor \nconnection lost... reconnecting ")
            while not connected:
                try:
                    s.connect((host, port))
                    connected = True 
                    print("re-connection successful") 
                except socket.error:
                    sleep(2)
                                                          
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program kapatılıyor\nShutdown")
    s.close()

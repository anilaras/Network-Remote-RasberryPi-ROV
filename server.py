import socket
import pickle
import time
import pigpio
import ms5837

STOP_PULSE = 1500
SAG_MOTOR = 17
SOL_MOTOR = 18


host = ''        # Symbolic name meaning all available interfaces
port = 12347     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print (host, port)
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

sensor = ms5837.MS5837_30BA()
pi = pigpio.pi()
if not pi.connected:
       exit()


def Motor(fuc):
    Stopped = 1500
    if (fuc < 1):
        return Stopped + fuc
    elif (fuc > 1):
        return Stopped + fuc



#####################################################################
def donusKontrol(deger):
    if deger > 1:
        deger_sag = deger + STOP_PULSE
        print("birinci motor", deger_sag) #burada sagdaki motor escsi pwm ile sürülecek, şimdilik raspberry pi üzerinde çalışmadığım için print ile değerleri yazdırmayı tercih ettim. Pi üzerinde çalışırken burada gpio.write gibi bir değer olacak.
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_sag)
        deger_sol = STOP_PULSE - deger
        print("ikinci motor", deger_sol)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_sol)
    elif deger < 1:
        deger_sag = 1500 + deger
        print("birinci motor", deger_sag)
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_sag)
        deger_sol = (deger * -1) + 1500
        print("ikinci motor", deger_sol)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_sol)
    else:
        pi.set_servo_pulsewidth(17,STOP_PULSE)
        pi.set_servo_pulsewidth(18,STOP_PULSE)
#####################################################################



def main():
    while True:
        data = conn.recv(1024)
        if not data:
            break


        kontrolcu = pickle.loads(data)
        dalis = kontrolcu[0]
        donus = kontrolcu[1]
        print(pickle.loads(data))
        conn.sendall(data)


if __name__ == '__main__':
    main()

conn.close()

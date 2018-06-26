import socket
import pickle
import time
import sys
import pigpio
#import ms5837

STOP_PULSE = 1500
SAG_MOTOR = 17
SOL_MOTOR = 18
DALIS_MOTOR = 19 #sonra değişecek 19 hangi pin pwm var mı bilmiyorum?

host = ""        # Symbolic name meaning all available interfaces
port = 666     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print (host, port)
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

#sensor = ms5837.MS5837_30BA()
pi = pigpio.pi()
if not pi.connected:
       exit()


def Motor(fuc):
    Stopped = 1500
    if (fuc < 1):
        return Stopped + fuc
    elif (fuc > 1):
        return Stopped + fuc


#Dönüş yönü ve İleri hareketi kontrol eden fonksiyon
#####################################################################
def donusKontrol(deger,hiz,ileri):
    if (deger > 1 and ileri == 0):
        deger_sag = deger + STOP_PULSE
        print("sag motor", deger_sag) #burada sagdaki motor escsi pwm ile sürülecek, şimdilik raspberry pi üzerinde çalışmadığım için print ile değerleri yazdırmayı tercih ettim. Pi üzerinde çalışırken burada gpio.write gibi bir değer olacak.
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_sag)
        deger_sol = STOP_PULSE - deger
        print("sol motor", deger_sol)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_sol)
    elif (deger < 1 and ileri == 0):
        deger_sag = 1500 + deger
        print("sag motor", deger_sag)
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_sag)
        deger_sol = (deger * -1) + 1500
        print("sol motor", deger_sol)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_sol)
    elif (ileri == 1):
        deger_ileri = STOP_PULSE + hiz
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_ileri)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_ileri)
        print("iki motor tam güç ileri : ", deger_ileri)
    else:
        pi.set_servo_pulsewidth(17,STOP_PULSE)
        pi.set_servo_pulsewidth(18,STOP_PULSE)
#####################################################################

#Dalış kontrolü yapan fonksiyon
#####################################################################
def dalisKontrol(deger):
    if deger > 1:
        deger_dal = deger + STOP_PULSE
        print("çık motor", deger_dal) #burada sagdaki motor escsi pwm ile sürülecek, şimdilik raspberry pi üzerinde çalışmadığım için print ile değerleri yazdırmayı tercih ettim. Pi üzerinde çalışırken burada gpio.write gibi bir değer olacak.
        pi.set_servo_pulsewidth(DALIS_MOTOR,deger_dal)
        pi.set_servo_pulsewidth(DALIS_MOTOR,deger_dal)
    elif deger < 1:
        deger_dal = STOP_PULSE + deger
        print("dal motor", deger_dal)
        pi.set_servo_pulsewidth(SAG_MOTOR,deger_dal)
        pi.set_servo_pulsewidth(SOL_MOTOR,deger_dal)
    else:
        pi.set_servo_pulsewidth(17,STOP_PULSE)
        pi.set_servo_pulsewidth(18,STOP_PULSE)
#####################################################################



def main():
#    if not sensor.init():
#        print "Sensor could not be initialized"
#        exit(1)
    
    while True:
        data = conn.recv(1024)
        if not data:
            break


        kontrolcu = pickle.loads(data)
        dalis = kontrolcu[3]
        donus = kontrolcu[0]
        ileri_hiz = kontrolcu[1]
        ilerimi = kontrolcu[9]
        donusKontrol(donus,ileri_hiz,ilerimi)
        dalisKontrol(dalis)
        print(pickle.loads(data))
        conn.sendall(data)

 #       if sensor.read():    
 #           sens_data = [sensor.pressure(), sensor.pressure(ms5837.UNITS_psi), sensor.temperature(), sensor.temperature(ms5837.UNITS_Farenheit))]    
 #           conn.sendall(pickle.dumps(sens_data))




if __name__ == '__main__':
    main()

conn.close()


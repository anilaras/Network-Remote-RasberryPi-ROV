#! /usr/bin/python3

import socket
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="192.168.1.8"
port =8000
s.connect((host,port))

while 1:

    r = getch()
    #ts(s)
    if r == 'w':
        s.send('w'.encode()) 
        data = ''
        data = s.recv(1024).decode()
        print (data)
    elif r == 's':
        s.send('s'.encode()) 
        data = ''
        data = s.recv(1024).decode()
        print (data)

    elif r == 'a':
        s.send('a'.encode()) 
        data = ''
        data = s.recv(1024).decode()
        print (data)

    elif r == 'd':
        s.send('d'.encode()) 
        data = ''
        data = s.recv(1024).decode()
        print (data)
    
    s.send('0'.encode())
   #else:
    #    s.send('0'.encode()) 
     #   data = ''
     #   data = s.recv(1024).decode()
      #  print (data)
s.close ()

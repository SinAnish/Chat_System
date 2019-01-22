import socket,subprocess,os
from threading import Thread

clients = []

def client():
    global s
    global name
    global s_data

    try:
        ip = input('Connect to ip: ')
        port = int(input('Connect to port: '))

        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.settimeout(0.001)

        print('Successfully Connected.')

        name = input('What is your name? ')

        print('Type "q" in chat and hit enter to quit/leave.')

        s_data = ''
        c_r = Thread(target = client_recv,args = ('a','b'))
        c_r.start()

        s_data = input('{}: '.format(name))
        while s_data != 'q':
            s.sendto('{}: {}'.format(name,s_data).encode(),(ip,port))
            s_data = input('{}: '.format(name))
    finally:
        s.sendto('quit'.encode(),(ip,port))
        #print('client quitting')

def client_recv(a,b):
    global s
    global name
    global s_data
    while s_data != 'q':
        try:
            r_data,addr = s.recvfrom(1024)
        except socket.timeout:
            pass
        else:
            if r_data.decode()[:len(name)] != name:
                print('\r{}\n{}: '.format(r_data.decode(),name),end = '')
                os.system('osascript -e \'beep\'')
    #print('client_recv quitting')

def server():
    global s
    global name
    global s_data
    ip = socket.gethostbyname(socket.gethostname())
    port = 0

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((ip,port))
    s.settimeout(0.001)

    print('Successfully Connected.')
    print('Server hosted on ip address: {} with port: {}'.format(s.getsockname()[0],s.getsockname()[1]))

    name = input('What is your name? ')

    print('Type "q" in chat and hit enter to quit/leave.')

    s_data = ''
    s_r = Thread(target = server_recv,args = ('a','b'))
    s_r.start()

    s_data = input('{}: '.format(name))
    while s_data != 'q':
        for c in clients:
            s.sendto('{}: {}'.format(name,s_data).encode(),c)
        s_data = input('{}: '.format(name))
    #print('server quitting')

def server_recv(a,b):
    global s
    global name
    global s_data
    while s_data != 'q':
        try:
            r_data,addr = s.recvfrom(1024)
        except socket.timeout:
            pass
        else:

            if addr not in clients:
                clients.append(addr)

            if r_data.decode() != 'quit':
                print('\r{}\n{}: '.format(r_data.decode(),name),end = '')
                for c in clients:
                    s.sendto(r_data,c)
                os.system('osascript -e \'beep\'')
            elif r_data.decode() == 'quit':
                clients.remove(addr)

    #print('server_recv quitting')

subprocess.call(['tput','reset'])

mode = input('Welcome to the Chat System by Genki Asahi!\nType the key and hit enter to select the mode.\n[j] Join an existing chat server/room | [n] Create a new chat server/room\n')

subprocess.call(['tput','reset'])

if mode.lower() == 'n':
    server()
elif mode.lower() == 'j':
    client()
else:
    print('Error: Unknown Selection')

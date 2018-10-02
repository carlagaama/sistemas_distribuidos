#!/usr/bin/python3

from threading import Thread
import time
import os
import socket

def client_thread(threadPID):
    #GAMBIARRRAAAAAAAAAAAA
    time.sleep(0.5)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    server_address = ('localhost', 10000+os.getpid())
    sock.connect(server_address)

    try:
        message = 'NOTICE ME SENPAI'
        print ('[CLIENT - '+threadPID+'] sending "%s"' % message)
        sock.sendall(message.encode())

        while True:
            print ("[CLIENT - "+threadPID+"] Esperando ACKS...")
            try:
                data, server = sock.recvfrom(64)
                print("[CLIENT - "+threadPID+"] server: " + str(server))
            except socket.timeout:
                print ("[CLIENT - "+threadPID+"] TIMED OUT")
                break
            else:
                print ("[CLIENT - "+threadPID+"] recebido %s de %s" % (data.decode(), server))
    finally:
        print ('[CLIENT - '+threadPID+'] closing socket')
        sock.close()

def server_thread(threadPID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 10000+os.getpid()))

    while True:
        print("[SERVER] Escutando...")
        sock.listen(1)
        conn, address = sock.accept()
        data = conn.recv(64).decode()

        print("[SERVER] recebi: " + str(data))
        print("[SERVER] Enviando ack...")
        print("[SERVER] endereço: " + str(address))

        #delete address, it doesn't help our cause
        conn.sendto('ACK do processo X'.encode(), address)

try:
    thread_server = Thread(target=server_thread, args=(str(os.getpid()),))
    thread_client = Thread(target=client_thread, args=(str(os.getpid()),))
    thread_server.start()
    thread_client.start()
except:
    print("Error: unable to start thread")

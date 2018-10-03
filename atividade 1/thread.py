#!/usr/bin/python3

import threading
import time
import socket
import sys

class client(threading.Thread):
   def __init__(self, procID):
      threading.Thread.__init__(self)
      self.procID = procID

   def run(self):
      for i in range(1, (total_process+1)):
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            server_address = ('localhost', 2000 + i)
            sock.connect(server_address)
            sock.send(self.procID.encode())
            try:
               data, server = sock.recvfrom(64)
               print("Recebi o ACK do Processo: ", str(data.decode()))
            finally:
               sock.close()
         except socket.timeout:
            print("TIME OUT!")
         finally:
            sock.close()

class server(threading.Thread):
   def __init__(self, procID):
      threading.Thread.__init__(self)
      self.procID = procID
      self.list = []

   def run(self):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', (2000+int(sys.argv[1]))))
      sock.listen(1)
      print("[PROCESSO - "+self.procID+"] ouvindo....")

      while True:
         conn, address = sock.accept()
         data = conn.recv(64).decode()

         import pdb
         pdb.set_trace()

         print("LISTA ANTES DO ACK: " + str(self.list))

         print("Recebido mensagem do processo: " + str(data))
         if (data not in self.list) and (data is not self.procID):
            for i in range(1, (total_process+1)):
               try:
                  sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  server_address = ('localhost', 2000 + i)
                  sock_server.connect(server_address)
                  sock_server.send(self.procID.encode())
                  
                  print("Enviando ACK para processo: "+str(i))
                  conn.send((data).encode())
                  (self.list).append(i)
                  print("LISTA DEPOIS DO ACK: " + str(self.list))
         
               finally:
                  sock_server.close()

total_process = 3
procID = sys.argv[1]

op = client(procID)
dp = server(procID)
dp.start()

input("Pressione enter pra começar!\n")
print("Começou!")
op.start()

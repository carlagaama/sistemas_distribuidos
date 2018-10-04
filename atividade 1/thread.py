#!/usr/bin/python3

import threading
import time
import socket
import sys
import json

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
            x = {
               "msg": self.procID,
               "ack": 0,
               "time": (time.time() * 1000.0),
               "id": self.procID
            }
            sock.send(json.dumps(x).encode())
            
           # try:
           #    data, server = sock.recvfrom(64)
           #    print(data)
           #    print("Recebi o ACK do Processo: ", str(data.decode()))
           # finally:
           #    sock.close()
         except socket.timeout:
            print("TIME OUT!")
         finally:
            sock.close()

class server(threading.Thread):
   def __init__(self, procID):
      threading.Thread.__init__(self)
      self.procID = procID
      self.list_msg = set([])

   def run(self):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', (2000+int(sys.argv[1]))))
      sock.listen(1)
      print("[PROCESSO - "+self.procID+"] ouvindo....")
      while True:
         conn, address = sock.accept()
         data = conn.recv(1024).decode()

         y = json.loads(data)

         if not y["ack"]:
            print("A mensagem chegou para mim no tempo: "+str(y["time"]))
            self.list_msg.add(procID)
            sorted(self.list_msg)
            print(str(self.list_msg))
            for i in range(1, (total_process+1)):
               try:
                  sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  server_address = ('localhost', 2000+i)
                  sock_server.connect(server_address)
                  x = {
                     "ack": 1,
                     "time": (time.time() * 1000.0),
                     "id": self.procID
                  }
                  print("ENVIEI ACK PARA O MEU SENHOR PROCESSO "+str(i))
                  sock_server.send(json.dumps(x).encode())
                  
               except Exception as e:
                  print(e)
                  
         elif y["ack"] == 1 and procID in self.list_msg:
            print("Recebi ACK do Processo " + y["id"] + " no tempo: " + str(y["time"]))
            
      
      if(len(self.list_ack) == total_process):
            print("Enviado para aplicação de cima ^")
         

total_process = 3
procID = sys.argv[1]

op = client(procID)
dp = server(procID)
dp.start()

input("Pressione enter pra começar!\n")
print("Começou!")
op.start()

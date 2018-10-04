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
      self.lamp = procID
      print("Meu clock é: "+(self.lamp)+"\n")

   def run(self):
      self.lamp = str(int(self.lamp) + 1)
      print("Começou no tempo: "+self.lamp+self.procID)

      for i in range(1, (total_process+1)):
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            server_address = ('localhost', 1000 + i)
            sock.connect(server_address)
            time = i + int(self.lamp)
            print("Enviei a mensagem no tempo: "+str(time)+self.procID)
            x = {
               "msg": self.procID,
               "ack": 0,
               "time": time,
               "id": self.procID,
               "origem": self.procID
            }
            sock.send(json.dumps(x).encode())
            
         except socket.timeout:
            print("TIME OUT!")
         finally:
            sock.close()

class server(threading.Thread):
   def __init__(self, procID):
      threading.Thread.__init__(self)
      self.procID = procID
      self.lamp = '0'
      
   def run(self):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', (1000+int(sys.argv[1]))))
      sock.listen(1)
      print("[PROCESSO - "+self.procID+"] ouvindo....")
      while True:
         conn, address = sock.accept()
         data = conn.recv(1024).decode()

         y = json.loads(data)

         time = max(int(self.lamp), int(y["time"]))
         time = time + 1
         self.lamp = str(time)

         if not y["ack"]:
            print("\nA mensagem chegou para mim no tempo: "+str(self.lamp+self.procID))
            list_msg_recebida.add(self.procID)
            for i in range(1, (total_process+1)):
               try:
                  sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  server_address = ('localhost', 1000+i)
                  sock_server.connect(server_address)
                  time = max(int(self.lamp), int(y["time"]))
                  self.lamp = time + 1
                  x = {
                     "ack": 1,
                     "time": self.lamp,
                     "id": self.procID,
                     "origem": y["origem"]
                  }
                  print("Enviado ACK para o Processo "+str(i)+" no tempo: "+str(self.lamp)+self.procID)
                  sock_server.send(json.dumps(x).encode())
                  list_msg_ack.add(i)
               except Exception as e:
                  print(e)
            print("\n")
                  
         elif y["ack"] == 1 and self.procID in list_msg_recebida:
            print("Recebi ACK do Processo " + y["id"] + " no tempo: " + str(self.lamp)+self.procID)
            list_acks.add(y["id"])

         if(len(list_acks) == total_process and y["origem"] == self.procID):
            print("\nEnviado para aplicação de cima ^")      
         

total_process = 3
procID = sys.argv[1]
lamp = sys.argv[1]
list_msg_ack = set([])
list_msg_recebida = set([])
list_acks = set([])

op = client(procID)
dp = server(procID)
dp.start()

input("Pressione enter pra começar!\n")
op.start()

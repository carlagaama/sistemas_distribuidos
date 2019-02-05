#!/usr/bin/python3
# Sistemas Distribuidos - Atividade 1
# Carla Simoes Gama     -     613843
# Daniel Bertoldi       -     620548

import threading
import time
import socket
import sys
import json

class client(threading.Thread):
   def __init__(self, id_processo):
      threading.Thread.__init__(self)
      self.id_processo = id_processo
      global id_mensagem
      print("Meu clock é: "+(id_mensagem)+"\n")

   def run(self):
      global id_mensagem

      id_mensagem = str(int(id_mensagem) + 1)
      print("Começou no tempo: "+id_mensagem+self.id_processo)

      for i in range(1, (total_process+1)):
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            server_address = ('localhost', 2000 + i)
            sock.connect(server_address)
            time = i + int(id_mensagem)
            print("Enviei a mensagem no tempo: "+str(time)+self.id_processo)
            x = {
               "ack": 0,
               "id_processo": self.id_processo,
               "id_mensagem": str(time)+self.id_processo,
               "origem": self.id_processo
            }
            id_mensagem = str(time)
            sock.send(json.dumps(x).encode())
            
         except socket.timeout:
            print("TIME OUT!")
         finally:
            sock.close()

class server(threading.Thread):
   def __init__(self, id_processo):
      threading.Thread.__init__(self)
      self.id_processo = id_processo
      
   def run(self):
      global id_mensagem
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', (2000+int(sys.argv[1]))))
      sock.listen(1)
      print("[PROCESSO - "+self.id_processo+"] ouvindo....")
      while True:
         conn, address = sock.accept()
         data = conn.recv(1024).decode()

         y = json.loads(data)

         time = max(int(id_mensagem), int(y["id_mensagem"]))
         time = time + 1
         id_mensagem = str(time)

         if not y["ack"]:
            print("\nA mensagem chegou para mim no tempo: "+str(id_mensagem+self.id_processo))
            lista_msg_recebida.add(id_mensagem+self.id_processo) 
            for i in range(1, (total_process+1)):
               time = max(int(id_mensagem), int(y["id_mensagem"]))
               time = time + 1
               id_mensagem = str(time)

               try:
                  sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  server_address = ('localhost', 2000+i)
                  sock_server.connect(server_address)
                  id_mensagem = str(int(id_mensagem) + 1)
                  x = {
                     "ack": 1,
                     "id_mensagem": id_mensagem,
                     "id_processo": self.id_processo,
                     "origem": y["origem"]
                  }
                  print("Enviado ACK para o Processo "+str(i)+" no tempo: "+str(id_mensagem)+self.id_processo)
                  sock_server.send(json.dumps(x).encode())
                  lista_acks_enviados.add(id_mensagem)
               except Exception as e:
                  print(e)
            print("\n")
                  
         elif y["ack"] == 1 and self.id_processo in lista_msg_recebida:
            print("Recebi ACK do Processo " + y["id_processo"] + " no tempo: " + str(id_mensagem)+self.id_processo)
            lista_acks_recebidos.add(y["id_mensagem"]) #idmsg

         if(len(lista_acks_recebidos) == total_process and y["origem"] == self.id_processo):
            print("\nEnviado para aplicação de cima ^")      
         
# Troque o número desta variável para a quantidade de terminais que você irá abrir
total_process = 3
id_processo = sys.argv[1]
id_mensagem = sys.argv[1]
lista_acks_enviados = set([])
lista_msg_recebida = set([])
lista_acks_recebidos = set([])

op = client(id_processo)
dp = server(id_processo)
dp.start()

input("Pressione enter pra começar!\n")
op.start()

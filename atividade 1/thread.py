#!/usr/bin/python3

import threading
import time
import socket

class client(threading.Thread):
   def __init__(self, processID, processName, num_processes, msg):
      threading.Thread.__init__(self)
      self.processID = processID
      self.processName = processName
      self.num_processes = num_processes
      self.msg = msg
      
   def run(self):
      for i in range(0, int(num_processes)):
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            server_address = ('localhost', 10000+i)
            sock.connect(server_address)
            sock.send((self.msg).encode())

            while True:
               print("Esperando ACKS...")
               try:
                  data, server = sock.recvfrom(64)
                  print("Ack recebido do processo: " + str(i))
                  break
               except socket.timeout:
                  print("timeout!")

         finally:
            sock.close()

class server(threading.Thread):
   def __init__(self, processID, processName):
      threading.Thread.__init__(self)
      self.processID = processID
      self.processName = processName
      self.timeStamp = time.gmtime()
      #pode trocar para milisegundos mesmo, pra notar a diferença
      print(self.processName + time.strftime(" inicializado em: %X", self.timeStamp))

   def run(self):
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(('localhost', 10000+self.processID))

      while True:
         print(self.processName + " escutando...")
         sock.listen(1)
         conn, address = sock.accept()
         data = conn.recv(64).decode()

         print(str(self.processName) + " - Recebi: " + str(data))
         conn.sendto("ACK do Processo".encode(), address)
         
      
      print("Oi, eu sou a thread servidor do processo "+self.processName)

num_processes = input("Quantos processos serão?\n")
clients = []
servers = []
flag = 0

for i in range(0, int(num_processes)):
  # thread = client(i, ("Processo %s" % i))
  # clients.append(thread)
  # thread.start()
   thread = server(i, ("Processo %s" % i))
   servers.append(thread)
   thread.start()

print("Processos inicializados!\n")

time.sleep(0.1)

for i in range(0, int(num_processes)):
   thread = client(i, ("Processo %s" % i), num_processes, "oie")
   thread.start()


   

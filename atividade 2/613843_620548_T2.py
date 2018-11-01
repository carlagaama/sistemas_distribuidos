###########################################################################
##  Carla Simões Gama           -            613843                     ###
##  Daniel Souza Bertoldi       -            620548                     ###
###########################################################################

import json
import threading
import socket
import sys
import random
import time

id_processo = 0
fila_requisicoes = list()

class EnviaRequisicao(threading.Thread):
    def __init__(self, id_processo):
        global lamp
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.querendo_usar_recurso = 1

    def run(self):
        global lamp
        for i in range(1, 4):
            #if(i != int(self.pid)):
                #envia para todos menos o próprio nó
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.2)
                    addr = ('localhost', 6660+i)
                    sock.connect(addr)

                    lamp += 1
                    mensagem = {
                        "request": 1,
                        "ok": -1,
                        "sender": self.pid,
                        "time": lamp
                    }

                    print("Enviando requisicao para o processo "+str(i))

                    sock.send(json.dumps(mensagem).encode())
                except socket.timeout:
                   print("We fucking dead, homie.")
                finally:
                    sock.close()
        print("\nEsperando OKs...")
        return

class RecebeRequisicao(threading.Thread):
    def __init__(self, id_processo):
        global lamp
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.querendo_usar_recurso = 0
        self.usando_recurso = 0
        self.ok_count = 0

    def run(self):
        global lamp, fila_requisicoes, usando_recurso, querendo_usar_recurso
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', (6660+int(self.pid))))
        sock.listen(1)

        while True:
            data, addr = sock.accept()
            mensagem = data.recv(1024).decode()

            json_data = json.loads(mensagem)

            #checa se o processo já está na fila de requisicoes
            if json_data["sender"] in fila_requisicoes:
                process_in_list = 1
            else:
                process_in_list = 0

            #se o processo estiver usando o recurso, adiciona na fila para enviar ok depois
            if(usando_recurso == True and process_in_list == False and json_data["request"] == 1):
                fila_requisicoes.append(json_data["sender"])
            elif(querendo_usar_recurso == True and process_in_list == False and json_data["request"] == 1):
                fila_requisicoes.append(json_data["sender"])

            #checa se o processo quer usar o recurso ou não
            if(json_data["request"] == 1 and json_data["sender"] == self.pid):
                print("Quero usar o recurso!")
                querendo_usar_recurso = 1

            #se a mensagem for ok e o destinatário for o processo que enviou o pedido de requisição, incrementa o self.ok_count
            if(json_data["ok"] == 1 and str(json_data["recipient"]) == self.pid):
                print("Recebi OK do processo "+str(json_data["sender"]))
                self.ok_count += 1

                print(str(self.ok_count))
                if(self.ok_count == 2):
                    #significa que recebeu ok de todo mundo, portanto pode consumir o recurso!
                    usando_recurso = 1
                    recurso = Recurso(self.pid)
                    recurso.start()
                    self.ok_count = 0

            #checa se é uma requisição e checa se está utilizando o recurso
            if(json_data["request"] == 1 and (querendo_usar_recurso == False) and (usando_recurso == False)):
                enviaOks = EnviaOks(self.pid, int(json_data["sender"]))
                enviaOks.start()
            elif(json_data["request"] == 1 and (querendo_usar_recurso == True) and (usando_recurso == False)):
                 print("Estou na fila de espera...")
                 fila_requisicoes.append(self.pid)

class Recurso(threading.Thread):
    def __init__(self, pid):
        threading.Thread.__init__(self)
        self.timer = random.randrange(3, 7)
        self.current_process = pid

    def run(self):
        global lock, fila_requisicoes, usando_recurso, querendo_usar_recurso

        lock.acquire()
        print("\n--------------------------ENTREI NA REGIÃO CRÍTICA!--------------------------")
        print("Vou segurar o recurso durante "+str(self.timer)+" segundos!")
        while(self.timer > 0):
            print("\t\t\t\t\t"+str(self.timer))
            self.timer -= 1
            time.sleep(1)
        lock.release()
        print("Recurso liberado!")
        print("-----------------------------------------------------------------------------")

        usando_recurso = 0
        querendo_usar_recurso = 0
        while(len(fila_requisicoes) > 0):
            next_process = fila_requisicoes.pop(0)
            enviaOks = EnviaOks(self.current_process, int(next_process))
            enviaOks.start()

        return

class EnviaOks(threading.Thread):
    def __init__(self, pid, sender):
        threading.Thread.__init__(self)
        self.pid = pid
        self.sender = sender

    def run(self):
        global lamp
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            if(int(self.sender) != int(self.pid)):
                addr = ('localhost', 6660+self.sender)
                sock.connect(addr)

                mensagem = {
                    "request": 0,
                    "ok": 1,
                    "sender": self.pid,
                    "recipient": self.sender,
                    "time": lamp
                }

                print("Enviado OK para o processo "+str(mensagem["recipient"]))

                sock.send(json.dumps(mensagem).encode())
        except socket.timeout:
            print("We fucking dead, homie.")
        finally:
            sock.close()

        #return kills the thread
        return

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("Falta argumentos.")
        sys.exit(0)

    lock = threading.Lock()
    id_processo = sys.argv[1]
    lamp = int(sys.argv[2])
    querendo_usar_recurso = 0
    usando_recurso = 0

    recebeRequisicao = RecebeRequisicao(id_processo)
    recebeRequisicao.start()

    while True:
        enviaRequisicao = EnviaRequisicao(id_processo)
        input()
        print("Enviando requisição...")
        enviaRequisicao.start()

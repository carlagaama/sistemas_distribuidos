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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class EnviaRequisicao(threading.Thread):
    def __init__(self, id_processo):
        global lamp
        threading.Thread.__init__(self)
        self.pid = id_processo

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

                    print(bcolors.OKBLUE+"Enviando requisicao para o processo "+str(i)+bcolors.ENDC)

                    sock.send(json.dumps(mensagem).encode())
                except socket.timeout:
                   print("We fucking dead, homie.")
                finally:
                    sock.close()
        print(bcolors.UNDERLINE+"\nEsperando OKs..."+bcolors.ENDC)
        return

class RecebeRequisicao(threading.Thread):
    def __init__(self, id_processo):
        global lamp
        threading.Thread.__init__(self)
        self.pid = id_processo
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

            #se o processo estiver usando o recurso, adiciona na fila para enviar ok depois
            if(usando_recurso == True and json_data["request"] == 1):
                fila_requisicoes.append(json_data["sender"])
                print(bcolors.HEADER+bcolors.UNDERLINE+"Processo "+str(json_data["sender"])+" esperando na fila"+bcolors.ENDC)
            elif(querendo_usar_recurso == True and json_data["request"] == 1):
                #-------bater lamp
                fila_requisicoes.append(json_data["sender"])
                print(bcolors.HEADER+bcolors.UNDERLINE+"Processo "+str(json_data["sender"])+" esperando na fila"+bcolors.ENDC)

            #checa se o processo atual quer usar o recurso ou não
            if(json_data["request"] == 1 and json_data["sender"] == self.pid):
                print(bcolors.OKGREEN+"Quero usar o recurso!"+bcolors.ENDC)
                querendo_usar_recurso = 1

            #se a mensagem for ok e o destinatário for o processo que enviou o pedido de requisição, incrementa o self.ok_count
            if(json_data["ok"] == 1 and str(json_data["recipient"]) == self.pid):
                print(bcolors.WARNING+"Recebi OK do processo "+str(json_data["sender"])+bcolors.ENDC)
                self.ok_count += 1

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

class Recurso(threading.Thread):
    def __init__(self, pid):
        threading.Thread.__init__(self)
        self.timer = random.randrange(4, 7)
        self.current_process = pid

    def run(self):
        global lock, fila_requisicoes, usando_recurso, querendo_usar_recurso

        lock.acquire()
        print(bcolors.FAIL+"\n--------------------------ENTREI NA REGIÃO CRÍTICA!--------------------------"+bcolors.ENDC)
        print(bcolors.FAIL+"Vou segurar o recurso durante "+str(self.timer)+" segundos!"+bcolors.ENDC)
        while(self.timer > 0):
            print(bcolors.FAIL+"\t\t\t\t\t"+str(self.timer)+bcolors.ENDC)
            self.timer -= 1
            time.sleep(1)
        lock.release()
        print(bcolors.FAIL+"Recurso liberado!"+bcolors.ENDC)
        print(bcolors.FAIL+"-----------------------------------------------------------------------------"+bcolors.ENDC)

        usando_recurso = 0
        querendo_usar_recurso = 0
        print("Fila:"+str(fila_requisicoes))
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

    print("Aperte ENTER para fazer uma requisição.")
    while True:
        enviaRequisicao = EnviaRequisicao(id_processo)
        input()
        print(bcolors.OKBLUE+bcolors.UNDERLINE+"Enviando requisição..."+bcolors.ENDC)
        enviaRequisicao.start()

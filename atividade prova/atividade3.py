###########################################################################
###  Carla Simões Gama           -            613843                    ###
###  Daniel Souza Bertoldi       -            620548                    ###
###########################################################################

import json
import socket
import threading
import sys

lista_vizinhos = list()
total_neighbours = 0

class bcolors:
    HEADER = '\033[95m'
    RED = '\033[31m'
    COLRED = '\033[41m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    COLGREEN = '\033[42m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ComecaEleicao(threading.Thread):
    def __init__(self, id_processo):
        threading.Thread.__init__(self)
        self.pid = id_processo

    def run(self):
        global leader

        if leader == 1:

            print("[COMEÇANDO ELEIÇÃO]")

            repassaEleicao = RepassaEleicao(self.pid, self.pid)
            repassaEleicao.start()
        else:
            print("Você não é o líder, nem rola de começar a eleição.")


class EscutaMensagens (threading.Thread):
    def __init__(self, id_processo, value):
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.value = value
        self.parent = -1
        self.messages_received = 0
        self.bo = 0
        self.le = 0
        
        # these last attributes are for leader use only, by default, it supposes that itself is the winning node
        self.returns_received = 0
        self.winning_node = self.pid
        self.winning_node_value = self.value

    def run(self):
        global total_neighbours, leader
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', (6660+int(self.pid))))
        sock.listen(2)

        print("Minha porta é: "+str(6660+int(self.pid)))

        while True:
            data, addr = sock.accept()
            mensagem = data.recv(1024).decode()

            json_mensagem = json.loads(mensagem)
            
            # leader variable
            if json_mensagem["return"] == 1:
                self.returns_received+=1

            if json_mensagem["return"] == 1 or json_mensagem["ack"] == 1:
                self.messages_received+=1

            # see what's the message is all about
            if json_mensagem["election"] == 1:
                self.le = 0
                
                # i need a father!
                if self.parent == -1 and leader == 0:
                    self.parent = json_mensagem["sender"]

                    print(bcolors.RED+"\n[ENCONTRADO PAI] processo: "+str(json_mensagem["sender"])+bcolors.ENDC)

                    # send to all neighbours
                    repassaEleicao = RepassaEleicao(self.pid, json_mensagem["sender"])
                    repassaEleicao.start()
                else:
                    # send ack to the node that contacted me
                    sendAck = SendAck(json_mensagem["sender"], self.pid)
                    sendAck.start()
            # if someone sent me their value
            elif json_mensagem["return"] == 1:
                
                print(bcolors.UNDERLINE+"[RECEBIDO VALOR] "+str(json_mensagem["value"])+" do nó "+str(json_mensagem["sender"])+bcolors.ENDC)

                # if my child value is greater than my value, then send child value
                if int(json_mensagem["value"]) > int(self.winning_node_value):
                    # if i'm not the leader, then send it to my parent
                    if leader == 0 and self.messages_received == total_neighbours-1:
                        # TODO na hora de printar vai dar bosta pq to mandando o pid do filho ao inves do no atual, consertar depois
                        sendParent = SendParent(self.parent, json_mensagem["sender"], json_mensagem["value"])
                        sendParent.start()
                        self.bo = 1
                    # otherwise, i'll just update and wait for all connections to be made
                    elif leader == 1:
                        self.winning_node = json_mensagem["sender"]
                        self.winning_node_value = json_mensagem["value"]
                # if i'm not the leader, then send my value instead
                elif leader == 0 and self.bo == 0 and self.messages_received == total_neighbours-1:
                    sendParent = SendParent(self.parent, self.pid, self.value)
                    sendParent.start()
                    self.bo = 1
            # if i received an ACK, print
            elif json_mensagem["ack"] == 1:
                print(bcolors.WARNING+"[RECEBIDO ACK] do processo "+json_mensagem["sender"]+bcolors.ENDC)
            # if it's a new leader message
            elif json_mensagem["new leader"][0] == 1:
                # reset all attributes
                self.parent = -1
                self.messages_received = 0
                self.bo = 0
                self.returns_received = 0
                self.winning_node = self.pid
                self.winning_node_value = self.value
                                
                # if i'm the new leader
                if json_mensagem["new leader"][1] == self.pid and self.le == 0:
                    leader = 1
                    sendNewLeader = SendNewLeader(self.pid, json_mensagem["new leader"][1])
                    sendNewLeader.start()
                    print(bcolors.COLGREEN+"\nParabéns, você é o novo líder. Pressione ENTER para começar a eleição."+bcolors.ENDC)
                    self.le = 1
                # else just send it
                elif self.le == 0:
                    sendNewLeader = SendNewLeader(self.pid, json_mensagem["new leader"][1])
                    sendNewLeader.start()
                    self.le = 1
                
            # if i'm the last node, then send value to parent
            if self.messages_received == total_neighbours-1 and leader == 0 and self.bo == 0:
                sendParent = SendParent(self.parent, self.pid, self.value)
                sendParent.start()
                self.bo = 1

            # if i'm the leader and just received all messages from my children, then broadcast that shit
            if self.returns_received == total_neighbours and leader == 1 and json_mensagem["ack"] != 1:
                # if i'm not the leader anymore, broadcast the new leader
                if int(self.winning_node) != int(self.pid):
                    print(bcolors.COLRED+"[ENVIADO NOVO LIDER]"+bcolors.ENDC)
                    sendNewLeader = SendNewLeader(self.pid, self.winning_node)
                    sendNewLeader.start()
                    self.bo = 0
                    leader = 0
                # TODO if i'm still the lader, what do I do?
                else:
                    print(bcolors.COLRED+"[CONTINUO LIDER]"+bcolors.ENDC)


class RepassaEleicao(threading.Thread):
    def __init__(self, id_processo, sender):
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.sender = sender

    def run(self):
        for i in lista_vizinhos:
            if i != int(self.sender):                
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.2)
                    addr = ('localhost', 6660+i)
                    sock.connect(addr)

                    mensagem = {
                        "election": 1,
                        "sender": self.pid,
                        "value": -1,
                        "return": -1,
                        "ack": 0,
                        "new leader": [-1, -1]
                    }

                    print(bcolors.HEADER+"[ENVIADO ELEIÇÃO] para o processo "+str(i)+bcolors.ENDC)
                    sock.send(json.dumps(mensagem).encode())
                except socket.timeout:
                    print("Where the fuck are you")
                finally:
                    sock.close()


class SendParent(threading.Thread):
    def __init__(self, parent, sender, value):
        threading.Thread.__init__(self)
        self.parent = parent
        self.sender = sender
        self.value = value

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            addr = ('localhost', 6660+int(self.parent))
            sock.connect(addr)

            mensagem = {
                "election": 0,
                "sender": self.sender,
                "value": self.value,
                "return": 1,
                "ack": 0,
                "new leader": [-1, -1]
            }

            print(bcolors.GREEN + "[ENVIADO VALOR] " + str(self.value) + " para o processo " + self.parent + bcolors.ENDC)
            sock.send(json.dumps(mensagem).encode())
        except socket.timeout:
            print("Who at?")
        finally:
            sock.close()


class SendAck(threading.Thread):
    def __init__(self, recipient, sender):
        threading.Thread.__init__(self)
        self.recipient = recipient
        self.sender = sender

    def run(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            addr = ('localhost', 6660+int(self.recipient))
            sock.connect(addr)

            mensagem = {
                "election": 0,
                "sender": self.sender,
                "value": -1,
                "return": -1,
                "ack": 1,
                "new leader": [-1, -1]
            }

            print(bcolors.BLUE + "[ENVIADO ACK] para o processo " + self.recipient + bcolors.ENDC)
            sock.send(json.dumps(mensagem).encode())
        except socket.timeout:
            print("Who at?")
        finally:
            sock.close()

class SendNewLeader(threading.Thread):
    def __init__(self, pid, winning_node):
        threading.Thread.__init__(self)
        self.pid = pid
        self.winning_node = winning_node

    def run(self):
        for i in lista_vizinhos:
            if i != int(self.pid):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.2)
                    addr = ('localhost', 6660+i)
                    sock.connect(addr)

                    mensagem = {
                        "election": -1,
                        "sender": -1,
                        "value": -1,
                        "return": -1,
                        "ack": -1,
                        "new leader": [1, self.winning_node]
                    }

                    sock.send(json.dumps(mensagem).encode())
                except socket.timeout:
                    print("Where the fuck are you")
                finally:
                    sock.close()


def inicializa_nos(id_processo):
    global total_neighbours

    if int(id_processo) == 1:
        lista_vizinhos.append(2)
        lista_vizinhos.append(3)
        lista_vizinhos.append(4)
        total_neighbours = 3
    elif int(id_processo) == 2:
        lista_vizinhos.append(1)
        lista_vizinhos.append(3)
        lista_vizinhos.append(5)
        total_neighbours = 3
    elif int(id_processo) == 3:
        lista_vizinhos.append(1)
        lista_vizinhos.append(2)
        lista_vizinhos.append(4)
        lista_vizinhos.append(5)
        total_neighbours = 4
    elif int(id_processo) == 4:
        lista_vizinhos.append(1)
        lista_vizinhos.append(3)
        lista_vizinhos.append(5)
        total_neighbours = 3
    elif int(id_processo) == 5:
        lista_vizinhos.append(2)
        lista_vizinhos.append(3)
        lista_vizinhos.append(4)
        lista_vizinhos.append(7)
        total_neighbours = 4
    elif int(id_processo) == 6:
        lista_vizinhos.append(8)
        lista_vizinhos.append(9)
        lista_vizinhos.append(10)
        total_neighbours = 3
    elif int(id_processo) == 7:
        lista_vizinhos.append(5)
        lista_vizinhos.append(10)
        total_neighbours = 2
    elif int(id_processo) == 8:
        lista_vizinhos.append(6)
        total_neighbours = 1
    elif int(id_processo) == 9:
        lista_vizinhos.append(6)
        lista_vizinhos.append(10)
        total_neighbours = 2
    else:
        lista_vizinhos.append(6)
        lista_vizinhos.append(7)
        lista_vizinhos.append(9)
        total_neighbours = 3


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Está faltando argumentos, carai.")
        sys.exit(0)

    id_processo = sys.argv[1]
    valor = sys.argv[2]

    # means the current node is actually the leader.
    if len(sys.argv) == 4:
        leader = 1
    else:
        leader = 0
        
    # we need to initialize who are the neighbours of each node
    inicializa_nos(id_processo)

    escutaMensagens = EscutaMensagens(id_processo, valor)
    escutaMensagens.start()

    if(leader == 1):
        print("Pressione ENTER para começar a eleição.")

    while True:
        comecaEleicao = ComecaEleicao(id_processo)
        input()
        comecaEleicao.start()

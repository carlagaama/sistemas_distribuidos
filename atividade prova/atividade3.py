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

# TODO change print colors


class ComecaEleicao(threading.Thread):
    def __init__(self, id_processo, leader):
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.leader = leader

    def run(self):
        if self.leader == 1:

            print("Sou o líder, portanto vou começar a eleição.")

            for i in lista_vizinhos:
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
                    }

                    print("Estou enviando eleicao para o meu vizinho Node "+str(i))
                    sock.send(json.dumps(mensagem).encode())
                except socket.timeout:
                    print("Where the fuck are you")
                finally:
                    sock.close()
        else:
            print("Você não é o líder, nem rola de começar a eleição.")


class EscutaMensagens (threading.Thread):
    def __init__(self, id_processo, value):
        threading.Thread.__init__(self)
        self.pid = id_processo
        self.value = value
        self.parent = -1
        self.messages_received = 0
        # these last attributes are for leader use only, by default, it supposes that itself is the winning node
        self.returns_received = 0
        self.winning_node = self.pid
        self.winning_node_value = self.value

    def run(self):
        global total_neighbours, leader
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', (6660+int(self.pid))))
        sock.listen(1)

        print("Minha porta é: "+str(6660+int(self.pid)))

        while True:
            data, addr = sock.accept()
            mensagem = data.recv(1024).decode()

            json_mensagem = json.loads(mensagem)

            # if it accepted a connection, adds if it's not a ack message
            if json_mensagem["ack"] != 1:
                self.messages_received+=1
                
            # leader variable...
            if json_mensagem["return"] == 1:
                self.returns_received+=1

            # see what's the message all about
            if json_mensagem["election"] == 1 and self.messages_received != total_neighbours:
                # i need a father!
                if self.parent == -1 and leader == 0:
                    self.parent = json_mensagem["sender"]

                    print("\nMeu pai agora é o nó: "+str(json_mensagem["sender"]+"\n"))

                    # send to all neighbours
                    repassaEleicao = RepassaEleicao(self.pid, json_mensagem["sender"])
                    repassaEleicao.start()
                else:
                    # send ack to the node that contacted me
                    sendAck = SendAck(json_mensagem["sender"], self.pid)
                    sendAck.start()
            # if someone sent me their value
            elif json_mensagem["return"] == 1:

                print("Recebi o valor: "+str(json_mensagem["value"])+" do nó "+str(json_mensagem["sender"]))
                
                # if my child value is greater than my value, then send child value
                if json_mensagem["value"] > self.value:
                    # if i'm not the leader, then send it to my parent
                    if leader == 0:
                        # TODO na hora de printar vai dar bosta pq to mandando o pid do filho ao inves do no atual, consertar depois
                        sendParent = SendParent(self.parent, json_mensagem["sender"], json_mensagem["value"])
                        sendParent.start()
                    # otherwise, i'll just update and wait for all connections to be made
                    elif leader == 1:
                        self.winning_node = json_mensagem["sender"]
                        self.winning_node_value = json_mensagem["value"]
                elif leader == 0:
                    sendParent = SendParent(self.parent, self.parent, self.value)
                    sendParent.start()
            elif json_mensagem["ack"] == 1:
                print("Eu recebi um ACK do Node "+json_mensagem["sender"])
            # if i'm the last node, then send value to parent
            elif self.messages_received == total_neighbours and leader == 0:
                sendParent = SendParent(self.parent, self.pid, self.value)
                sendParent.start()

            # if i'm the leader and just received all messages from my child, then broadcast that shit
            if self.returns_received == total_neighbours and leader == 1:
                # TODO send the new leader to the rest of the nodes.
                print("O nó líder agora é: "+str(self.winning_node)+", com valor: "+str(self.winning_node_value))


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
                    }

                    print("Estou enviando eleicao para o meu vizinho nó "+str(i))
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
                "ack": 0
            }

            print("Enviando valor "+str(self.value)+" para o Node "+self.parent)
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
                "ack": 1
            }

            print("Enviando ACK para o Node "+self.recipient)
            sock.send(json.dumps(mensagem).encode())
        except socket.timeout:
            print("Who at?")
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
    else:
        lista_vizinhos.append(2)
        lista_vizinhos.append(3)
        lista_vizinhos.append(4)
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
        comecaEleicao = ComecaEleicao(id_processo, leader)
        input()
        comecaEleicao.start()

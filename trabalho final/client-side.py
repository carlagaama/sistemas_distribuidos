from requests import post

numvms = 0
vmsids =[]
url = "http://ip_externo_da_vm:porta_de_sua_escolha"


def buyfunc():
    global numvms, vmsids

    reqvms = int(input("\nDigite o número de MVs a serem requisitadas: "))
    cpu = int(input("Digite a quantidade de CPU: "))
    ram = str(input("Digite a quantidade de RAM (em GB): "))
    dsk = str(input("Digite a quantidade de HD (em GB): "))

    returnedjson = post(url+'/buy/', json={"qtd_vms": reqvms, "specs": {"cpu": cpu, "ram": ram, "dsk": dsk}}).json()

    if returnedjson.get("success"):
        for vm in returnedjson["data"]["vmsreturned"]:
            print("\n\n*****\nDetalhes da MV "+str(numvms))
            print("Provedor: "+str(vm["provider"]))
            print("ID: "+vm["objectid"])
            print("Preço: "+str(vm["vm_specs"]["price"]))

            numvms+=1
            vmsids.append(vm["objectid"])

        if returnedjson.get("msg"):
            print(returnedjson.get("msg"))
    else:
        print("\n"+returnedjson.get("error"))


def addfunc():
    prov = int(input("\nDigite o número do provedor da MV: "))
    name = str(input("Digite o nome da MV: "))
    cpu = int(input("Digite a quantidade de CPU: "))
    ram = str(input("Digite a quantidade de RAM (em GB): "))
    dsk = str(input("Digite a quantidade de HD (em GB): "))
    val = float(input("Digite o preço da MV por hora: "))

    returnedjson = post(url+'/add/', json={"provider": prov, "vm_specs": {"vm_name": name, "qtd_cpu": cpu, "qtd_ram": ram, "qtd_dsk": dsk, "price": val, "using": 0}}).json()

    if returnedjson.get("success"):
        print("\nMV adicionada na Cloud com sucesso!")
        print("O id da MV é: "+str(returnedjson.get("vm_id")))
    else:
        print("\n"+returnedjson.get("error"))


def delfunc():
    global vmsids, numvms
    i = 0

    if numvms > 0:
        print("\nVocê tem um total de "+str(len(vmsids))+" MVs. Quantas você quer liberar?")

        while i < len(vmsids):
            print(str(i)+" - "+vmsids[i])
            i+=1

        num = input()
        num = eval("["+num+"]")

        for j in num:
            id = vmsids[j]
            returnedjson = post(url+'/release/', json={"objid": id}).json()
            numvms-=1
            vmsids.remove(id)

            if returnedjson.get("success"):
                print("\nMV "+id+" liberada com sucesso!")
            else:
                print(returnedjson.get("error"))
    else:
        print("\nVocê não está usando nenhuma MV!")


if __name__ == '__main__' :
    while(True):
        print("\n****\nEscolha uma opção:\n1 - Comprar VMs\n2 - Adicionar VM\n3 - Liberar VMs")
        op = int(input())

        if op == 1:
            buyfunc()
        elif op == 2:
            addfunc()
        elif op == 3:
            delfunc()
        else:
            print("\n Escolha uma opção entre 1 e 3! >:( ")

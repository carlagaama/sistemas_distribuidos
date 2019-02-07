# Cloud Broker

Leia o PDF da [descrição do projeto](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/descricao.pdf) para maiores informações.

## Começando
### Pré-requisitos

Da forma como arquitetamos e desenvolvemos este projeto, você **deverá** ter uma máquina virtual ativa em algum provedor de computação em nuvem, como o [GCP](https://cloud.google.com/) ou a [AWS](https://aws.amazon.com/), ou qualquer outra de sua escolha. Nós optamos por usar o GCP, por sua simplicidade.

Sua VM deverá ter um banco de dados ```NoSQL``` localmente, que irá armazenar as informações de todas as VMs, e uma API que deverá receber requisições e retornar resultados para o cliente. Para o banco, escolhemos utilizar o [MongoDB](https://www.mongodb.com/), simples e fácil de aprender, e para a API utilizamos [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/), que abstrai e simplifica toda a lógica por debaixo de ouvir e responder por chamadas ```HTTP```.

**OPCIONAL:** para testar a API, utilizamos o [Postman](https://www.getpostman.com/), que facilita a leitura dos *JSONs* que serão enviados e recebidos, tornando-os mais legíveis.

## Configurando sua VM pelo GCP
### Criando sua instância de VM

  1. Após logar no GCP e criar um projeto, abra o menu de navegação e navegue até *Compute Engine* > *Instâncias de VMs* e ative o faturamento, caso necessite.
  2. Clique em ```Criar```, dê um nome a sua VM e escolha a região ```southamerica-east1```, com a zona de sua preferência.
  3. Como se trata de um trabalho simples, escolha as opções mais básicas, então selecione ```Personalizar``` e selecione apenas 1 núcleo de CPU compartilhado, com ```0,6 GB``` de memória.
  4. Na opção de ```Disco de Inicialização```, nós optamos por rodar ```Ubuntu 18.04 LTS```, com ```15 GB``` de espaço de disco.
  5. Em ```Conta de Serviço```, selecione *Nenhuma conta de serviço*.
  6. **IMPORTANTE:** verifique que você permitiu o tráfego ```HTTP/HTTPS``` na seção ```Firewall```, caso contrário a API não irá funcionar!

Se você não errou em nenhum passo até agora, você deve estar vendo algo parecido com isso na sua tela:

![print1](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print1.png)

Pronto! Você acabou de criar uma VM no Google Cloud! Vá tomar um café, você merece. :)

### Inicialização inicial da VM

  1. Clique na seta ao lado do *SSH*, na categoria ```Conectar```, e selecione *Visualizar comando gcloud*.
  2. Na tela que abrirá, clique no botão *Executar no Cloud Shell*. Começará o processo de inialização da sua VM. Você verá uma tela desta forma:

![Google Cloud Shell](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print2.png)

  3. Pressione ```ENTER```. Após os metadados SSH do projeto terem sido atualizados, use o comando ```gcloud init```.
  4. Após aceitar o pedido de login, clique no link que será gerado, selecione sua conta do GCP, copie o código e cole no Google Cloud Shell.
  5. Digite o número correspondente ao seu projeto.
  6. Não é necessário configurar uma ```Zona``` e ```Região``` padrão, mas caso queira, saiba mais sobre as diferenças de cada [clicando neste link](https://cloud.google.com/compute/docs/regions-zones/).
  7. Se tudo deu certo, suba um pouco a tela do Google Cloud Shell e você verá as seguintes mensagens:
  
![config success](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print3.png)

Agora sim sua VM poderá fazer downloads dos arquivos que você irá armazenar em um ```bucket``` (calma, explicaremos esta parte mais para a frente!). Agora você pode conectar na sua VM usando a opção *SSH* diretamente, e **lembre de rodar os comandos ```sudo apt-get update``` e ```sudo apt-get upgrade``` assim que a conexão for estabelecida!**

### Criando, adicionando e baixando arquivos de um Bucket na VM
#### Criando o bucket

No *Console* do GCP, abra o *Menu de Navegação* e selecione *Storage*. Você terá que criar um ```bucket``` (intervalo, na versão PT-BR) para poder transferir arquivos da sua máquina local para a VM.

  1. Clique em ```Criar intervalo```, e dê um nome para o seu ```bucket```.
  2. Selecione a ```Classe de armazenamento padrão```, recomendo selecionar a classe ```Regional```. Para saber mais sobre as diferentes classes, acesse [este guia](https://cloud.google.com/storage/docs/storage-classes).
  3. Na seção ```Local```, se você está usando a classe Regional, selecione ```southamerica-east1```.
  4. Ignore as configurações avançadas e crie o ```bucket```.

#### Adicionando arquivos no bucket

  1. Selecione a opção ```Enviar arquivos``` e selecione o arquivo ```api.py``` para ser enviado.
  2. Pronto, seu arquivo foi adicionado no ```bucket```. É literalmente só isso mesmo.
  
 ![arquivo adicionado](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print4.png)

#### Baixando arquivos do bucket na VM

  1. Abra a conexão com sua VM via *SSH* caso ainda não o tenha feito.
  2. Rode o comando: ```gsutil cp gs://<nome_do_seu_bucket>/<nome_do_arquivo> .```.
  3. Tcharam! Sua VM acabou de baixar o arquivo do bucket!
  
  ![arquivo baixado](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print5.png)
  
### Criando um IP externo para sua VM

Como você já deve ter percebido durante sua estadia no menu de *Instâncias de VMs*, sua VM tem um IP interno, que é usado para se comunicar com outras VMs que você tenha criado, porém este IP não tem acesso a internet. Para isso, precisamos reservar um IP externo estático que iremos usar para fazer a conexão do cliente com a ```API``` que está na VM.

  1. A partir do *Menu de Navegação*, clique em *Rede VPC* > *Endereços IP externos*.
  2. Dê um nome para seu endereço, uma breve descrição do para que ele será usado.
  3. Selecione ```southamerica-east1``` na seção ```Region```, não importa que seremos forçados a usar nível Premium de serviço de rede.
  4. Deixe o ```Tipo``` como ```Regional```.
  5. **Importante:** na seção ```Anexado a```, selecione o nome do seu projeto.
  6. Clique em ```Reservar```.
  
 ![ip externo criado](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print6.png)
 
### Adicionando regra de firewall

Caso você já tenha dado uma olhada no código ```cliente.py``` ou seja familiarizado com APIs ```REST```, você já deve saber que é necessário especificarmos uma porta para podermos fazer as requisições ```HTTP```. Como já foi feito anteriormente, a VM aceita conexões ```HTTP/HTTPS```, porém a porta que estamos usando para fazer as chamadas serão bloqueadas pelo ```Firewall``` da VM. Para fazer a VM aceitar conexões na porta da API:

  1. Na própria página da ```Rede VPC```, selecione ```Regras de Firewall```.
  2. Embaixo da barra de busca, selecione ```Criar regra de Firewall```.
  3. Dê um nome para a sua regra, uma breve descrição e deixe os ```Registros``` desativados.
  4. Não mude nada e desça até a seção ```Tags de destino```, e dê uma tag para sua regra.
  5. Em ```Intervalos de IPs de origem```, deixe 0.0.0.0/0. Dessa forma o firewall irá deixar qualquer outro computador se conectar com sua VM.

(**Observação:** isso é **extremamente** perigoso em cenários reais, você deveria criar intervalos que aceitem computadores com IPs confiáveis, mas já que esse trabalho se trata de um projeto de universidade, então podemos "ignorar" esse quesito de segurança de redes.)

  6. Em ```Portas e protocolos``` > ```Protocolos e portas especificados```, selecione ```tcp```e digite o valor da porta da API. Lembrando que este valor **tem** que ser maior que 1024.
  7. Clique em ```Criar```.
  
 ![regra firewall criada](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/media/print7.png)
 
  8. Volte na página *Instâncias de VMs*, clique no nome da sua VM, depois na opção *Editar*.
  9. Encontre o campo ```Tags de rede``` e digite o nome da tag da regra de firewall que você criou no passo 4.
  10. Desça até o final da página e clique em ```Salvar```.
  
Finalmente, sua VM agora está completamente configurada para ser utilizada com o ```api.py```. Mas, espera! Falta instalarmos e configurarmos o ```MongoDB``` na VM!

## Instalando e configurando o MongoDB na sua VM

Esta é a última parte antes de podermos finalmente testar a VM funcionando com a API e o banco de dados. Porém, como você deve ter notado, só conseguimos acessar nossa VM via *SSH*, portanto teremos que baixar, configurar e criar *bancos* e *coleções* tudo via terminal. Caso queira seguir viagem sem esse tutorial, você pode ler o guia direto [aqui](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)

Respira, vai dar tudo certo, ok? Conecte com sua máquina via *SSH*, faz uma prece e siga o resto dos passos.

  1. Rode o comando ```sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4```.
  2. Crie um arquivo de lista pro ```MongoDB```. Essa parte vai depender do SO que você usou para inicializar sua VM, acesse [este link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#create-a-list-file-for-mongodb) para rodar o comando correspondente ao seu SO.
  3. Dê um ```sudo apt-get update```.
  4. Para instalar a última versão do ```MongoDB```, use ```sudo apt-get install -y mongodb-org```. Caso queira uma versão específica, veja [este link](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-the-mongodb-packages).

Espere a instalação acabar e **bang!**, sua VM agora tem ```MongoDB```! Agora temos que iniciá-lo, criar um *banco de dados* e uma *coleção*. Bora lá:

  1. Rode o comando ```sudo service mongod start```.
  2. Caso queira ter certeza de que tudo está funcional, dê um ```sudo less /var/log/mongodb/mongod.log``` e procure uma linha escrita *```[initandlisten] waiting for connections on port 27017```*. 27017 é a porta padrão que o ```MongoDB```usa. Se tudo estiver correto, prossiga.
  3. O Mongo só cria um *bd* e uma *coleção* quando há pelo menos um documento neles. Há duas formas de prosseguir daqui:
  
      3.1. Caso você tenha um arquivo *.json* do Mongo pronto para ser importado, basta usar o comando ```mongo import --db <nome_db> --collection <nome_colecao> --file <nome_do_arquivo_.json>```.
      
      3.2. Caso contrário, você deverá rodar os comandos (dentro do ```mongo```): ```use <nome_bd>```, depois ```db.<nome_colecao>.insertOne({<campos e valores do seu bd>})```.
    
Lembrando que fica mais fácil se você montar o seu banco de dados localmente, depois enviar para o ```bucket```, baixar pela VM e finalizar usando o ```mongoimport```.

FINALMENTE, tudo está pronto para funcionar! Não foi tão difícil, não é? :)

## Rodando o programa
### Usando o Postman

Caso opte por usar o ```Postman``` (altamente recomendado) para testar apenas as chamadas e troca de mensagens, então há 3 rotas que deverão ser testadas:

* **Rota /buy/**

  O endereço no qual será enviado o *JSON* é: ```http://<ip_externo_da_vm>:<porta_da_api>/buy/```

  O *JSON* que será lido nesta rota deverá ter a seguinte estrutura:
  
  ```
    {
      "qtd_vms": 2,
      "specs": {
    	  "cpu": 3,
    	  "ram": "8GB",
    	  "dsk": "500GB"
      }
    }
  ```
  
  Note que os campos ```"qtd_vms"``` e ```"cpu"``` carregam um inteiro, enquanto os campos ```"ram``` e ```"dsk"``` contém uma string, com *GB* escrito no final. Sem o *GB* a API irá acusar que não existe VMs no *banco de dados* com as especificações.
  
  Caso a requisição tenha sucesso, o *JSON* que será retornado terá a seguinte estrutura:

  ```javascript
    {
      "data": {
          "vmsreturned": [
              {
                  "objectid": "5c4d8392abb6940577873cc6",
                  "provider": 4,
                  "vm_specs": {
                      "price": 0.043,
                      "qtd_cpu": 3,
                      "qtd_dsk": "500GB",
                      "qtd_ram": "8GB",
                      "using": 1,
                      "vm_name": "vm_4_001"
                  }
              },
              {
                  "objectid": "5c4f08fb0f37159765456bc0",
                  "provider": 8,
                  "vm_specs": {
                      "price": 0.184,
                      "qtd_cpu": 3,
                      "qtd_dsk": "500GB",
                      "qtd_ram": "8GB",
                      "using": 1,
                      "vm_name": "vm_8_002"
                  }
              }
          ]
      },
      "success": true
    }
  ```
  Caso o cliente peça mais VMs do que existem no*banco de dados*, o *JSON* retornado é:
  
  ```javascript
    {
      "data": {
          "vmsreturned": [
              {
                  "objectid": "5c4d82feabb6940577873cc2",
                  "provider": 1,
                  "vm_specs": {
                      "price": 0.523,
                      "qtd_cpu": 3,
                      "qtd_dsk": "500GB",
                      "qtd_ram": "8GB",
                      "using": 1,
                      "vm_name": "vm_1_001"
                  }
              }
          ]
      },
      "msg": "Existem apenas 1 MVs com a especificação requisitada",
      "success": true
    }
  ```
  
  Em caso de falha, o *JSON* retornado será:

  ```javascript
    {
      "error": "Não existem MVs com estas especificações",
      "success": false
    }
  ```
  
  Com esta informação você pode alterar a forma como o *JSON* é lido do lado do cliente da forma que bem entender. Assim que o cliente faz a requisição e é encontrado uma VM, o *banco de dados* atualiza o campo ```using``` para 1, buscas posteriores com as mesmas requisições não serão retornadas tais VMs.
  
  * **Rota /add/**
  
    O endereço no qual será enviado o *JSON* é: ```http://<ip_externo_da_vm>:<porta_da_api>/add/```
  
  Esta rota é utilizada para adicionar uma VM no *banco de dados*, portanto o *JSON* deve conter todas as informações da VM. Exemplo:
  
  ```javascript
    {
      "provider": 5,
      "vm_specs": {
          "vm_name": "vm_5_001",
          "qtd_cpu": 3,
          "qtd_ram": "8GB",
          "qtd_dsk": "300GB",
          "price": 0.054,
          "using": 0
      }
    }
  ```
  
  O *JSON* de sucesso retorna o ```id``` da VM que foi inserida no *banco de dados*:
  
  ```javascript
    {
        "success": true,
        "vm_id": "5c5b4715b443262bdc70fe9c"
    }
  ```
  
  * **Rota /release/**

  O endereço no qual será enviado o *JSON* é: ```http://<ip_externo_da_vm>:<porta_da_api>/release/```
  
  Como o próprio nome diz, é por meio desta rota que o cliente libera a VM. O *JSON* é simples, apenas o ```id``` da VM que está sendo liberada é enviada para a API, que atualiza o campo ```using``` da VM para 0, podendo ser retornada em outras buscas.
  
  ```javascript
    {
        "objid": "5c4d82feabb6940577873cc2"
    }
  ```
  
  O retorno é tão simples quanto a mensagem enviada:
  
  ```javascript
    {
      "success": true
    }
  ```
  
### Usando o código client-side.py

Apenas digite o número da operação que você quer realizar e digite o que o programa lhe pedir. **Lembrando** que quando o programa te pedir a quantidade de RAM e disco, certifique-se de acrescentar ```GB``` no final, colado ao número.

O próprio código torna o *JSON* retornado legível para o cliente final.

### O que melhorar no código

O ideal seria ter o cliente separado do provedor, como um verdadeiro ```Cloud Broker```. Da forma que desenvolvemos, o cliente e o provedor são um só, sendo possível buscar, adicionar e liberar VMs. Se quiser implementar corretamente, basta criar um código provedor que irá fazer a ponte entre o uso/liberação das VMs do cliente com o *banco de dados* do ```Cloud Broker```.

Outro ponto: não trata concorrência. Caso dois clientes solicitem a mesma VM, tecnicamente ambos estarão usando a mesma VM caso o *banco de dados* não atualize a tempo do segundo cliente buscar a VM. Para corrigir isso, basta criar um ```timer``` que vai esperar alguns breves segundos antes de liberar o uso para o primeiro cliente.

Por fim, caso caia a conexão do cliente com o ```Cloud Broker```, a VM ficaria sendo usada para todo sempre. Um método que fique pingando o cliente a cada X segundos é o suficiente para solucionar esse problema.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/carlagaama/sistemas_distribuidos/blob/master/LICENSE) file for details

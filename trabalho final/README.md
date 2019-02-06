# Cloud Broker

Leia o PDF da [descrição do projeto](https://github.com/carlagaama/sistemas_distribuidos/blob/master/trabalho%20final/descricao.pdf) para maiores informações.

## Começando
### Pré-requisitos

Da forma como arquitetamos e desenvolvemos este projeto, você **deverá** ter uma máquina virtual ativa em algum provedor de computação em nuvem, como o [GCP](https://cloud.google.com/) ou a [AWS](https://aws.amazon.com/), ou qualquer outra de sua escolha. Nós optamos por usar o GCP, por sua simplicidade.

Sua VM deverá ter um banco de dados ```NoSQL``` localmente, que irá armazenar as informações de todas as VMs, e uma API que deverá receber requisições e retornar resultados para o cliente. Para o banco, escolhemos utilizar o [MongoDB](https://www.mongodb.com/), simples e fácil de aprender, e para a API utilizamos [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/), que abstrai e simplifica toda a lógica por debaixo de ouvir e responder por chamadas ```HTTP```.

## Configurando sua VM pelo GCP
### Criando sua instância de VM

  1. Após logar no GCP e criar um projeto, abra o menu de navegação e navegue até *Compute Engine* > *Instâncias de VMs* e ative o faturamento, caso necessite.
  2. Clique em ```Criar```, dê um nome a sua VM e escolha a região ```southamerica-east1```, com a zona de sua preferência.
  3. Como se trata de um trabalho simples, escolha as opções mais básicas, então selecione ```Personalizar``` e selecione apenas 1 núcleo de CPU compartilhado, com ```0,6 GB``` de memória.
  4. Na opção de ```Disco de Inicialização```, nós optamos por rodar ```Ubuntu 18.04 LTS```, com ```15 GB``` de espaço de disco.
  5. Em ```Conta de Serviço```, selecione *Nenhuma conta de serviço*.
  6. **IMPORTANTE:** verifique que você permitiu o tráfego ```HTTP/HTTPS``` na seção ```Firewall```, caso contrário a API não irá funcionar!

Se você não errou em nenhum passo até agora, você deve estar vendo algo parecido com isso na sua tela:

<print1_2>

Pronto! Você acabou de criar uma VM no Google Cloud! Vá tomar um café, você merece. :)

### Inicialização inicial da VM

  1. No canto superior direito, clique na seta ao lado do *SSH*, na categoria ```Conectar```, e selecione *Visualizar comando gcloud*.
  2. Na tela que abrirá, clique no botão *Executar no Cloud Shell*. Começará o processo de inialização da sua VM. Você verá uma tela desta forma:

<print_gcloud_shell>

  3. Pressione ```ENTER```. Após os metadados SSH do projeto terem sido atualizados, use o comando ```gcloud init```.
  4. Após aceitar o pedido de login, clique no link que será gerado, selecione sua conta do GCP, copie o código e cole no Google Cloud Shell.
  5. Digite o número correspondente ao seu projeto.
  6. Não é necessário configurar uma ```Zona``` e ```Região``` padrão, mas caso queira, saiba mais sobre as diferenças de cada [clicando neste link](https://cloud.google.com/compute/docs/regions-zones/).
  7. Se tudo deu certo, suba um pouco a tela do Google Cloud Shell e você verá as seguintes mensagens:
  
<print3_sucess>

Agora sim sua VM poderá fazer downloads dos arquivos que você irá armazenar em um ```bucket``` (calma, explicaremos esta parte mais para a frente!). Agora você pode conectar na sua VM usando a opção *SSH* diretamente, e **lembre de rodar os comandos ```sudo apt-get update``` e ```sudo apt-get upgrade``` assim que a conexão for estabelecida!**

## Rodando o programa

Você deverá abrir 10 processos rodando o programa ```atividade3.py```, seja via terminal ou pela IDE que estiver utilizando, seguido de um número, que será o ```id``` do processo, e outro número que será o ```valor``` do mesmo. Caso você queira iniciar um processo como líder, basta acrescentar um quarto argumento, com valor 1. Somente o líder pode começar uma eleição, então faça questão de ter um líder ativo na sua topologia.

Inicializar o processo da forma:

```
python3 atividade3.py 1 1
```

Irá criar o processo 1, com valor 1.

Já inicializar um processo da forma:

```
python3 atividade3.py 4 20 1
```

Irá criar o processo 4, com valor 20 e que é o líder.

Assim que cada processo estiver com a mensagem:

```
Minha porta é: X
```

E o líder estiver sido inicializado, com a seguinte mensagem sendo mostrada na tela:

```
Pressione ENTER para começar a eleição.
```

Você está pronto para começar. Basta pressionar ```Enter``` no processo líder e ver como o novo líder é encontrado, com base na sua topologia.

**OBSERVAÇÕES:**
* A topologia que adotamos é a seguinte:

![topologia](https://github.com/carlagaama/sistemas_distribuidos/blob/master/atividade%20prova/topologia.PNG)

Se você quiser mudar esta topologia, terá que alterar os valores do método ```inicializa_nos``` para que fique igual a sua topologia.

### O que melhorar no código

Este programa não trata concorrência de eleição, já que deve haver um líder preestabelecido para que o mesmo funcione. Para testar concorrência, você deverá implementar um arquivo que irá intermediar as chamadas de eleições, e retornar o ```id``` do líder encontrado, assim como o momento em que a eleição de menor valor deixou de existir.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/carlagaama/sistemas_distribuidos/blob/master/LICENSE) file for details

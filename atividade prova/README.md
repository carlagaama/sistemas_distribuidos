# Eleição de Líder em Ambientes Sem-Fio

Leia o PDF da [descrição do projeto](https://github.com/carlagaama/sistemas_distribuidos/blob/master/atividade%20prova/descricao.pdf) para maiores informações.

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

# Multicast ordenado

Leia o PDF da [descrição do projeto](https://github.com/carlagaama/sistemas_distribuidos/blob/master/atividade%201/descricao.pdf) para maiores informações.

## Rodando o programa

Você deverá abrir 3 processos (caso você troque o valor da variável ```total_process```, abra a mesma quantidade de terminais que você especificou) rodando o programa ```613843_620548.py```, seja via terminal ou pela IDE que estiver utilizando, seguido do ```id``` do processo, que também será utilizado como marca de tempo do mesmo.

Inicializar o processo da forma:

```
python3 613843_620548.py 1
```

Irá criar o processo 1, com marca de tempo 1.

Assim que cada processo estiver com a mensagem:

```
[PROCESSO - X] ouvindo...
```

Você está pronto para começar. Basta pressionar ```Enter``` no processo escolhido e ver como o multicast ocorre.

**OBSERVAÇÃO:** o processo que iniciou o multicast não poderá mandar mais mensagens até ser reiniciado.

### O que melhorar no código

Como a marca de tempo está no ```id```, nós utilizamos o próprio ```id``` para decrementar a marca de tempo (que também recebe o valor do ```id```). Funciona, porém não está nos padrões de um multicast de verdade. O correto seria utilizar a fila de mensagens recebidas para ter maior controle sobre o tempo lógico de cada processo.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/carlagaama/sistemas_distribuidos/blob/master/LICENSE) file for details

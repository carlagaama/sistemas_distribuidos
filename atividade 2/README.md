# Exclusão Mútua

Leia o PDF da [descrição do projeto](https://github.com/carlagaama/sistemas_distribuidos/blob/master/atividade%202/descricao.pdf) para maiores informações.

## Rodando o programa

Você deverá abrir 3 processos rodando o programa ```613843_620548_T2.py```, seja via terminal ou pela IDE que estiver utilizando, seguido de um número, que será o ```id``` do processo, e outro número que será a marca de tempo lógico do processo, o ```lamp```.

Inicializar o processo da forma:

```
python3 613843_620548_T2.py 1 1
```

Irá criar o processo 1, com marca de tempo 1.

Assim que cada processo estiver com a mensagem:

```
Aperte ENTER para fazer uma requisição.
```

Você está pronto para começar. Basta pressionar ```Enter``` no processo escolhido e ver como o recurso é consumido.

**OBSERVAÇÃO:** a classe ```Recurso``` gera um valor aleatório entre 4 e 6, que será o tempo em segundos que o processo que está consumindo o recurso ficará "trancado" até deixar de consumir o recurso. É tempo o suficiente para você pressionar ```ENTER``` nos outros processos para que eles entrem na fila e consumam o recurso posteriormente.

### O que melhorar no código

Nunca é usado o relógio lógico dos processos para decidir quem vai entrar na fila de espera, e quem vai "ignorar" a requisição. Um bônus também seria criar um novo recurso que pode ser consumido paralelo a outro recurso.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/carlagaama/sistemas_distribuidos/blob/master/LICENSE) file for details

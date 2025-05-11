# **Projeto Banco Dio**

Repositório criado para compartilhar a resolução do desafio "Criando um sistema bancário com Python" feito pela [Dio](https://web.dio.me/home). 

O objetivo desse projeto é simular um sistema de banco básico onde é possível fazer depósito, saque e visualizar o extrato bancário.

## 💻 Funcionalidades
**Depósito**: permite depósito de valores positivos maiores que zero.

**Saque**: permite saque de valores positivos maiores que zero e menores que o valor total da conta do usuário. Limite máximo de R$500 por saque e apenas 3 saques diários.

**Extrato bancário**: exibe o histórico de saques, depósitos e o valor total disponível na conta do usuário.

**Menu**:
O menu é composto por 4 opções:
[S] para saque, [D] para depósito, [E] para extrato, [C] para cadastro de cliente, [Y] para cadastro de conta e [Q] para fechar o programa. Se digitado um valor diferente é exibido uma mensagem de erro. O valor digitado pode ser tanto maiúsculo quanto minúsculo.

**Cadastro de Cliente**: Faz o cadastro de um novo cliente verificando se o cpf já existe na lista, caso exista exibe uma mensagem de alerta. Só é possivel cadastrar uma conta se existir um cliente cadastrado.

**Cadastro de Conta**: Verifica se existe cliente cadastrado através do cpf, se existir cria uma nova conta em uma lista de contas. Clientes podem ter várias contas mas uma conta só pode ter vínculo com apenas um cliente.


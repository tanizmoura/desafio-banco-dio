from datetime import datetime
from abc import ABC, abstractmethod
import textwrap

class Historico:
    def __init__(self):
        self._transacoes = []
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        )


class Conta:
    def __init__(self, numero, cliente):
        self._saldo =  0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    @property
    def saldo(self):
        return self._saldo    
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    @property
    def agencia(self):
        return self._agencia
    @property
    def numero(self):
        return self._numero
    
    def sacar(self, valor):
        saldo = self.saldo
        if valor < saldo and valor > 0:
            print("Saque realizado com sucesso!")
            self._saldo -= valor
            return True
        elif valor > saldo:
            print("Saldo insuficiente...")
        else:
            print("Digite um valor válido...")
        return False
            
    def depositar(self, valor):
        if valor > 0:
            print("Depósito realizado com sucesso!")
            self._saldo += valor
        else:
            print("Digite um valor válido...")
            return False
        return True
    
    def mostra_conta(self):
        return self._numero    
    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join(f'{chave} = {valor}' for chave, valor in self.__dict__.items())}"

class ContaCorrente(Conta):
    def __init__(self,numero, cliente, limite = 500, limite_saques = 3):        
        self.limite = limite
        self.limite_saques = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques > self.limite_saques
        if excedeu_limite:
            print("O valor de saque excede o limite!")
        elif excedeu_saque:
            print("Número máximo de saques excedido!")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            """

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(self, conta = Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta=Conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta = Conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

#Recupera a conta do cliente
def recupera_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    return cliente.contas[0]

#Exibe o extrato
def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    conta = recupera_conta_cliente(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "Não foram realizado movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\n R${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\nR${conta.saldo:.2f}")
    print("-"*40)

#Lógica de depósito
def depositar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recupera_conta_cliente(cliente)

    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

#Lógica de saque
def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recupera_conta_cliente(cliente)

    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)    

#Cadastro de clientes
def cadastro_cliente(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("CPF já cadastrado!")
        return
    
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (00/00/000): ")   
    print("Endereço:")
    endereco = {
        "logradouro": input("Logradouro: "),
        "número:": input("Número: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "estado": input("Estado: ")
    }

    cliente = PessoaFisica(nome = nome, data_nascimento= data_nascimento, cpf= cpf, endereco = endereco)

    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")
    
#Verifica se o valor digitado é um numero válido
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

#Cadastro de conta
def cadastro_conta(numero_conta, clientes, contas):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado!")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero= numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")

def lista_contas(contas):
    for conta in contas:
        print("-"*40)
        print(textwrap.dedent(str(conta)))

#Filtra Clientes
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

#Imprime o menu interativo
def menu():
    menu = """
    ========= BANCO DIO =========
    [S]\tSaque
    [D]\tDepósito
    [E]\tExtrato
    [C]\tCadastro de Cliente
    [Y]\tCadastro de Conta
    [Q]\tSair
    =============================
    Opção: 
    """
    return input(textwrap.dedent(menu))

def main():      
    
    clientes = []  
    contas = []

    while True:

        opcao = menu()
        #SAQUE
        if opcao == "s" or opcao == "S":
            print(" SAQUE ".center(40,"="))
            sacar(clientes)
                    
        #DEPÓSITO
        elif opcao == "d" or opcao == "D":
            print(" DEPÓSITO ".center(40,"="))
            depositar(clientes)
                
        #EXTRATO        
        elif opcao == "e" or opcao == "E":
            print(" EXTRATO ".center(40,"="))
            exibir_extrato(clientes)

        #CADASTRO CLIENTE
        elif opcao == "c" or opcao == "C":
            print(" CADASTRO DE CLIENTE ".center(40,"="))
            cadastro_cliente(clientes)

        #CADASTRO CONTA
        elif opcao == "y" or opcao == "Y":
            print(" CADASTRO DE CONTA ".center(40,"="))
            numero_conta = len(contas) + 1
            cadastro_conta(numero_conta, clientes, contas)

        #ENCERRAR 
        elif opcao == "q" or opcao == "Q":
                print("Volte sempre!")
                break

        else:
            print("Opção inválida!")

main()   

 


from datetime import datetime
import textwrap

#Soma o valor do depósito com a conta
def depositar(saldo, valor, data, id, contas=[]):
    saldo += valor
    contas[id]["extrato"].append(adiciona_extrato("depósito", valor, saldo, data))
    
    return saldo

#Lógica de depósito
def deposito(data_atual, id, contas=[]):
    while True:
                            
        valor_deposito = input("Informe o valor que deseja depositar: R$")

        if is_float(valor_deposito):
            valor_deposito = float(valor_deposito)
            if valor_deposito <= 0:
                print("Valor não pode ser menor ou igual a 0!")
            else:
                contas[id]["saldo"] = depositar(contas[id]["saldo"], valor_deposito, data_atual, id, contas)
                print("Depósito realizado com sucesso!")
                break
        else:
            print("Digite um valor válido!")   

#Desconta o valor de saque da conta
def sacar(*,saldo, valor, data, id, contas=[]):
    saldo -= valor
    contas[id]["extrato"].append(adiciona_extrato("saque", valor, saldo, data))
    return saldo

#Lógica de saque
def saque(data_atual, id, contas=[]):
    qtd_saque = saque_diario(data_atual, id, contas)
    LIMITE_SAQUE = 10

    while True:

        valor_saque = int(input("Informe o valor que deseja sacar: R$"))

        if is_float(valor_saque):
            valor_saque = float(valor_saque)
            if valor_saque <= 0:
                print("Valor não pode ser menor ou igual a 0!")
            elif qtd_saque < 10 and contas[id]["saldo"] > valor_saque and valor_saque <= 500:
                contas[id]["saldo"] = sacar(saldo=contas[id]["saldo"], valor=valor_saque, data= data_atual, id=id, contas= contas)
                print("Saque realizado com sucesso!")       
                break
            elif qtd_saque == LIMITE_SAQUE:
                print("Quantidade de saques excedidas! Tente novamente amanhã.")
                break
            elif valor_saque > 500:
                print("Limite de saque excedido! (Limite: R$500)")
            else:
                print("Saldo insuficiente...")
                break
        else:
            print("Digite um valor válido!")

#Cria um novo valor no extrato
def adiciona_extrato(operacao, valor, saldo, data):
    data = datetime.strptime(data, '%d/%m/%Y %H:%M')
    extrato = {"op": operacao, "valor": valor, "saldo": saldo, "data": data }

    return extrato

def extrato(id, contas=[]):
    for i in contas[id]["extrato"]:
        print(f"{i['op']} no valor de R${i['valor']} - Saldo: R${i['saldo']}")
        print(f"{i['data'].strftime("%d/%m/%Y %H:%M")}\n")

#Verifica quantos saques foram feitos no dia
def saque_diario(data, id, contas=[]):
    qtd_saque = 0
    data_atual = datetime.strptime(data, "%d/%m/%Y %H:%M")
    data_atual = data_atual.strftime("%d/%m/%Y")

    if contas[id]["extrato"]:
        for i in contas[id]["extrato"]:
            if i['op'] == 'saque':
                if i['data'].strftime("%d/%m/%Y") == data_atual:
                    qtd_saque += 1   
    return qtd_saque

#Adiciona usuario a lista de usuários
def adiciona_usuario(**usuario):    
    return usuario

#Cadastro de clientes
def cadastro_cliente(usuarios = []):
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento (00/00/000): ")   

    while True:
        cpf = input("CPF: ")

        if is_float(cpf):
            if usuarios and valida_cpf(cpf, usuarios):
                print("CPF já está cadastrado!")
            else:
                break
        else:
            print("Digite um cpf válido!")

    print("Endereço:")
    endereco = {
        "logradouro": input("Logradouro: "),
        "número:": input("Número: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "estado": input("Estado: ")
    }

    usuarios.append(adiciona_usuario(nome = nome, data_nascimento = data_nascimento, cpf = cpf, endereco = endereco))
    print("Cliente cadastrado com sucesso!")
    
#Verifica se o valor digitado é um numero válido
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
#Verifica se já existe usuário com o cpf cadastrado
def valida_cpf(cpf, usuarios=[]):
    existe = 0
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            existe += 1
            
    if existe == 1:
        return True
    else:
        return False
    
#Cadastro de Conta Corrente
def cria_conta(cpf, contas =[]):
    agencia = "0001"
    usuario = cpf
    saldo = 0
    extrato = []

    if not contas:
        numero_conta = 1
    else:
        numero_conta = len(contas) + 1

    conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": saldo, "extrato": extrato}

    return conta

#Cadastro de conta
def cadastro_conta(usuarios=[], contas=[]):
    usuario = input("Digite seu cpf: ")

    if is_float(usuario):
        if usuarios and valida_cpf(usuario, usuarios):
            contas.append(cria_conta(usuario, contas))
            print("Conta criada com sucesso!")
        else:
            print("Cpf não cadastrado...")
    else:
        print("Digite um cpf válido!")

#Verifica se conta existe
def verifica_conta(conta, contas=[]):
    existe = 0
    id = 0
    for c in contas:
        if conta == c["numero_conta"]: 
            existe += 1 

    if existe == 1:
        return True
    else:
        return False
    
#Acessar contas
def acessar(numero_conta, contas=[]):
    id = 0
    if verifica_conta(numero_conta, contas):
        for i, c in enumerate(contas):
            if numero_conta == c["numero_conta"]:
                id = i
        return id
    else:
        print("Conta inexistente! Para realizar essa operação é preciso ter uma conta válida.")
        return "NEGADO"

#Mostra o a conta e usuário que está sendo acessado    
def mostra_usuario(id, contas=[]):
    print(f" Conta: {contas[id]['numero_conta']}   Usuário: {contas[id]['usuario']}".center(40," "))
    print(40*"-")
        
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

    
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    usuarios = []
    contas = []

    while True:

        opcao = menu()
        #SAQUE
        if opcao == "s" or opcao == "S":
            numero_conta = int(input("Informe o número da conta que deseja acessar: "))
            id = acessar(numero_conta, contas)

            if id != "NEGADO":
                print(" SAQUE ".center(40,"="))            
                mostra_usuario(id, contas)
                saque(data_atual, id, contas)
                    
        #DEPÓSITO
        elif opcao == "d" or opcao == "D":
            numero_conta = int(input("Informe o número da conta que deseja acessar: "))
            id = acessar(numero_conta, contas)

            if id != "NEGADO":
            
                print(" DEPÓSITO ".center(40,"="))
                mostra_usuario(id, contas)           
                deposito(data_atual, id, contas)
                
        #EXTRATO        
        elif opcao == "e" or opcao == "E":
            numero_conta = int(input("Informe o número da conta que deseja acessar: "))
            id = acessar(numero_conta, contas)

            if id != "NEGADO":
                print(" EXTRATO ".center(40,"="))
                mostra_usuario(id, contas)
                extrato(id, contas)

        #CADASTRO CLIENTE
        elif opcao == "c" or opcao == "C":
            print(" CADASTRO DE CLIENTE ".center(40,"="))
            cadastro_cliente(usuarios)
            print(usuarios)

        #CADASTRO CONTA
        elif opcao == "y" or opcao == "Y":
            print(" CADASTRO DE CONTA ".center(40,"="))
            cadastro_conta(usuarios, contas)
            print(contas)


        #ENCERRAR 
        elif opcao == "q" or opcao == "Q":
                print("Volte sempre!")
                break

        else:
            print("Opção inválida!")

main()   

 


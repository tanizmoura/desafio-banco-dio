
#Soma o valor do depósito com a conta
def deposito(valor_deposito, valor_conta):
    valor_conta += valor_deposito
    return valor_conta

#Desconta o valor de saque da conta
def saque(valor_saque, valor_conta):
    valor_conta -= valor_saque
    return valor_conta
    
#Verifica se o valor digitado é um numero válido
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    

#Imprime o menu interativo
menu = """
========= BANCO DIO =========
[S] - Saque
[D] - Depósito
[E] - Extrato
[Q] - Sair
=============================
Opção: 
"""

limite = 500
LIMITE_SAQUE = 3
extrato = ""
valor_conta = 0
qtd_saque = 0


while True:
    opcao = input(menu)

    if opcao == "s" or opcao == "S":
        print(" SAQUE ".center(29,"="))
        while True:

            valor_saque = input("Informe o valor que deseja sacar: R$")

            if is_float(valor_saque):
                valor_saque = float(valor_saque)
                print(valor_saque)
                break
            else:
                print("Digite um valor válido!") 
                print(valor_saque)

        if valor_saque > valor_conta:
            print("Saldo insuficiente...")   

        elif valor_saque > 500:
            print("Limite de saque excedido!")    
        
        elif valor_saque > 0 and valor_saque <= 500 and qtd_saque < LIMITE_SAQUE:
            valor_conta = saque(valor_saque, valor_conta)
            print("Saque realizado com sucesso!")
            extrato += f"Saque no valor de R${valor_saque:.2f}\nSaldo da conta: R${valor_conta:.2f}\n\n"
            qtd_saque += 1

        elif qtd_saque == LIMITE_SAQUE:
            print("Quantidade de saques excedidas. Tente novamente amanhã!")

        else:
            print("Informe um valor maior que zero!")



    elif opcao == "d" or opcao == "D":
        print(" DEPÓSITO ".center(29,"="))

        while True:

            valor_deposito = input("Informe o valor que deseja depositar: R$")

            if is_float(valor_deposito):
                valor_deposito = float(valor_deposito)
                break
            else:
                print("Digite um valor válido!")        
        
        if valor_deposito > 0:
            valor_conta = deposito(valor_deposito, valor_conta)
            print("Depósito realizado com sucesso!")
            extrato += f"Depósito no valor de R${valor_deposito:.2f}\nSaldo da conta: R${valor_conta:.2f}\n\n"
        else:
            print("Informe um valor maior que zero!")
        

    elif opcao == "e" or opcao == "E":
       print(" EXTRATO ".center(29,"="))
       print(extrato)

    elif opcao == "q" or opcao == "Q":
        print("Volte sempre!")
        break

    else:
        print("Opção inválida!")

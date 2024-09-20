menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

saldo = 0
limite_saque = 500
extrato = "Saldo atual: Extrato:\n\n"
numero_saques = 0
LIMITE_SAQUES = 3

def deposito(saldo, valor):
    saldo += valor
    print(f"Saldo após depósito:  R${saldo:.2f}")
    return saldo

def saque(saldo, valor):
    saldo -= valor
    print(f"Saldo após saque:  R${saldo:.2f}")
    return saldo

def exibir_extrato(extrato):
    extrato += f"Saldo atual: R${saldo:.2f}"
    print(extrato)

while True:
    
    opcao = input(menu)
    
    if opcao == "d":
        print(f"Saldo atual: R${saldo:.2f}")
        valor = float(input("Insira o valor que deseja depositar: "))   
        if(valor >= 0):
            saldo = deposito(saldo, valor)
            extrato = extrato + f"Depósito no valor de R${valor:.2f}\n"
        else:
            print("Não é possivel fazer um depósito negativo.")
        
    elif opcao == "s":
        if(numero_saques < LIMITE_SAQUES):
            print(f"Saldo atual: R${saldo:.2f}")
            valor = float(input("Insira o valor que deseja sacar: "))
            if(valor >= 0):
                if(valor <= 500):
                    if(saldo >= valor):
                        saldo = saque(saldo, valor)
                        numero_saques += 1
                        extrato = extrato + f"Saque no valor de R${valor:.2f}\n"
                    else:
                        print("Saldo insuficiente para saque.")
                else:
                    print("Valor acima do limite de saque de R$500,00")
            else:
                print("Não é possivel fazer um saque com valor negativo.")
        else:
            print("Limite de saque diário atingido, tente novamente amanhã.")
           
    
    elif opcao == "e":
        exibir_extrato(extrato)
           
    
    elif opcao == "q":
        break
    
    else:
        print("Operação inválida, por favor selecione novamente a opção desejada.")   
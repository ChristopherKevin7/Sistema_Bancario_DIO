import time

menuPrincipal = """

[c] Cadastrar Usuario
[e] Login
[q] Sair

"""

menuUsuario = """

[d] Depositar
[s] Sacar
[e] Extrato
[t] Trocar Conta
[n] Nova Conta
[q] Voltar

=>"""

saldo = 0
limite_saque = 500
extrato = "Saldo atual: Extrato:\n\n"
LIMITE_SAQUES = 3
usuarios = []
numero_conta_sequencial = 1  
AGENCIA_FIXA = "0001" 

def criarUsuario(nome, data_nascimento, cpf, endereco):
    usuario_existe = verifica_cpf(cpf, usuarios)
    
    if not usuario_existe: 
        usuario = {
            "nome": nome,
            "nasc": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
            "contas": []  
        }
        usuarios.append(usuario)
        print("Usuário cadastrado com sucesso!")
        # Exibir informações do usuário cadastrado
        print("\nDetalhes do usuário cadastrado:")
        print(f"Nome: {usuario['nome']}")
        print(f"Data de nascimento: {usuario['nasc']}")
        print(f"CPF: {usuario['cpf']}")
        print(f"Endereço: {usuario['endereco']}")
        print(f"Contas: {usuario['contas']}")
    else:
        print(f"O CPF de número {cpf} já está cadastrado no sistema.")



def verifica_cpf(cpf, lista_usuarios):
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            return True  # CPF já existe
    return False  # CPF não encontrado


def login(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    print("Nenhum usuário cadastrado com este CPF.")
    return False


def criarConta(usuario):
    global numero_conta_sequencial
    conta = {
        "agencia": AGENCIA_FIXA,
        "numero": numero_conta_sequencial, 
        "saldo": 0,
        "extrato": "Extrato:\n\n",
        "numero_saques": 0 
    }
    usuario["contas"].append(conta)
    numero_conta_sequencial += 1 
    print(f"Conta criada com sucesso! Agência: {conta['agencia']}, Número da conta: {conta['numero']}")


def listarContas(usuario):
    if not usuario["contas"]:
        print("Este usuário não possui contas. Você será direcionado para criar uma nova conta.")
        criarConta(usuario)
    else:
        for conta in usuario["contas"]:
            print(f"Agência: {conta['agencia']} | Número da conta: {conta['numero']} | Saldo: R${conta['saldo']:.2f}")

def deposito(conta, valor):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    conta["saldo"] += valor
    conta["extrato"] += f"Depósito no valor de R${valor:.2f} em {timestamp}\n"
    print(f"Saldo após depósito: R${conta['saldo']:.2f}")


def saque(conta, valor, limite_saque, LIMITE_SAQUES):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Obtém a data e hora atuais
    if conta["numero_saques"] < LIMITE_SAQUES:
        if valor <= conta["saldo"]:
            if valor <= limite_saque:
                conta["saldo"] -= valor
                conta["extrato"] += f"Saque no valor de R${valor:.2f} em {timestamp}\n"
                conta["numero_saques"] += 1
                print(f"Saldo após saque:  R${conta['saldo']:.2f}")
            else:
                print("O valor ultrapassa o limite de saque.")
        else:
            print("Saldo insuficiente.")
    else:
        print("Você atingiu o limite de saques diários.")


def exibir_extrato(conta):
    print(f'{conta["extrato"]} \n\n Saldo atual: R$ {conta["saldo"]:.2f}')


while True:
    
    opcao = input(menuPrincipal)
    
    if opcao == "e":
        cpf = input("Digite seu CPF: ")
        usuario = login(cpf)
        if usuario:
            listarContas(usuario)
            if usuario["contas"]:
                conta_selecionada = int(input("Selecione o número da conta que deseja usar: "))
                conta = None
                for c in usuario["contas"]:
                    if c["numero"] == conta_selecionada:
                        conta = c
                        break

                if conta:
                    while True:
                        opcao = input(menuUsuario)
                        
                        if opcao == "d":
                            print(f"Saldo atual: R${conta['saldo']:.2f}")
                            valor = float(input("Insira o valor que deseja depositar: "))   
                            if valor >= 0:
                                deposito(conta, valor)
                            else:
                                print("Não é possível fazer um depósito negativo.")
                        
                        elif opcao == "s":
                            valor = float(input("Insira o valor que deseja sacar: "))
                            if valor >= 0:
                                saque(conta, valor, limite_saque, LIMITE_SAQUES)
                            else:
                                print("Não é possível fazer um saque com valor negativo.")
                        
                        elif opcao == "e":
                            exibir_extrato(conta)
                        
                        elif opcao == "t":
                            break  # Trocar conta ou sair da sessão atual
                        
                        elif opcao == "n":
                            criarConta(usuario)
                        
                        elif opcao == "q":
                            break
                        
                        else:
                            print("Operação inválida, por favor selecione novamente a opção desejada.")
                else:
                    print("Conta não encontrada.")
    
    elif opcao == "c":
        nome = input("Nome: ")
        nasc = input("Data de nascimento: ")
        cpf = input("CPF: ")
        print("Endereço: ")
        logradouro = input("Logradouro: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Sigla do estado: ")
        endereco = f"{logradouro} - {bairro} - {cidade}/{estado}"
        criarUsuario(nome, nasc, cpf, endereco)
    
    elif opcao == "q":
        print("Saindo...")
        break
    
    else:
        print("Opção inválida!")

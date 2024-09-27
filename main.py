from abc import ABC, abstractmethod
import datetime

class Transacao(ABC):
    """Interface para representar uma transação"""

    @abstractmethod
    def registrar(self, conta):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Historico:
    """Classe para armazenar o histórico de transações"""

    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)


class Conta:
    """Classe que representa uma conta bancária"""

    def __init__(self, saldo: float, numero: int, agencia: str, cliente):
        self.saldo = saldo
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()
        self.saques_dia = 0
        self.ultima_data_saque = None

    def sacar(self, valor: float) -> bool:
        # Verifica se o saque é no mesmo dia; se não for, zera os saques do dia
        hoje = datetime.date.today()
        if self.ultima_data_saque != hoje:
            self.saques_dia = 0
            self.ultima_data_saque = hoje
        
        # Verifica o limite de saques por dia
        if self.saques_dia >= 3:
            print("Limite de 3 saques por dia atingido.")
            return False
        
        if self.saldo >= valor:
            self.saldo -= valor
            self.saques_dia += 1
            return True
        
        print("Saldo insuficiente.")
        return False

    def depositar(self, valor: float) -> bool:
        self.saldo += valor
        return True


class Cliente:
    """Classe que representa um cliente"""

    def __init__(self, cpf: str, nome: str, endereco: str, data_nascimento: str):
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Classe que representa uma pessoa física (herda Cliente)"""

    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(cpf, nome, endereco, data_nascimento)


class ContaCorrente(Conta):
    """Classe que representa uma conta corrente (herda Conta)"""

    def __init__(self, saldo: float, numero: int, agencia: str, cliente, limite: float, limite_saques: int):
        super().__init__(saldo, numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


class Deposito(Transacao):
    """Classe que representa um depósito (herda Transacao)"""

    def __init__(self, valor: float):
        self.valor = valor
        self.data_hora = datetime.datetime.now()  # Armazena a data e hora da transação

    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        timestamp = self.data_hora.strftime('%Y-%m-%d %H:%M:%S')
        return f"Depósito no valor de R${valor:.2f} em {timestamp}\n"


class Saque(Transacao):
    """Classe que representa um saque (herda Transacao)"""

    def __init__(self, valor: float):
        self.valor = valor
        self.data_hora = datetime.datetime.now()  # Armazena a data e hora da transação

    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R${valor:.2f} realizado com sucesso!")

    def __str__(self):
        timestamp = self.data_hora.strftime('%Y-%m-%d %H:%M:%S')
        return f"Saque no valor de R${valor:.2f} em {timestamp}\n"


# Variáveis para armazenamento de dados
usuarios = []
LIMITE_SAQUES = 3  # Limite de 3 saques por dia
limite_saque = 500
numero_conta_global = 1  # Número global de contas

def login(cpf: str):
    """Realiza login de um usuário pelo CPF"""
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None


def listarContas(usuario: Cliente):
    """Lista as contas de um cliente"""
    if usuario.contas:
        print("Contas disponíveis:")
        for conta in usuario.contas:
            print(f"Número da conta: {conta.numero}, Saldo: R${conta.saldo:.2f}")
    else:
        print("Nenhuma conta disponível.")


def criarConta(usuario: Cliente):
    """Cria uma nova conta para o cliente"""
    global numero_conta_global  # Usa a variável global para o número da conta
    nova_conta = ContaCorrente(saldo=0, numero=numero_conta_global, agencia="0001", cliente=usuario, limite=limite_saque, limite_saques=LIMITE_SAQUES)
    usuario.adicionar_conta(nova_conta)
    print(f"Conta {numero_conta_global} criada com sucesso!")
    numero_conta_global += 1  # Incrementa o número global de contas


def criarUsuario(nome: str, nasc: str, cpf: str, endereco: str):
    """Cadastra um novo usuário"""
    novo_cliente = PessoaFisica(cpf, nome, nasc, endereco)
    usuarios.append(novo_cliente)
    print(f"Usuário {nome} cadastrado com sucesso!")


def deposito(conta: Conta, valor: float):
    """Realiza um depósito"""
    deposito = Deposito(valor)
    deposito.registrar(conta)
    print(f"Depósito de R${valor:.2f} realizado com sucesso!")


def saque(conta: Conta, valor: float, limite: float):
    """Realiza um saque, respeitando o limite diário e valor máximo"""
    if valor <= limite:
        if conta.saques_dia <= LIMITE_SAQUES:
            saque = Saque(valor)
            saque.registrar(conta)
            conta.saques_dia += 1
            conta.ultima_data_saque = datetime.date.today()
        else:
            print("Limite de saques diarios atingido")
    else:
        print("Valor do saque excede o limite permitido!")


def exibir_extrato(conta: Conta):
    """Exibe o extrato da conta"""
    print("Extrato:")
    for transacao in conta.historico.transacoes:
        print(transacao)


# Menu do sistema
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
=> """


while True:
    opcao = input(menuPrincipal)

    if opcao == "e":
        cpf = input("Digite seu CPF: ")
        usuario = login(cpf)
        if usuario:
            if not usuario.contas:
                print("Usuário não possui contas, é necessário criar uma conta primeiro.")
                criarConta(usuario)

            while True:
                listarContas(usuario)
                conta_selecionada = int(input("Selecione o número da conta que deseja usar: "))
                conta = None
                for c in usuario.contas:
                    if c.numero == conta_selecionada:
                        conta = c
                        break

                if conta:
                    while True:
                        opcao = input(menuUsuario)

                        if opcao == "d":
                            print(f"Saldo atual: R${conta.saldo:.2f}")
                            valor = float(input("Insira o valor que deseja depositar: "))
                            if valor >= 0:
                                deposito(conta, valor)
                            else:
                                print("Não é possível fazer um depósito negativo.")

                        elif opcao == "s":
                            valor = float(input("Insira o valor que deseja sacar: "))
                            if valor >= 0:
                                saque(conta, valor, limite_saque)
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
        else:
            print("Usuário não encontrado.")

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

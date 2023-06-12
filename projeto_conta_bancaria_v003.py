import json
from abc import ABC, abstractmethod, abstractproperty

class Transacao(ABC):

    @abstractmethod
    def sacar(self):
        pass

    @abstractmethod
    def depositar(self):
        pass

class Historico:
    def __init__(self, saques, depositos):
        self.saques = saques
        self.depositos = depositos
    
    def add_transacao(self, tipo, valor):
        if tipo == '+':
          self.saques += f"{valor}\r\n"
        else:
            self.depositos += f"{valor}\r\n"

class Conta(Transacao):

    def __init__(self, saldo = 0, nro_agencia = 0, nro_conta = 0, historico = Historico("", ""), cliente = 0):
        self.saldo = saldo
        self.nro_agencia = nro_agencia
        self.nro_conta = nro_conta
        self.historico = historico
        self.cliente = cliente
    
    def get_saldo(self):
        return self.saldo
    
    
    #Métodos de classe: Mexem diretamente com dados da classe
    @classmethod
    def criar_conta(cls, cliente, nro_conta):
        #CLS = Referência para a classe
        return cls(0, "0", nro_conta, "", cliente)

    def sacar(self, valor):
        if(self.saldo >= valor):
            self.saldo -= valor
            self.historico.add_transacao('-',f"R$ {valor},00")
            return True
        else:
            return False

    def depositar(self, valor):
        self.saldo += valor
        self.historico.add_transacao('+', f"R$ {valor},00")
        return True

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
        # return(f"Biscicleta {self.modelo} de cor {self.cor} cujo ano é {self.ano} e custa R${self.valor},00")

class ContaCorrente(Conta):
    def __init__(self, limite, nro_saques, **kw):
        super().__init__(**kw)
        self.limite = limite
        self.nro_saques = nro_saques
        self._saques_idx = 0

class Cliente:

    def __init__(self, nome="", data_nascimento="", endereco="", cpf="", contas = []):
        self.nome=nome
        self.data_nascimento=data_nascimento
        self.endereco=endereco
        self.cpf=cpf
        self.contas=contas
    
    def add_conta(self, conta):
        # conta = ContaCorrente(cliente = self.nome, nro_conta = conta.nro_conta, limite = conta.limite, nro_saques = conta.nro_saques)
        
        for cont in self.contas:
            if cont.nro_conta == conta.nro_conta:
                return False
        conta.cliente = self.nome
        self.contas.append(conta)
        return True
    
    def realizar_transacao(self, conta, transacao, valor):
        print(f"avaliando nro_conta: {conta.nro_conta} saldo: {conta.saldo}\n\r")
        for cont in self.contas:
            if conta.nro_conta == cont.nro_conta:
                if transacao == '+':
                    cont.depositar(valor)
                else:
                    if (int(conta._saques_idx) < int(conta.nro_saques)):
                        cont.sacar(valor)
                        conta._saques_idx += 1
                    else:
                        print("Extourou o limite da conta!")
                break;
    
def mostra_contas(objs):
    for obj in objs:
        print(obj)

## -----------------------TESTE ----------------------------------
# c1 = ContaCorrente(nro_conta = 123, limite = 500, nro_saques = 3)
# c2 = ContaCorrente(nro_conta = 456, limite = 500, nro_saques = 3)
# c3 = ContaCorrente(nro_conta = 456, limite = 500, nro_saques = 3)
# cliente1 = Cliente("Mesels", "14/10/1996", "1234-56" "Rua da Hora")

# if cliente1.add_conta(c1) == True:
#     print("Conta cadastrada com sucesso!")
# else:
#     print("Falha ao cadastrar a conta!")

# if cliente1.add_conta(c2) == True:
#     print("Conta cadastrada com sucesso!")
# else:
#     print("Falha ao cadastrar a conta!")

# if cliente1.add_conta(c3) == True:
#     print("Conta cadastrada com sucesso!")
# else:
#     print("Falha ao cadastrar a conta!")

# cliente1.realizar_transacao(c1, '+', 500)
# print(mostra_contas(cliente1.contas))
# cliente1.realizar_transacao(c1, '-', 200)
# print(mostra_contas(cliente1.contas))
## -----------------------TESTE ----------------------------------


menu =  """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [u] Novo Usuario
    [lu] Listar Usuarios
    [c] Nova Conta
    [lc] Listar Contas
    [q] Sair

=> """

usuarios = []
extrato = ""

#Função que verifica se o usuário já foi cadastrado anteriormente
def is_usuario_cadastrado(usuario, usuarios):
    for u in usuarios:
        if u.cpf == usuario.cpf:
            return True
    return False

#Função que cadastra usuários no repositório do banco
def cadastrar_usuario(usuario, usuarios):
    if len(usuarios) == 0:
        usuarios.append(usuario)
    else:
        if is_usuario_cadastrado(usuario, usuarios) == False:
            usuarios.append(usuario)
            print("Operação realizada com sucesso!")
        else:
            print("Operação falhou: Usuario já cadastrado")

#Função que retorna o usuário pelo CPF
def get_usuario(cpf):
    for u in usuarios:
        if u.cpf == cpf:
            return u
    return False

#Função que cadastra contas no repositório de contas do cliente
def cadastrar_contas(conta, contas):
    if is_usuario_cadastrado(conta["usuario"], usuarios) == True:
        contas.append(conta)
        print("Operação realizada com sucesso!")
    else:
        print("Operação falhou: O usuário não está cadastrado")

def atualizar_extrato(valor):
    global extrato
    extrato += f"{valor}"

def exportar_extrato():
    global extrato
    return extrato


#Função que printa todos os clientes do banco
def mostrar_clientes():
    for cliente in usuarios:
        print("--------------Cliente --------------")
        print(cliente.nome)
        print(cliente.data_nascimento)
        print(cliente.cpf)
        print(cliente.endereco)
        print("------------------------------------")


#Função que printa todas as contas de um cliente específico
def mostrar_contas(cliente_cpf):
    cliente_listar = get_usuario(cliente_cpf)
    for c in cliente_listar.contas:
        print(c)

#Função que retorna a conta a partir do número e do cpf do cliente
def get_conta(nro_conta, cliente_cpf):
    cliente_listar = get_usuario(cliente_cpf)
    for c in cliente_listar.contas:
        if(c.nro_conta == nro_conta):
            print(f"achei {c.nro_conta}")
            return c
    return False


while True:
    opcao = input(menu)

    if opcao == "d": #Ok
        mostrar_clientes()
        cpf = input("Digite o cpf do usuário:")
        mostrar_contas(cpf)
        nro_conta = input("Digite o número da conta:")
        valor = float(input("Digite o quanto quer depositar:"))
        conta = get_conta(nro_conta, cpf)
        cliente1 = get_usuario(cpf)
        if conta != False:
            cliente1.realizar_transacao(conta, '+', valor)
        else:
            print("Conta não encontrada!")


    elif opcao == "s": #Ok
        mostrar_clientes()
        cpf = input("Digite o cpf do usuário:")
        mostrar_contas(cpf)
        nro_conta = input("Digite o número da conta:")
        valor = float(input("Digite o quanto quer sacar:"))
        conta = get_conta(nro_conta, cpf)
        cliente1 = get_usuario(cpf)
        if conta != False:
            if float(valor) <= float(conta.limite):
                cliente1.realizar_transacao(conta, '-', valor)
            else:
                print(f"R${valor},00 é acima do limite da conta R${conta.limite}")
        else:
            print("Conta não encontrada!")

    elif opcao == "e":
        print(exportar_extrato())
        print(f"O valor total na conta: {saldo:.2f}\n")
    
    elif opcao == "u": #Ok
        
        nome = input("Digite o nome do usuário:")
        data_nascimento = input("Digite a data de nascimento:")
        cpf = input("Digite o cpf:")
        logradouro = input("Digite o logradouro:")
        bairro = input("Digite o bairro:")
        cidade = input("Digite a cidade:")
        estado = input("Digite o estado")
        endereco = f"{logradouro} {bairro} {cidade} {estado}"
        novo_cliente = Cliente(nome, data_nascimento, endereco, cpf)
        cadastrar_usuario(novo_cliente, usuarios)
    
    elif opcao == "lu": #Ok
        mostrar_clientes()
    
    elif opcao == "c": #Ok
        mostrar_clientes()
        cpf_usuario = input("Selecione o usuário e digite o cpf:")
        cliente_update = get_usuario(cpf_usuario)
        nro_conta = input("Digite o número da conta:")
        limite = input("Digite o limite da conta:")
        nro_saques = input("Digite o número de saques da conta:")
        c1 = ContaCorrente(nro_conta = nro_conta, limite = limite, nro_saques = nro_saques)
        if cliente_update.add_conta(c1) == True:
            print("Conta cadastrada com sucesso!")
        else:
            print("Falha ao cadastrar a conta!")
    
    elif opcao == "lc": #Ok
        mostrar_clientes()
        cpf_usuario = input("Selecione o usuário e digite o cpf:")
        mostrar_contas(cpf)

    elif opcao == "q": #Ok
        print("Finalizando a operação")
        break;

    else:
        print("opção inválida")

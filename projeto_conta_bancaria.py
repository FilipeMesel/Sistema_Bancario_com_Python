# Fomos contratados por um grande banco para desenvolver seu novo sistema.
# Esse banco deseja modernizar suas operações e para isso, escolheu a linguagem Python.
# Para a primeira versão do sistema, devemos implementar apenas 3 operações: depósito, saque e extrato

import json

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
contas = []

numero_conta = 1
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3


def is_usuario_cadastrado(usuario, usuarios):
    for u in usuarios:
        if u['cpf'] == usuario['cpf']:
            return True
    return False

def cadastrar_usuario(usuario, usuarios):
    # usuario_cadastrado = False
    if len(usuarios) == 0:
        usuarios.append(usuario)
    else:
        if is_usuario_cadastrado(usuario, usuarios) == False:
            usuarios.append(usuario)
            print("Operação realizada com sucesso!")
        else:
            print("Operação falhou: Usuario já cadastrado")
    #print("Usuarios: ", usuarios)

def get_usuario(cpf):
    for u in usuarios:
        if u['cpf'] == cpf:
            return u
    return False

def cadastrar_contas(conta, contas):
    if is_usuario_cadastrado(conta["usuario"], usuarios) == True:
        contas.append(conta)
        print("Operação realizada com sucesso!")
    else:
        print("Operação falhou: O usuário não está cadastrado")
    # print("Contas: ", contas)

def atualizar_extrato(valor):
    global extrato
    extrato += f"{valor}"

def exportar_extrato():
    global extrato
    return extrato

def depositar(quantia):
    global extrato
    global saldo
    if quantia > 0:
        status = f"Depósito:  + R$ {quantia:.2f}\n"
        atualizar_extrato(status)
        saldo += quantia
        return True
    else:
        return False

def sacar(quantia):
    global numero_saques
    global LIMITE_SAQUES
    global extrato
    global saldo

    if numero_saques < LIMITE_SAQUES:
        if quantia > 0:
            status = f"Saque:  - R$ {quantia:.2f}\n"
            atualizar_extrato(status)
            saldo -= quantia
            numero_saques+=1
            return 0
        else:
            return 1
    else:
        return 2


while True:
    opcao = input(menu)

    ##OPERAÇÃO DE TESTES CADASTRO DE USUARIOS
    # usuario_teste = {
    #     "nome": "João",
    #     "data_nascimento": "14/10/1996",
    #     "cpf": "12345",
    #     "address": {
    #         "logradouro": "Rua da Hora",
    #         "bairro": "Espinheiro",
    #         "cidade": "Recife",
    #         "estado": "PE"
    #     }
    # }
    # cadastrar_usuario(usuario_teste, usuarios)

    # ##OPERAÇÃO DE TESTES CADASTRO DE CONTAS
    # conta_teste = {
    #     "numero": numero_conta,
    #     "agencia": "0001",
    #     "usuario": usuario_teste
    # }
    # cadastrar_contas(conta_teste, contas)
    # numero_conta += 1
    ##OPERAÇÃO DE TESTES

    if opcao == "d":
        valor = float(input("Digite o quanto quer depositar:"))
        if depositar(valor) == True:
            print("Operação realizada com sucesso!")
        else:
            print("Operação falhou pois o valor é inválido")

    elif opcao == "s":

        valor = float(input("Digite o quanto quer sacar:"))
        status_operacao = sacar(valor)
        if status_operacao == 0:
            print("Operação realizada com sucesso!")
        elif status_operacao == 1:
            print("Erro: A quantia é menor ou igual a zero")
        else:
            print("Erro: você ultrapassou a quantidade de saques")

    elif opcao == "e":
        print(exportar_extrato())
        print(f"O valor total na conta: {saldo:.2f}\n")
    
    elif opcao == "u":
        nome = input("Digite o nome do usuário:")
        data_nascimento = input("Digite a data de nascimento:")
        cpf = input("Digite o cpf:")
        logradouro = input("Digite o logradouro:")
        bairro = input("Digite o bairro:")
        cidade = input("Digite a cidade:")
        estado = input("Digite o estado")
        usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "address": {
                "logradouro": logradouro,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado
            }
        }
        cadastrar_usuario(usuario, usuarios)
    
    elif opcao == "lu":
        print(usuarios)
    
    elif opcao == "c":
        cpf_usuario = input("Digite o cpf do usuario:")
        usuario = get_usuario(cpf_usuario)

        if usuario != False:

            conta = {
                "numero": numero_conta,
                "agencia": "0001",
                "usuario": usuario
            }
            cadastrar_contas(conta, contas)
            numero_conta += 1
        else:
            print("Erro: Usuario não cadastrado")
    
    elif opcao == "lc":
        print(contas)

    elif opcao == "q":
        print("Finalizando a operação")
        break;

    else:
        print("opção inválida")

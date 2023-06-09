# Fomos contratados por um grande banco para desenvolver seu novo sistema.
# Esse banco deseja modernizar suas operações e para isso, escolheu a linguagem Python.
# Para a primeira versão do sistema, devemos implementar apenas 3 operações: depósito, saque e extrato

menu =  """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

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

    elif opcao == "q":
        print("Finalizando a operação")
        break;

    else:
        print("opção inválida")

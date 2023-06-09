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

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Digite o quanto quer depositar:"))
        if valor > 0:
            extrato += f"Depósito:  + R$ {valor:.2f}\n"
            saldo += valor
        else:
            print("Operação falhou pois o valor é inválido")

    elif opcao == "s":
        if numero_saques < LIMITE_SAQUES:
            valor = float(input("Digite o quanto quer sacar:"))
            if valor > 0:
                extrato += f"Saque:  - R$ {valor:.2f}\n"
                saldo -= valor
                numero_saques+=1
            else:
                print("Operação falhou pois o valor é inválido")
        else:
            print("Você atingiu o limite de saques por hoje")

    elif opcao == "e":
        print(extrato)
        print(f"O valor total na conta: {saldo:.2f}\n")

    elif opcao == "q":
        print("Finalizando a operação")
        break;

    else:
        print("opção inválida")

def menu():
    print(
        """
============== TELI BANK =============
|   Selecione a operação desejada:   |
|                                    |
|         [C] - Cadastrar Usuário    |
|         [N] - Nova Conta           |
|         [D] - Depositar            |
|         [S] - Sacar                |
|         [E] - Extrato              |
|         [Q] - Sair                 |
|                                    |
======================================
"""
    )
    return input("\n: ")


def cadastro(lista_clientes):
    print("\nVocê iniciou o processo de Cadastro, seja bem vindo ao Telibank!")
    print("Insira os dados solicitados no formato correto.")
    nome = input("Nome completo: ")
    nasc = input("Data de nascimento no formato (DD/MM/AAAA): ")
    cpf = int(input("CPF (somente números): "))
    end = input("Endereço (Logradouro, número, bairro, cidade, sigla estado): ")

    cliente = {"Nome": nome, "CPF": cpf, "Nascimento": nasc, "Endereço": end}

    existente = [cliente for cliente in lista_clientes if cliente["CPF"] == cpf]

    if existente:
        print("\033[91mErro! O CPF informado já está cadastrado no sistema.\033[0m")
    else:
        lista_clientes.append(cliente)
        print("Cadastro concluído com sucesso.")
        
    return lista_clientes


def nova_conta(lista_clientes, lista_contas, N_AGENCIA):
    print("\nVocê iniciou o processo de Criaçao de nova conta corrente!")
    print("Insira os dados solicitados no formato correto.")

    cpf = int(input("Informe o CPF do usuário: "))

    existente = [cliente for cliente in lista_clientes if cliente["CPF"] == cpf]

    if existente:
        lista_contas.append(
            {
                "agencia": N_AGENCIA,
                "n_conta": len(lista_contas) + 1,
                "cliente": existente[0]["Nome"],
            }
        )
        print(f"Conta corrente criada com sucesso para o usuário {existente[0]["Nome"]}")
    else:
        print("\033[91mErro! CPF informado não pertence a nenhum cliente.\033[0m")
        
    return lista_contas


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"|   Depósito: R$ {valor:.2f}\n"
    else:
        print("\033[91mOperação mal sucedida! O valor informado é inválido.\033[0m")

    return saldo, extrato


def saque(*, saldo, valor, extrato, LIM_SAQUES_DIARIOS, n_saques, LIM_POR_SAQUE):
    if n_saques >= LIM_SAQUES_DIARIOS:
        print(
            "\033[91mOperação mal sucedida! Limite diário de saques excedido.\nPara mais informações verifique o extrato.\033[0m"
        )
    else:
        if valor > LIM_POR_SAQUE:
            print(
                "\033[91mOperação falhou! O valor informado supera o limite máximo por saque.\033[0m"
            )
        elif valor > saldo:
            print("\033[91mOperação falhou! Saldo insuficiente.\033[0m")
        else:
            saldo -= valor
            n_saques += 1
            extrato += f"|   Saque: R$ {valor:.2f}\n"
            print("Saque efetuado! Verifique os detalhes no extrato.")
    return saldo, extrato, n_saques


def mostrar_extrato(saldo, /, *, extrato):
    print("\n============== EXTRATO ==============")
    print("|   Não foram realizadas movimentações." if not extrato else extrato)
    print(f"|   Saldo: R$ {saldo:.2f}")
    print("=====================================")


def main_loop():
    saldo = 0
    extrato = ""
    n_saques = 0

    lista_clientes = []
    lista_contas = []

    LIM_POR_SAQUE = 500
    LIM_SAQUES_DIARIOS = 3
    N_AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao.lower() == "c":
            lista_clientes = cadastro(lista_clientes)

        elif opcao.lower() == "n":
            lista_contas = nova_conta(lista_clientes, lista_contas, N_AGENCIA)

        elif opcao.lower() == "d":
            print('\nVocê selecionou a opção "Depósito!"')
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao.lower() == "s":
            print('\nVocê selecionou a opção "Saque!"')
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, n_saques = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                LIM_POR_SAQUE=LIM_POR_SAQUE,
                n_saques=n_saques,
                LIM_SAQUES_DIARIOS=LIM_SAQUES_DIARIOS,
            )

        elif opcao.lower() == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao.lower() == "q":
            print("\nObrigado por ser nosso cliente! TeliBank agradece.\n\n")
            break
        else:
            print(
                "\nOperação inválida, por favor selecione uma das opções mostradas no menu."
            )


main_loop()

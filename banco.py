import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova conta
    [lc] Listar contas
    [nu] Novo usuário
    [q]  Sair
    => """
    return input(textwrap.dedent(menu_text))

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    elif valor > saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif valor > limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print(extrato if extrato else "Não foram realizadas movimentações.")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n@@@ Usuário não encontrado, criação de conta cancelada. @@@")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    operacoes = {
        "d": lambda: depositar(saldo, float(input("Informe o valor do depósito: ")), extrato),
        "s": lambda: sacar(
            saldo, float(input("Informe o valor do saque: ")), extrato, limite, numero_saques, LIMITE_SAQUES
        ),
        "e": lambda: exibir_extrato(saldo, extrato),
        "nu": lambda: criar_usuario(usuarios),
        "nc": lambda: contas.append(criar_conta(AGENCIA, len(contas) + 1, usuarios)) if criar_conta else None,
        "lc": lambda: listar_contas(contas),
    }

    while True:
        opcao = menu()
        if opcao == "q":
            print("Obrigado por utilizar nosso sistema. Até logo!")
            break
        operacao = operacoes.get(opcao)
        if operacao:
            resultado = operacao()
            if resultado:
                saldo, extrato, numero_saques = resultado if len(resultado) == 3 else resultado + (numero_saques,)
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()

import random


def eh_primo(numero):
    if numero < 2:
        return False

    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False

    return True


def gerar_primo(inicio=100, fim=500):
    while True:
        numero = random.randint(inicio, fim)

        if eh_primo(numero):
            return numero


def diffie_hellman():

    print("=== DIFFIE-HELLMAN ===\n")

    # Senhas privadas
    senha_a = int(input("Digite a senha de A: "))
    senha_b = int(input("Digite a senha de B: "))

    # N deve ser primo
    N = gerar_primo()

    # G deve ser menor que N
    G = random.randint(2, N - 2)

    # Chaves públicas
    chave_publica_a = pow(G, senha_a, N)
    chave_publica_b = pow(G, senha_b, N)

    # Chaves compartilhadas
    chave_compartilhada_a = pow(
        chave_publica_b,
        senha_a,
        N
    )

    chave_compartilhada_b = pow(
        chave_publica_a,
        senha_b,
        N
    )

    print("\n=== VALORES GERADOS ===")

    print(f"G = {G}")
    print(f"N = {N}")

    print("\n=== SENHAS PRIVADAS ===")

    print(f"Senha de A = {senha_a}")
    print(f"Senha de B = {senha_b}")

    print("\n=== CHAVES PÚBLICAS ===")

    print(f"Chave pública de A = {chave_publica_a}")
    print(f"Chave pública de B = {chave_publica_b}")

    print("\n=== CHAVES COMPARTILHADAS ===")

    print(
        f"Chave calculada por A = "
        f"{chave_compartilhada_a}"
    )

    print(
        f"Chave calculada por B = "
        f"{chave_compartilhada_b}"
    )

    if chave_compartilhada_a == chave_compartilhada_b:

        print(
            "\nChave compartilhada gerada com sucesso:"
        )

        print(chave_compartilhada_a)

    else:
        print("\nErro: as chaves são diferentes.")


if __name__ == "__main__":
    diffie_hellman()
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

ARQUIVO_DADOS = 'dados.json'

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r') as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(dados, f, indent=4)

def cadastrar_novo_recurso():
    dados = carregar_dados()

    nome = input("Nome do novo recurso: ")
    unidade = input("Unidade de medida (ex: litros, kg, unidades): ")

    try:
        quantidade = int(input(f"Quantidade inicial ({unidade}): "))
    except ValueError:
        print("Quantidade inválida.")
        return

    novo_recurso = {
        "nome": nome,
        "unidade": unidade,
        "quantidade": quantidade,
        "historico": [{
            "quantidade": quantidade,
            "data": datetime.now().isoformat()
        }]
    }
    dados.append(novo_recurso)
    salvar_dados(dados)
    print("Novo recurso cadastrado com sucesso.")

def adicionar_quantidade():
    dados = carregar_dados()
    recurso = escolher_recurso(dados)
    if not recurso:
        return

    try:
        quantidade = int(input(f"Quantidade a adicionar a '{recurso['nome']}' ({recurso['unidade']}): "))
    except ValueError:
        print("Quantidade inválida.")
        return

    recurso["quantidade"] += quantidade
    recurso["historico"].append({
        "quantidade": quantidade,
        "data": datetime.now().isoformat()
    })

    salvar_dados(dados)
    print("Recurso atualizado com sucesso.")

def remover_quantidade():
    dados = carregar_dados()
    recurso = escolher_recurso(dados)
    if not recurso:
        return

    try:
        quantidade = int(input(f"Quantidade a remover de '{recurso['nome']}' ({recurso['unidade']}): "))
    except ValueError:
        print("Quantidade inválida.")
        return

    if quantidade > recurso["quantidade"]:
        print("Quantidade maior do que a disponível.")
        return

    recurso["quantidade"] -= quantidade
    recurso["historico"].append({
        "quantidade": -quantidade,
        "data": datetime.now().isoformat()
    })

    salvar_dados(dados)
    print("Recurso atualizado com sucesso.")

def escolher_recurso(dados):
    if not dados:
        print("Nenhum recurso disponível.")
        return None

    print("\n--- Recursos disponíveis ---")
    for i, item in enumerate(dados):
        print(f"{i + 1}. {item['nome']} ({item['quantidade']} {item['unidade']})")

    while True:
        try:
            escolha = int(input("Escolha o número do recurso: "))
            if 1 <= escolha <= len(dados):
                return dados[escolha - 1]
            else:
                print("Número inválido.")
        except ValueError:
            print("Digite um número válido.")

def listar_recursos():
    dados = carregar_dados()
    if not dados:
        print("Nenhum recurso cadastrado.")
        return
    for item in dados:
        print(f"{item['nome']}: {item['quantidade']} {item['unidade']}")

def grafico_linha():
    dados = carregar_dados()
    if not dados:
        print("Sem dados para o gráfico.")
        return

    for item in dados:
        nome = item["nome"]
        unidade = item.get("unidade", "")
        entradas = item.get("historico", [])
        if not entradas:
            continue
        entradas.sort(key=lambda x: x["data"])
        datas = [datetime.fromisoformat(x["data"]) for x in entradas]
        quantidades = []
        atual = 0
        for x in entradas:
            atual += x["quantidade"]
            quantidades.append(atual)
        plt.plot(datas, quantidades, label=f"{nome} ({unidade})")

    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    plt.title("Histórico de Recursos")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def grafico_barras():
    dados = carregar_dados()
    if not dados:
        print("Sem dados para o gráfico.")
        return

    nomes = [f"{item['nome']} ({item['unidade']})" for item in dados]
    quantidades = [item['quantidade'] for item in dados]

    plt.bar(nomes, quantidades)
    plt.xlabel("Recurso")
    plt.ylabel("Quantidade")
    plt.title("Totais por Recurso")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

def grafico_pizza():
    dados = carregar_dados()
    if not dados:
        print("Sem dados para o gráfico.")
        return

    nomes = [f"{item['nome']} ({item['unidade']})" for item in dados]
    quantidades = [item['quantidade'] for item in dados]

    plt.pie(quantidades, labels=nomes, autopct='%1.1f%%')
    plt.title("Distribuição de Recursos")
    plt.tight_layout()
    plt.show()

def menu_graficos():
    while True:
        print("\nTipos de gráfico:")
        print("1. Gráfico de Linha (Histórico)")
        print("2. Gráfico de Barras (Totais)")
        print("3. Gráfico de Pizza (Distribuição)")
        print("0. Voltar")
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            grafico_linha()
        elif escolha == '2':
            grafico_barras()
        elif escolha == '3':
            grafico_pizza()
        elif escolha == '0':
            break
        else:
            print("Opção inválida.")

def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar novo recurso")
        print("2. Adicionar quantidade a recurso existente")
        print("3. Remover quantidade de recurso existente")
        print("4. Listar recursos")
        print("5. Gerar gráficos")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            cadastrar_novo_recurso()
        elif opcao == '2':
            adicionar_quantidade()
        elif opcao == '3':
            remover_quantidade()
        elif opcao == '4':
            listar_recursos()
        elif opcao == '5':
            menu_graficos()
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

menu()

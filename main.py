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


def cadastrar_novo_recurso(nome, unidade, quantidade):
    dados = carregar_dados()
    novo = {
        "nome": nome,
        "unidade": unidade,
        "quantidade": quantidade,
        "historico": [{"quantidade": quantidade, "data": datetime.now().isoformat()}]
    }
    dados.append(novo)
    salvar_dados(dados)
    return "Novo recurso cadastrado com sucesso."

def adicionar_quantidade(indice, quantidade):
    dados = carregar_dados()
    if indice < 0 or indice >= len(dados):
        return "Índice inválido."
    recurso = dados[indice]
    recurso["quantidade"] += quantidade
    recurso["historico"].append({"quantidade": quantidade, "data": datetime.now().isoformat()})
    salvar_dados(dados)
    return "Recurso atualizado com sucesso."

def remover_quantidade(indice, quantidade):
    dados = carregar_dados()
    if indice < 0 or indice >= len(dados):
        return "Índice inválido."
    recurso = dados[indice]
    if quantidade > recurso["quantidade"]:
        return "Quantidade maior do que a disponível."
    recurso["quantidade"] -= quantidade
    recurso["historico"].append({"quantidade": -quantidade, "data": datetime.now().isoformat()})
    salvar_dados(dados)
    return "Recurso atualizado com sucesso."

def listar_recursos():
    return carregar_dados()

def gerar_grafico(tipo):
    dados = carregar_dados()
    if not dados:
        return "Sem dados para o gráfico."
    if tipo == 'linha':
        for item in dados:
            hist = sorted(item.get("historico", []), key=lambda x: x["data"])
            datas = [datetime.fromisoformat(i["data"]) for i in hist]
            cumul = 0
            vals = []
            for i in hist:
                cumul += i["quantidade"]
                vals.append(cumul)
            plt.plot(datas, vals, label=f"{item['nome']} ({item.get('unidade','')})")
        plt.xlabel("Data")
        plt.ylabel("Quantidade")
        plt.title("Histórico de Recursos")
    elif tipo == 'barras':
        nomes = [f"{i['nome']} ({i['unidade']})" for i in dados]
        vals = [i['quantidade'] for i in dados]
        plt.bar(nomes, vals)
        plt.xlabel("Recurso")
        plt.ylabel("Quantidade")
        plt.title("Totais por Recurso")
        plt.xticks(rotation=30)
    elif tipo == 'pizza':
        nomes = [f"{i['nome']} ({i['unidade']})" for i in dados]
        vals = [i['quantidade'] for i in dados]
        plt.pie(vals, labels=nomes, autopct='%1.1f%%')
        plt.title("Distribuição de Recursos")
    else:
        return "Tipo de gráfico inválido."
    plt.tight_layout()
    plt.grid(tipo == 'linha')
    plt.legend() if tipo == 'linha' else None
    plt.show()
    return f"Gráfico de {tipo} exibido."


def menu():
    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar novo recurso")
        print("2. Adicionar quantidade")
        print("3. Remover quantidade")
        print("4. Listar recursos")
        print("5. Gerar gráfico")
        print("6. Sair")
        opc = input("Opção: ")

        if opc == '1':
            nome = input("Nome do recurso: ")
            uni = input("Unidade de medida: ")
            try:
                qt = int(input(f"Quantidade inicial ({uni}): "))
            except ValueError:
                print("Quantidade inválida.")
                continue
            msg = cadastrar_novo_recurso(nome, uni, qt)
            print(msg)

        elif opc in ('2', '3'):
            recursos = listar_recursos()
            if not recursos:
                print("Nenhum recurso cadastrado.")
                continue
            for idx, r in enumerate(recursos):
                print(f"{idx+1}. {r['nome']} ({r['quantidade']} {r['unidade']})")
            try:
                sel = int(input("Escolha o número do recurso: ")) - 1
                qt = int(input("Quantidade: "))
            except ValueError:
                print("Entrada inválida.")
                continue
            if opc == '2':
                msg = adicionar_quantidade(sel, qt)
            else:
                msg = remover_quantidade(sel, qt)
            print(msg)

        elif opc == '4':
            recursos = listar_recursos()
            if not recursos:
                print("Nenhum recurso cadastrado.")
            else:
                for r in recursos:
                    print(f"{r['nome']}: {r['quantidade']} {r['unidade']}")

        elif opc == '5':
            print("Tipos de gráfico: 1: Linha 2: Barras 3: Pizza")
            t = input("Escolha: ")
            tipos = {'1':'linha','2':'barras','3':'pizza'}
            if t in tipos:
                msg = gerar_grafico(tipos[t])
                print(msg)
            else:
                print("Opção inválida.")

        elif opc == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            
menu()

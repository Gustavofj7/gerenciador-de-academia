"""Gravação e leitura dos cadastros em arquivos CSV (R4 / US09).

Os arquivos planos.csv e alunos.csv ficam na pasta dados, junto deste
projeto. Assim, os dados são encontrados mesmo quando o programa é
executado a partir de outro diretório.
"""

import csv
import os

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA_PROJETO, "dados")
ARQ_PLANOS = os.path.join(PASTA_DADOS, "planos.csv")
ARQ_ALUNOS = os.path.join(PASTA_DADOS, "alunos.csv")

CAMPOS_PLANOS = ["id", "nome", "valor", "duracao"]
CAMPOS_ALUNOS = ["id", "nome", "telefone", "idade", "id_plano"]

CONVERSORES_PLANOS = {"id": int, "valor": float, "duracao": int}
CONVERSORES_ALUNOS = {"id": int, "idade": int, "id_plano": int}


def salvar_csv(caminho, lista, campos):
    """Grava uma lista de dicionários em um arquivo CSV.

    Parâmetros:
        caminho (str): nome do arquivo, ex.: "planos.csv".
        lista (list): lista de dicionários a gravar.
        campos (list): nomes das colunas, na ordem em que aparecem.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    try:
        # Cria a pasta de destino automaticamente, se ainda não existir.
        pasta_destino = os.path.dirname(os.path.abspath(caminho))
        os.makedirs(pasta_destino, exist_ok=True)

        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
            escritor.writeheader()
            for item in lista:
                escritor.writerow(item)
        return True, f"{len(lista)} registro(s) salvo(s) em {caminho}."
    except OSError as erro:
        return False, f"Não foi possível salvar em {caminho}: {erro}"


def carregar_csv(caminho, campos, conversores):
    """Lê um arquivo CSV e devolve a lista de dicionários com os tipos certos.

    Se o arquivo ainda não existe (primeira execução), devolve lista vazia
    e sucesso True. Se o arquivo existe mas está com erro, devolve
    sucesso False, para não sobrescrever os dados com uma lista vazia.

    Parâmetros:
        caminho (str): nome do arquivo.
        campos (list): colunas esperadas.
        conversores (dict): campo -> função de conversão (int, float...).

    Retorna:
        tuple: (sucesso, lista, mensagem).
    """
    if not os.path.exists(caminho):
        return True, [], f"Nenhum arquivo {caminho} encontrado. Começando vazio."

    lista = []
    try:
        with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
            for linha in csv.DictReader(arquivo):
                item = {}
                for campo in campos:
                    conversor = conversores.get(campo, str)
                    item[campo] = conversor(linha[campo])
                lista.append(item)
    except (OSError, KeyError, ValueError) as erro:
        return False, [], f"Erro ao ler {caminho}: {erro}"
    return True, lista, f"{len(lista)} registro(s) carregado(s) de {caminho}."


def salvar_planos(planos, caminho=ARQ_PLANOS):
    """Grava os planos no arquivo planos.csv.

    Parâmetros:
        planos (list): lista de planos.
        caminho (str): arquivo de destino.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    return salvar_csv(caminho, planos, CAMPOS_PLANOS)


def carregar_planos(caminho=ARQ_PLANOS):
    """Lê os planos do arquivo planos.csv.

    Parâmetros:
        caminho (str): arquivo de origem.

    Retorna:
        tuple: (sucesso, lista de planos, mensagem).
    """
    return carregar_csv(caminho, CAMPOS_PLANOS, CONVERSORES_PLANOS)


def salvar_alunos(alunos, caminho=ARQ_ALUNOS):
    """Grava os alunos no arquivo alunos.csv.

    Parâmetros:
        alunos (list): lista de alunos.
        caminho (str): arquivo de destino.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    return salvar_csv(caminho, alunos, CAMPOS_ALUNOS)


def carregar_alunos(caminho=ARQ_ALUNOS):
    """Lê os alunos do arquivo alunos.csv.

    Parâmetros:
        caminho (str): arquivo de origem.

    Retorna:
        tuple: (sucesso, lista de alunos, mensagem).
    """
    return carregar_csv(caminho, CAMPOS_ALUNOS, CONVERSORES_ALUNOS)

"""Módulo de dados e regras dos PLANOS da academia.

Cada plano é um dicionário com as chaves:
    id (int), nome (str), valor (float), duracao (int, em meses)

As funções recebem o texto digitado pelo usuário (string) e fazem a
validação e a conversão aqui dentro, com try/except. Assim o programa
não fecha por erro de digitação (R3).
"""


def converter_id(texto):
    """Converte um ID digitado em número inteiro.

    Parâmetros:
        texto (str): ID digitado pelo usuário.

    Retorna:
        int ou None: o número, ou None se o texto não for um inteiro.
    """
    try:
        return int(texto.strip())
    except ValueError:
        return None


def gerar_id(lista):
    """Gera o próximo ID livre de uma lista de cadastros.

    Parâmetros:
        lista (list): lista de dicionários que têm a chave "id".

    Retorna:
        int: maior ID existente + 1 (ou 1 se a lista estiver vazia).
    """
    maior = 0
    for item in lista:
        if item["id"] > maior:
            maior = item["id"]
    return maior + 1


def validar_plano(nome, valor_txt, duracao_txt):
    """Valida e converte os dados digitados de um plano.

    Regras:
        - nome não pode ser vazio e deve ter no máximo 30 caracteres;
        - valor mensal deve ser número entre 1 e 10000 (aceita vírgula);
        - duração deve ser número inteiro de meses entre 1 e 24.

    Parâmetros:
        nome (str): nome do plano.
        valor_txt (str): valor mensal digitado.
        duracao_txt (str): duração em meses digitada.

    Retorna:
        tuple: (erro, nome, valor, duracao). Se estiver tudo certo,
        erro é "" (texto vazio); senão traz a mensagem do problema.
    """
    nome = nome.strip()
    if nome == "":
        return "O nome do plano não pode ficar vazio.", None, None, None
    if len(nome) > 30:
        return "O nome do plano deve ter no máximo 30 caracteres.", None, None, None

    try:
        valor = float(valor_txt.strip().replace(",", "."))
    except ValueError:
        return "Valor inválido. Digite um número, ex.: 99,90.", None, None, None
    if valor < 1 or valor > 10000:
        return "O valor deve estar entre R$ 1,00 e R$ 10.000,00.", None, None, None

    try:
        duracao = int(duracao_txt.strip())
    except ValueError:
        return "Duração inválida. Digite um número inteiro de meses.", None, None, None
    if duracao < 1 or duracao > 24:
        return "A duração deve ser de 1 a 24 meses.", None, None, None

    return "", nome, valor, duracao


def nome_plano_existe(planos, nome):
    """Verifica se já existe um plano com o mesmo nome (sem diferenciar maiúsculas).

    Parâmetros:
        planos (list): lista de planos.
        nome (str): nome a procurar.

    Retorna:
        bool: True se o nome já está cadastrado.
    """
    for plano in planos:
        if plano["nome"].lower() == nome.strip().lower():
            return True
    return False


def cadastrar_plano(planos, nome, valor_txt, duracao_txt):
    """Cadastra um novo plano na lista, se os dados forem válidos (US02).

    Parâmetros:
        planos (list): lista de planos (é alterada se der certo).
        nome (str): nome do plano.
        valor_txt (str): valor mensal digitado.
        duracao_txt (str): duração em meses digitada.

    Retorna:
        tuple: (sucesso, mensagem). sucesso é True ou False.
    """
    erro, nome, valor, duracao = validar_plano(nome, valor_txt, duracao_txt)
    if erro != "":
        return False, erro
    if nome_plano_existe(planos, nome):
        return False, f"Já existe um plano chamado '{nome}'."

    novo = {"id": gerar_id(planos), "nome": nome, "valor": valor, "duracao": duracao}
    planos.append(novo)
    return True, f"Plano '{nome}' cadastrado com ID {novo['id']}."


def buscar_plano_por_id(planos, id_plano):
    """Procura um plano pelo ID.

    Parâmetros:
        planos (list): lista de planos.
        id_plano (int): ID procurado.

    Retorna:
        dict ou None: o plano encontrado, ou None se não existir.
    """
    for plano in planos:
        if plano["id"] == id_plano:
            return plano
    return None


def buscar_planos_por_nome(planos, termo):
    """Busca planos por parte do nome, sem diferenciar maiúsculas (US03 / R8).

    Parâmetros:
        planos (list): lista de planos.
        termo (str): parte do nome digitada.

    Retorna:
        list: planos cujo nome contém o termo (lista vazia se nenhum).
    """
    termo = termo.strip().lower()
    encontrados = []
    if termo == "":
        return encontrados
    for plano in planos:
        if termo in plano["nome"].lower():
            encontrados.append(plano)
    return encontrados


def atualizar_plano(planos, id_txt, nome, valor_txt, duracao_txt):
    """Altera um plano existente (US08). Campo em branco mantém o valor atual.

    Parâmetros:
        planos (list): lista de planos (é alterada se der certo).
        id_txt (str): ID do plano digitado.
        nome (str), valor_txt (str), duracao_txt (str): novos valores;
        texto vazio mantém o valor que já está cadastrado.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    id_plano = converter_id(id_txt)
    if id_plano is None:
        return False, "ID inválido. Digite um número."
    plano = buscar_plano_por_id(planos, id_plano)
    if plano is None:
        return False, f"Não existe plano com ID {id_plano}."

    if nome.strip() == "":
        nome = plano["nome"]
    if valor_txt.strip() == "":
        valor_txt = str(plano["valor"])
    if duracao_txt.strip() == "":
        duracao_txt = str(plano["duracao"])

    erro, nome, valor, duracao = validar_plano(nome, valor_txt, duracao_txt)
    if erro != "":
        return False, erro
    for outro in planos:
        if outro["id"] != id_plano and outro["nome"].lower() == nome.lower():
            return False, f"Já existe outro plano chamado '{nome}'."

    plano["nome"] = nome
    plano["valor"] = valor
    plano["duracao"] = duracao
    return True, f"Plano {id_plano} atualizado."


def excluir_plano(planos, alunos, id_txt):
    """Exclui um plano, somente se nenhum aluno estiver vinculado a ele (US08).

    Parâmetros:
        planos (list): lista de planos (é alterada se der certo).
        alunos (list): lista de alunos, para checar o vínculo.
        id_txt (str): ID do plano digitado.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    id_plano = converter_id(id_txt)
    if id_plano is None:
        return False, "ID inválido. Digite um número."
    plano = buscar_plano_por_id(planos, id_plano)
    if plano is None:
        return False, f"Não existe plano com ID {id_plano}."

    for aluno in alunos:
        if aluno["id_plano"] == id_plano:
            return False, f"O plano '{plano['nome']}' tem alunos vinculados e não pode ser excluído."

    planos.remove(plano)
    return True, f"Plano '{plano['nome']}' excluído."


def formatar_plano(plano):
    """Monta uma linha de texto para exibir um plano (f-string / R8).

    Parâmetros:
        plano (dict): plano a ser exibido.

    Retorna:
        str: linha formatada, ex.: "  1 | Mensal          | R$    99.90 |  1 mês(es)".
    """
    nome = plano["nome"][:15]  # fatiamento: corta nomes longos para caber na tabela
    return f"{plano['id']:>3} | {nome:<15} | R$ {plano['valor']:>8.2f} | {plano['duracao']:>2} mês(es)"


def listar_planos(planos):
    """Gera o texto da listagem de todos os planos (US03).

    Parâmetros:
        planos (list): lista de planos.

    Retorna:
        str: tabela pronta para print, ou aviso se não houver planos.
    """
    if len(planos) == 0:
        return "Nenhum plano cadastrado."
    linhas = [" ID | Nome            | Valor       | Duração", "-" * 46]
    for plano in planos:
        linhas.append(formatar_plano(plano))
    return "\n".join(linhas)

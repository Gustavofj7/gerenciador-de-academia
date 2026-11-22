"""Módulo de dados e regras dos ALUNOS da academia.

Cada aluno é um dicionário com as chaves:
    id (int), nome (str), telefone (str), idade (int), id_plano (int)

O aluno se relaciona com o plano pelo campo id_plano (R2).
"""

try:
    from .planos import gerar_id, buscar_plano_por_id, converter_id
except ImportError:
    from planos import gerar_id, buscar_plano_por_id, converter_id


def validar_telefone(telefone):
    """Valida um telefone, aceitando espaços, traços e parênteses.

    Regra: depois de tirar os símbolos, precisa ter de 10 a 11 dígitos
    (DDD + número), ex.: (11) 98765-4321.

    Parâmetros:
        telefone (str): telefone digitado.

    Retorna:
        str: só os dígitos do telefone, ou "" se for inválido.
    """
    digitos = ""
    for caractere in telefone:
        if caractere.isdigit():
            digitos += caractere
        elif caractere not in " -()":
            return ""
    if len(digitos) < 10 or len(digitos) > 11:
        return ""
    return digitos


def validar_aluno(planos, nome, telefone, idade_txt, id_plano_txt):
    """Valida e converte os dados digitados de um aluno.

    Regras:
        - nome não pode ser vazio, máximo 50 caracteres;
        - telefone com 10 ou 11 dígitos;
        - idade inteira entre 12 e 100 anos;
        - ID do plano deve ser de um plano já cadastrado.

    Parâmetros:
        planos (list): lista de planos (para conferir o vínculo).
        nome (str), telefone (str), idade_txt (str), id_plano_txt (str):
        dados como foram digitados.

    Retorna:
        tuple: (erro, dados). erro é "" se estiver tudo certo e dados é
        um dicionário com nome, telefone, idade e id_plano já convertidos.
    """
    nome = nome.strip()
    if nome == "":
        return "O nome do aluno não pode ficar vazio.", None
    if len(nome) > 50:
        return "O nome deve ter no máximo 50 caracteres.", None

    tel = validar_telefone(telefone)
    if tel == "":
        return "Telefone inválido. Use DDD + número, ex.: (11) 98765-4321.", None

    try:
        idade = int(idade_txt.strip())
    except ValueError:
        return "Idade inválida. Digite um número inteiro.", None
    if idade < 12 or idade > 100:
        return "A idade deve estar entre 12 e 100 anos.", None

    try:
        id_plano = int(id_plano_txt.strip())
    except ValueError:
        return "ID do plano inválido. Digite um número.", None
    if buscar_plano_por_id(planos, id_plano) is None:
        return f"Não existe plano com ID {id_plano}. Cadastre o plano antes.", None

    dados = {"nome": nome, "telefone": tel, "idade": idade, "id_plano": id_plano}
    return "", dados


def cadastrar_aluno(alunos, planos, nome, telefone, idade_txt, id_plano_txt):
    """Cadastra um novo aluno, se os dados forem válidos e o plano existir (US04).

    Parâmetros:
        alunos (list): lista de alunos (é alterada se der certo).
        planos (list): lista de planos cadastrados.
        nome, telefone, idade_txt, id_plano_txt (str): dados digitados.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    if len(planos) == 0:
        return False, "Nenhum plano cadastrado. Cadastre um plano primeiro."

    erro, dados = validar_aluno(planos, nome, telefone, idade_txt, id_plano_txt)
    if erro != "":
        return False, erro

    novo = {"id": gerar_id(alunos)}
    novo.update(dados)
    alunos.append(novo)
    plano = buscar_plano_por_id(planos, novo["id_plano"])
    return True, f"Aluno '{novo['nome']}' cadastrado com ID {novo['id']} no plano {plano['nome']}."


def buscar_aluno_por_id(alunos, id_aluno):
    """Procura um aluno pelo ID.

    Parâmetros:
        alunos (list): lista de alunos.
        id_aluno (int): ID procurado.

    Retorna:
        dict ou None: o aluno encontrado, ou None se não existir.
    """
    for aluno in alunos:
        if aluno["id"] == id_aluno:
            return aluno
    return None


def buscar_alunos_por_nome(alunos, termo):
    """Busca alunos por parte do nome, sem diferenciar maiúsculas (US05 / R8).

    Parâmetros:
        alunos (list): lista de alunos.
        termo (str): parte do nome digitada.

    Retorna:
        list: alunos cujo nome contém o termo (lista vazia se nenhum).
    """
    termo = termo.strip().lower()
    encontrados = []
    if termo == "":
        return encontrados
    for aluno in alunos:
        if termo in aluno["nome"].lower():
            encontrados.append(aluno)
    return encontrados


def atualizar_aluno(alunos, planos, id_txt, nome, telefone, idade_txt, id_plano_txt):
    """Altera um aluno existente (US06). Campo em branco mantém o valor atual.

    Parâmetros:
        alunos (list): lista de alunos (é alterada se der certo).
        planos (list): lista de planos, para checar o novo plano.
        id_txt (str): ID do aluno digitado.
        nome, telefone, idade_txt, id_plano_txt (str): novos dados;
        texto vazio mantém o dado que já está cadastrado.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    id_aluno = converter_id(id_txt)
    if id_aluno is None:
        return False, "ID inválido. Digite um número."
    aluno = buscar_aluno_por_id(alunos, id_aluno)
    if aluno is None:
        return False, f"Não existe aluno com ID {id_aluno}."

    if nome.strip() == "":
        nome = aluno["nome"]
    if telefone.strip() == "":
        telefone = aluno["telefone"]
    if idade_txt.strip() == "":
        idade_txt = str(aluno["idade"])
    if id_plano_txt.strip() == "":
        id_plano_txt = str(aluno["id_plano"])

    erro, dados = validar_aluno(planos, nome, telefone, idade_txt, id_plano_txt)
    if erro != "":
        return False, erro

    aluno.update(dados)
    return True, f"Aluno {id_aluno} atualizado."


def excluir_aluno(alunos, id_txt):
    """Exclui um aluno pelo ID (US07). A confirmação é pedida na tela.

    Parâmetros:
        alunos (list): lista de alunos (é alterada se der certo).
        id_txt (str): ID do aluno digitado.

    Retorna:
        tuple: (sucesso, mensagem).
    """
    id_aluno = converter_id(id_txt)
    if id_aluno is None:
        return False, "ID inválido. Digite um número."
    aluno = buscar_aluno_por_id(alunos, id_aluno)
    if aluno is None:
        return False, f"Não existe aluno com ID {id_aluno}."

    alunos.remove(aluno)
    return True, f"Aluno '{aluno['nome']}' excluído."


def formatar_telefone(digitos):
    """Formata os dígitos do telefone para exibição usando fatiamento (R8).

    Parâmetros:
        digitos (str): telefone só com números (10 ou 11 dígitos).

    Retorna:
        str: telefone no formato (11) 98765-4321.
    """
    return f"({digitos[:2]}) {digitos[2:-4]}-{digitos[-4:]}"


def formatar_aluno(aluno, planos):
    """Formata os dados de um aluno para uma linha da tabela.

    O nome do plano é localizado pelo campo id_plano. Se o plano não existir,
    a função mostra um aviso em vez de interromper a listagem.
    """
    plano = buscar_plano_por_id(planos, aluno["id_plano"])
    nome_plano = plano["nome"] if plano else "Plano não encontrado"
    telefone = formatar_telefone(aluno["telefone"])

    return (
        f'{aluno["id"]:>3} | {aluno["nome"]:<30} | '
        f'{telefone:<15} | {aluno["idade"]:>5} | {nome_plano}'
    )


def listar_alunos(alunos, planos):
    """Monta uma tabela com os alunos e os respectivos planos."""
    if not alunos:
        return "Nenhum aluno cadastrado."

    linhas = [
        " ID | Nome                           | Telefone        | Idade | Plano",
        "-" * 78
    ]

    for aluno in alunos:
        linhas.append(formatar_aluno(aluno, planos))

    return "\n".join(linhas)


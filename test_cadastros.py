"""Testes automáticos dos cadastros de planos e alunos (padrão AAA)."""

import os
import tempfile

try:
    from . import alunos as A
    from . import arquivos as ARQ
    from . import planos as P
except ImportError:
    import alunos as A
    import arquivos as ARQ
    import planos as P


def preparar_planos():
    """Cria uma lista de planos de exemplo para os testes."""
    lista = []
    P.cadastrar_plano(lista, "Mensal", "99,90", "1")
    P.cadastrar_plano(lista, "Trimestral", "250", "3")
    return lista


def preparar_alunos(planos):
    """Cria uma lista de alunos de exemplo para os testes."""
    lista = []
    A.cadastrar_aluno(lista, planos, "Ana Souza", "(11) 98765-4321", "17", "1")
    A.cadastrar_aluno(lista, planos, "Bruno Lima", "11912345678", "30", "2")
    return lista


def test_cadastrar_plano_valido():
    """Cadastra um plano com dados válidos."""
    # Preparação
    planos = []
    # Execução
    ok, _ = P.cadastrar_plano(planos, "Mensal", "99,90", "1")
    # Verificação
    assert ok is True
    assert len(planos) == 1


def test_cadastrar_plano_nome_repetido_recusado():
    """Recusa um plano com nome já existente, sem diferenciar maiúsculas."""
    # Preparação
    planos = preparar_planos()
    # Execução
    ok, _ = P.cadastrar_plano(planos, "mensal", "10", "1")
    # Verificação
    assert ok is False
    assert len(planos) == 2


def test_atualizar_plano_mantem_campo_em_branco():
    """Altera um plano e mantém o nome quando o campo vem em branco."""
    # Preparação
    planos = preparar_planos()
    # Execução
    ok, _ = P.atualizar_plano(planos, "1", "", "120", "")
    # Verificação
    assert ok is True
    assert planos[0]["valor"] == 120.0
    assert planos[0]["nome"] == "Mensal"


def test_excluir_plano_com_aluno_vinculado_recusado():
    """Impede excluir um plano que tem aluno vinculado."""
    # Preparação
    planos = preparar_planos()
    alunos = preparar_alunos(planos)
    # Execução
    ok, _ = P.excluir_plano(planos, alunos, "1")
    # Verificação
    assert ok is False
    assert len(planos) == 2


def test_excluir_plano_sem_aluno_vinculado():
    """Exclui um plano que não tem aluno vinculado."""
    # Preparação
    planos = preparar_planos()
    alunos = []
    # Execução
    ok, _ = P.excluir_plano(planos, alunos, "2")
    # Verificação
    assert ok is True
    assert len(planos) == 1


def test_buscar_plano_parcial_sem_diferenca_de_maiuscula():
    """Busca plano por parte do nome sem diferenciar maiúsculas."""
    # Preparação
    planos = preparar_planos()
    # Execução
    encontrados = P.buscar_planos_por_nome(planos, "TRIM")
    # Verificação
    assert len(encontrados) == 1
    assert encontrados[0]["nome"] == "Trimestral"


def test_cadastrar_aluno_com_plano_inexistente_recusado():
    """Recusa aluno com ID de plano que não existe."""
    # Preparação
    planos = preparar_planos()
    alunos = []
    # Execução
    ok, _ = A.cadastrar_aluno(alunos, planos, "Ana", "11987654321", "20", "9")
    # Verificação
    assert ok is False
    assert alunos == []


def test_cadastrar_aluno_telefone_curto_recusado():
    """Recusa aluno com telefone curto demais."""
    # Preparação
    planos = preparar_planos()
    alunos = []
    # Execução
    ok, _ = A.cadastrar_aluno(alunos, planos, "Ana", "123", "20", "1")
    # Verificação
    assert ok is False


def test_atualizar_aluno_idade_invalida_recusada():
    """Recusa alteração de aluno com idade fora da faixa."""
    # Preparação
    planos = preparar_planos()
    alunos = preparar_alunos(planos)
    # Execução
    ok, _ = A.atualizar_aluno(alunos, planos, "1", "", "", "5", "")
    # Verificação
    assert ok is False
    assert alunos[0]["idade"] == 17


def test_excluir_aluno_existente():
    """Exclui um aluno existente."""
    # Preparação
    planos = preparar_planos()
    alunos = preparar_alunos(planos)
    # Execução
    ok, _ = A.excluir_aluno(alunos, "1")
    # Verificação
    assert ok is True
    assert len(alunos) == 1


def test_buscar_aluno_parcial():
    """Busca aluno por parte do nome."""
    # Preparação
    planos = preparar_planos()
    alunos = preparar_alunos(planos)
    # Execução
    encontrados = A.buscar_alunos_por_nome(alunos, "lima")
    # Verificação
    assert len(encontrados) == 1
    assert encontrados[0]["nome"] == "Bruno Lima"


def test_salvar_e_carregar_csv_mantem_dados_e_tipos():
    """Salva e carrega os CSVs e confere que os dados e tipos são mantidos."""
    # Preparação
    planos = preparar_planos()
    alunos = preparar_alunos(planos)
    pasta = tempfile.mkdtemp()
    caminho_planos = os.path.join(pasta, "planos.csv")
    caminho_alunos = os.path.join(pasta, "alunos.csv")
    # Execução
    ARQ.salvar_planos(planos, caminho_planos)
    ARQ.salvar_alunos(alunos, caminho_alunos)
    ok_p, planos_lidos, _ = ARQ.carregar_planos(caminho_planos)
    ok_a, alunos_lidos, _ = ARQ.carregar_alunos(caminho_alunos)
    # Verificação
    assert ok_p and ok_a
    assert planos_lidos == planos
    assert alunos_lidos == alunos
    assert isinstance(alunos_lidos[0]["id_plano"], int)


def test_carregar_arquivo_inexistente_comeca_vazio():
    """Carrega arquivo inexistente e começa com lista vazia."""
    # Preparação
    caminho = os.path.join(tempfile.mkdtemp(), "nao_existe.csv")
    # Execução
    ok, lista, _ = ARQ.carregar_planos(caminho)
    # Verificação
    assert ok is True
    assert lista == []


if __name__ == "__main__":
    testes = [valor for nome, valor in list(globals().items()) if nome.startswith("test_")]
    for teste in testes:
        teste()
        print(f"OK  {teste.__name__}")
    print(f"\n{len(testes)} testes passaram.")

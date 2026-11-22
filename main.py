"""
Sistema de gerenciamento de academia.

Este módulo integra os menus de alunos e planos aos módulos de regras
(alunos.py e planos.py) e à persistência em CSV (arquivos.py).
Pode ser executado como:
    python main.py
"""

# Imports relativos funcionam quando o projeto é executado como pacote.
# O segundo bloco permite executar main.py diretamente dentro da pasta.
try:
    from .alunos import (
        cadastrar_aluno,
        buscar_aluno_por_id,
        buscar_alunos_por_nome,
        atualizar_aluno,
        excluir_aluno,
        formatar_telefone,
        listar_alunos,
    )
    from .planos import (
        cadastrar_plano,
        buscar_plano_por_id,
        buscar_planos_por_nome,
        atualizar_plano,
        excluir_plano,
        formatar_plano,
        listar_planos,
    )
    from .arquivos import (
        carregar_alunos as _carregar_alunos,
        carregar_planos as _carregar_planos,
        salvar_alunos as _salvar_alunos_arquivo,
        salvar_planos as _salvar_planos_arquivo,
    )
except ImportError:
    from alunos import (
        cadastrar_aluno,
        buscar_aluno_por_id,
        buscar_alunos_por_nome,
        atualizar_aluno,
        excluir_aluno,
        formatar_telefone,
        listar_alunos,
    )
    from planos import (
        cadastrar_plano,
        buscar_plano_por_id,
        buscar_planos_por_nome,
        atualizar_plano,
        excluir_plano,
        formatar_plano,
        listar_planos,
    )
    from arquivos import (
        carregar_alunos as _carregar_alunos,
        carregar_planos as _carregar_planos,
        salvar_alunos as _salvar_alunos_arquivo,
        salvar_planos as _salvar_planos_arquivo,
    )


def _salvar_alunos(alunos):
    """Salva os alunos e informa se a gravação foi concluída."""
    sucesso, mensagem = _salvar_alunos_arquivo(alunos)
    print(mensagem)
    return sucesso


def _salvar_planos(planos):
    """Salva os planos e informa se a gravação foi concluída."""
    sucesso, mensagem = _salvar_planos_arquivo(planos)
    print(mensagem)
    return sucesso


def menu_principal():
    """Exibe o menu inicial e devolve a opção escolhida.

    Não recebe parâmetros porque apenas apresenta as opções gerais do sistema.

    Retorna:
        str: opção digitada pelo usuário.
    """
    print("\n========== SISTEMA DA ACADEMIA ==========")
    print("1 - Menu de alunos")
    print("2 - Menu de planos")
    print("0 - Sair")

    # strip() remove espaços extras digitados antes ou depois da opção.
    return input("Escolha uma opção: ").strip()


def exibir_alunos(alunos, planos):
    """Exibe a tabela de alunos usando a função de listagem do módulo alunos.

    Parâmetros:
        alunos (list): alunos cadastrados.
        planos (list): planos usados para mostrar o vínculo de cada aluno.
    """
    print("\n" + listar_alunos(alunos, planos))


def exibir_planos(planos):
    """Exibe a tabela de planos usando a função de listagem do módulo planos.

    Parâmetros:
        planos (list): planos cadastrados.
    """
    print("\n" + listar_planos(planos))


def menu_alunos(alunos, planos):
    """Mostra as operações de alunos e atualiza a lista recebida.

    Parâmetros:
        alunos (list): lista que guarda os alunos cadastrados.
        planos (list): lista de planos disponíveis para vincular aos alunos.

    Retorna:
        list: a mesma lista de alunos, com as alterações realizadas no menu.
    """
    while True:
        print("\n========== MENU DE ALUNOS ==========")
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Buscar aluno")
        print("4 - Alterar aluno")
        print("5 - Excluir aluno")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            # Um aluno precisa estar vinculado a um plano existente.
            if not planos:
                print("Cadastre um plano antes de cadastrar alunos.")
                continue

            exibir_planos(planos)

            # Os dados são recebidos como texto; o módulo alunos faz as validações.
            nome = input("Nome do aluno: ")
            telefone = input("Telefone: ")
            idade = input("Idade: ")
            id_plano = input("ID do plano: ")

            sucesso, mensagem = cadastrar_aluno(
                alunos, planos, nome, telefone, idade, id_plano
            )
            print(mensagem)

            # Só grava o CSV quando o cadastro realmente deu certo.
            if sucesso:
                _salvar_alunos(alunos)

        elif opcao == "2":
            # A função de listagem monta a tabela pronta para imprimir.
            exibir_alunos(alunos, planos)

        elif opcao == "3":
            # A busca pode ser feita por ID ou por parte do nome.
            print("1 - Buscar por ID")
            print("2 - Buscar por nome")
            tipo_busca = input("Escolha o tipo de busca: ").strip()

            if tipo_busca == "1":
                id_txt = input("Digite o ID do aluno: ")

                try:
                    id_aluno = int(id_txt.strip())
                    aluno = buscar_aluno_por_id(alunos, id_aluno)
                except ValueError:
                    aluno = None
                    print("ID inválido. Digite um número inteiro.")

                if aluno is not None:
                    print("\n" + listar_alunos([aluno], planos))
                elif id_txt.strip().isdigit():
                    print("Aluno não encontrado.")

            elif tipo_busca == "2":
                termo = input("Digite o nome ou parte do nome: ")
                encontrados = buscar_alunos_por_nome(alunos, termo)

                if encontrados:
                    print("\n" + listar_alunos(encontrados, planos))
                else:
                    print("Nenhum aluno encontrado.")

            else:
                print("Opção de busca inválida.")

        elif opcao == "4":
            # Primeiro localiza o aluno para mostrar os dados atuais.
            id_txt = input("Digite o ID do aluno que deseja alterar: ")

            try:
                id_aluno = int(id_txt.strip())
                aluno = buscar_aluno_por_id(alunos, id_aluno)
            except ValueError:
                aluno = None
                print("ID inválido. Digite um número inteiro.")

            if aluno is None:
                if id_txt.strip().isdigit():
                    print("Aluno não encontrado.")
                continue

            print("\nDados atuais:")
            print(listar_alunos([aluno], planos))
            print("Digite os novos dados. Deixe em branco para manter o valor atual.")

            # Se o usuário não digitar um novo valor, mantém o dado antigo.
            nome = input(f"Nome [{aluno['nome']}]: ").strip() or aluno["nome"]
            telefone_atual = formatar_telefone(aluno["telefone"])
            telefone = input(f"Telefone [{telefone_atual}]: ").strip() or aluno["telefone"]
            idade = input(f"Idade [{aluno['idade']}]: ").strip() or str(aluno["idade"])
            id_plano = input(f"ID do plano [{aluno['id_plano']}]: ").strip() or str(aluno["id_plano"])

            sucesso, mensagem = atualizar_aluno(
                alunos, planos, id_txt, nome, telefone, idade, id_plano
            )
            print(mensagem)

            if sucesso:
                _salvar_alunos(alunos)

        elif opcao == "5":
            # Confirma antes de remover definitivamente o cadastro.
            id_txt = input("Digite o ID do aluno que deseja excluir: ")
            confirmacao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()

            if confirmacao == "s":
                sucesso, mensagem = excluir_aluno(alunos, id_txt)
                print(mensagem)

                if sucesso:
                    _salvar_alunos(alunos)
            else:
                print("Exclusão cancelada.")

        elif opcao == "0":
            # Retorna ao menu principal sem perder a lista atualizada.
            return alunos

        else:
            print("Opção inválida. Tente novamente.")


def menu_planos(planos, alunos):
    """Mostra as operações de planos e atualiza a lista recebida.

    Parâmetros:
        planos (list): lista que guarda os planos cadastrados.
        alunos (list): lista usada para impedir a exclusão de planos em uso.

    Retorna:
        list: a mesma lista de planos, com as alterações realizadas no menu.
    """
    while True:
        print("\n========== MENU DE PLANOS ==========")
        print("1 - Cadastrar plano")
        print("2 - Listar planos")
        print("3 - Buscar plano")
        print("4 - Alterar plano")
        print("5 - Excluir plano")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do plano: ")
            valor = input("Valor mensal: R$ ")
            duracao = input("Duração em meses: ")

            sucesso, mensagem = cadastrar_plano(planos, nome, valor, duracao)
            print(mensagem)

            if sucesso:
                _salvar_planos(planos)

        elif opcao == "2":
            exibir_planos(planos)

        elif opcao == "3":
            # Pesquisa por nome completo ou por um trecho do nome.
            termo = input("Digite o nome ou parte do nome: ")
            encontrados = buscar_planos_por_nome(planos, termo)

            if encontrados:
                print("\n ID | Nome            | Valor       | Duração")
                print("-" * 46)

                # formatar_plano foi importada no topo, não dentro deste laço.
                for plano in encontrados:
                    print(formatar_plano(plano))
            else:
                print("Nenhum plano encontrado.")

        elif opcao == "4":
            id_txt = input("Digite o ID do plano que deseja alterar: ")

            try:
                id_plano = int(id_txt.strip())
                plano = buscar_plano_por_id(planos, id_plano)
            except ValueError:
                plano = None
                print("ID inválido. Digite um número inteiro.")

            if plano is None:
                if id_txt.strip().isdigit():
                    print("Plano não encontrado.")
                continue

            print("\nDados atuais:")
            print(listar_planos([plano]))
            print("Digite os novos dados. Deixe em branco para manter o valor atual.")

            # Valores vazios mantêm as informações que já estavam cadastradas.
            nome = input(f"Nome [{plano['nome']}]: ").strip() or plano["nome"]
            valor = input(f"Valor mensal [{plano['valor']:.2f}]: ").strip() or str(plano["valor"])
            duracao = input(f"Duração em meses [{plano['duracao']}]: ").strip() or str(plano["duracao"])

            sucesso, mensagem = atualizar_plano(
                planos, id_txt, nome, valor, duracao
            )
            print(mensagem)

            if sucesso:
                _salvar_planos(planos)

        elif opcao == "5":
            id_txt = input("Digite o ID do plano que deseja excluir: ")
            confirmacao = input("Tem certeza que deseja excluir? (s/n): ").strip().lower()

            if confirmacao == "s":
                sucesso, mensagem = excluir_plano(planos, alunos, id_txt)
                print(mensagem)

                if sucesso:
                    _salvar_planos(planos)
            else:
                print("Exclusão cancelada.")

        elif opcao == "0":
            return planos

        else:
            print("Opção inválida. Tente novamente.")


def main(alunos=None, planos=None):
    """Carrega os dados e inicia o menu principal.

    Quando listas são fornecidas, elas são usadas diretamente (útil em testes).
    Caso contrário, os cadastros são carregados dos arquivos CSV.

    Retorna:
        tuple: listas finais de alunos e planos; None se algum CSV não puder
        ser lido, evitando que dados inválidos sejam sobrescritos.
    """
    if alunos is None:
        sucesso, alunos_carregados, mensagem = _carregar_alunos()
        print(mensagem)
        if not sucesso:
            print("O sistema não foi iniciado para proteger os dados dos alunos.")
            return None
        alunos = alunos_carregados

    if planos is None:
        sucesso, planos_carregados, mensagem = _carregar_planos()
        print(mensagem)
        if not sucesso:
            print("O sistema não foi iniciado para proteger os dados dos planos.")
            return None
        planos = planos_carregados

    print("\nDados carregados com sucesso!")
    print(f"Alunos encontrados: {len(alunos)}")
    print(f"Planos encontrados: {len(planos)}")

    try:
        while True:
            opcao = menu_principal()

            if opcao == "1":
                alunos = menu_alunos(alunos, planos)

            elif opcao == "2":
                planos = menu_planos(planos, alunos)

            elif opcao == "0":
                # Faz a última gravação antes de encerrar.
                _salvar_alunos(alunos)
                _salvar_planos(planos)
                print("Dados salvos. Sistema encerrado.")
                return alunos, planos

            else:
                print("Opção inválida. Tente novamente.")
    except (EOFError, KeyboardInterrupt):
        # Ctrl+D ou Ctrl+C no meio de uma pergunta: salva antes de encerrar.
        print("\nEntrada encerrada. Salvando os dados antes de sair...")
        _salvar_alunos(alunos)
        _salvar_planos(planos)
        return alunos, planos


if __name__ == "__main__":
    main()

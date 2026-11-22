# Gerenciador de Academia

## Estrutura

```text
gerenciador-de-academia/
├── __init__.py
├── main.py
├── alunos.py
├── planos.py
├── arquivos.py
├── test_cadastros.py
└── dados/
    ├── alunos.csv
    └── planos.csv
```

## Como executar

Entre na pasta do projeto e execute:

```bash
python main.py
```

## Funcionalidades

- Cadastro, listagem, busca, alteração e exclusão de alunos.
- Cadastro, listagem, busca, alteração e exclusão de planos.
- Validação de telefone, idade, valor, duração e vínculo entre aluno e plano.
- Bloqueio da exclusão de planos que possuem alunos vinculados.
- Salvamento e carregamento automático dos cadastros em arquivos CSV.

Os arquivos CSV ficam dentro de `dados/`, independentemente da pasta de onde o programa é iniciado.

## Dados de teste

Os arquivos `dados/planos.csv` e `dados/alunos.csv` já vêm com registros de exemplo.

Planos de teste:

| ID | Nome       | Valor  | Duração |
|----|------------|--------|---------|
| 1  | Mensal     | 99,90  | 1 mês   |
| 2  | Trimestral | 250,00 | 3 meses |
| 3  | Anual      | 900,00 | 12 meses |

Alunos de teste:

| ID | Nome        | Telefone        | Idade | Plano |
|----|-------------|-----------------|-------|-------|
| 1  | Ana Souza   | (11) 98765-4321 | 17    | 1     |
| 2  | Bruno Lima  | (11) 91234-5678 | 30    | 2     |
| 3  | Carla Dias  | (21) 99988-7766 | 45    | 3     |

Para testar entradas inválidas, use por exemplo: nome em branco, telefone `123`, idade `5`, valor `abc` ou ID de plano inexistente (`9`).

## Testes

Dentro da pasta `gerenciador-de-academia`, execute:

```bash
python test_cadastros.py
```

O script executa os 13 testes automatizados e mostra o resultado de cada um.

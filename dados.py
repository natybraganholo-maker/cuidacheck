"""
dados.py — Módulo de persistência de dados
==========================================
Responsável por salvar e carregar registros do histórico.

Conceitos usados:
- JSON: formato de arquivo para guardar dados estruturados
- open(): abre arquivos para leitura ou escrita
- json.load() / json.dump(): converte entre Python e JSON
- try/except: trata erros (ex: arquivo não existe ainda)
- os.path: verifica se arquivo/pasta existem
"""

import json
import os
from datetime import datetime

# Caminho onde os dados serão salvos
# os.path.dirname(__file__) pega a pasta onde este arquivo está
PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")
ARQUIVO_HISTORICO = os.path.join(PASTA_DADOS, "historico.json")


def garantir_pasta_dados():
    """
    Cria a pasta 'dados/' se ela não existir.
    Chamada antes de qualquer leitura/escrita.
    """
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)
        # makedirs cria pastas intermediárias automaticamente


def carregar_historico():
    """
    Lê o arquivo historico.json e retorna uma lista de registros.

    Retorna:
        list: lista de dicionários com os registros salvos.
              Retorna lista vazia se o arquivo não existir.
    """
    garantir_pasta_dados()

    # try/except: tenta executar o código, e se der erro trata o problema
    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
            # json.load() lê o arquivo e converte para objeto Python
            dados = json.load(arquivo)
            return dados

    except FileNotFoundError:
        # Arquivo ainda não existe — normal na primeira vez
        return []

    except json.JSONDecodeError:
        # Arquivo existe mas está corrompido — retorna vazio e avisa
        print("  ⚠  Arquivo de histórico corrompido. Começando do zero.")
        return []


def salvar_registro(novo_registro):
    """
    Adiciona um novo registro ao histórico e salva no arquivo.

    Se já existir um registro com a mesma data, substitui.
    Isso permite preencher o checklist mais de uma vez no mesmo dia.

    Parâmetros:
        novo_registro (dict): dicionário com os dados do dia
    """
    garantir_pasta_dados()

    historico = carregar_historico()
    data_nova = novo_registro.get("data")

    # Verifica se já existe registro para essa data e remove
    historico = [r for r in historico if r.get("data") != data_nova]
    # Isso é uma "list comprehension": cria nova lista sem o item da mesma data

    # Adiciona o novo registro ao final
    historico.append(novo_registro)

    # Ordena por data (mais antigo primeiro)
    historico.sort(key=lambda r: r.get("data", ""))
    # lambda é uma função anônima: para cada r, retorna o campo "data"

    # Salva tudo de volta no arquivo
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as arquivo:
        # indent=2 formata o JSON com indentação para ficar legível
        # ensure_ascii=False permite caracteres acentuados
        json.dump(historico, arquivo, indent=2, ensure_ascii=False)


def registros_da_semana():
    """
    Retorna apenas os registros dos últimos 7 dias.

    Retorna:
        list: registros filtrados por data
    """
    from datetime import timedelta

    historico = carregar_historico()
    hoje = datetime.now().date()
    sete_dias_atras = hoje - timedelta(days=7)
    # timedelta representa uma duração de tempo

    registros_recentes = []
    for registro in historico:
        try:
            # Converte string "2024-01-15" para objeto date para comparar
            data_reg = datetime.strptime(registro["data"], "%Y-%m-%d").date()
            if data_reg >= sete_dias_atras:
                registros_recentes.append(registro)
        except (ValueError, KeyError):
            # Ignora registros com data inválida ou sem campo data
            continue

    return registros_recentes

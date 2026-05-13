"""
CuidaCheck — Checklist diário de cuidados
==========================================
Projeto 1 do portfólio: cuidado de idosos

Conceitos usados:
- input() para receber dados do usuário
- if/else para lógica condicional
- listas para armazenar tarefas
- dicionários para estruturar dados
- open/write para salvar arquivos
- datetime para registrar data e hora
- funções para organizar o código
- módulos separados (dados.py, relatorio.py)
"""

from datetime import datetime
from dados import carregar_historico, salvar_registro
from relatorio import mostrar_resumo_semanal


# ─── Definição das tarefas de cuidado ──────────────────────────────────────
# Cada tarefa tem: chave única, nome exibido e categoria
TAREFAS = [
    {"id": "medicacao_manha",   "nome": "Medicação da manhã",         "categoria": "Saúde"},
    {"id": "medicacao_noite",   "nome": "Medicação da noite",          "categoria": "Saúde"},
    {"id": "cafe_manha",        "nome": "Café da manhã feito",         "categoria": "Alimentação"},
    {"id": "almoco",            "nome": "Almoço feito",                "categoria": "Alimentação"},
    {"id": "jantar",            "nome": "Jantar feito",                "categoria": "Alimentação"},
    {"id": "hidratacao",        "nome": "Água / hidratação",           "categoria": "Saúde"},
    {"id": "banho",             "nome": "Banho / higiene pessoal",     "categoria": "Higiene"},
    {"id": "exercicio",         "nome": "Exercício / caminhada",       "categoria": "Bem-estar"},
    {"id": "conversa",          "nome": "Conversa / companhia",        "categoria": "Bem-estar"},
    {"id": "consulta_pendente", "nome": "Consulta ou exame pendente?", "categoria": "Saúde"},
]


# ─── Funções auxiliares de exibição ────────────────────────────────────────

def limpar_tela():
    """Imprime linhas em branco para simular limpeza de tela no terminal."""
    print("\n" * 2)


def linha_separadora():
    """Imprime uma linha divisória visual."""
    print("─" * 50)


def exibir_cabecalho():
    """Exibe o cabeçalho do app com data e hora atual."""
    agora = datetime.now()
    # strftime formata a data: %d = dia, %m = mês, %Y = ano, %H:%M = hora:minuto
    data_formatada = agora.strftime("%d/%m/%Y às %H:%M")

    limpar_tela()
    linha_separadora()
    print("  🩺  CuidaCheck — Checklist de Cuidados")
    print(f"  📅  {data_formatada}")
    linha_separadora()


def agrupar_por_categoria(tarefas):
    """
    Organiza a lista de tarefas em um dicionário agrupado por categoria.

    Entrada:  lista de dicionários (TAREFAS)
    Saída:    dicionário {"Saúde": [...], "Alimentação": [...], ...}
    """
    grupos = {}  # dicionário vazio que vamos preencher

    for tarefa in tarefas:
        categoria = tarefa["categoria"]

        # Se a categoria ainda não existe no dicionário, cria uma lista vazia
        if categoria not in grupos:
            grupos[categoria] = []

        # Adiciona a tarefa à lista da categoria correspondente
        grupos[categoria].append(tarefa)

    return grupos


# ─── Fluxo principal do checklist ──────────────────────────────────────────

def executar_checklist():
    """
    Percorre todas as tarefas, pergunta ao usuário e coleta as respostas.
    Retorna um dicionário com os resultados.
    """
    exibir_cabecalho()
    print("\n  Responda com S (sim) ou N (não) para cada item.\n")

    resultados = {}  # vai guardar {id_tarefa: True/False}
    grupos = agrupar_por_categoria(TAREFAS)

    for categoria, tarefas_do_grupo in grupos.items():
        print(f"\n  【 {categoria.upper()} 】")

        for tarefa in tarefas_do_grupo:
            # Loop que fica pedindo resposta até receber S ou N
            while True:
                resposta = input(f"  • {tarefa['nome']}? [S/N]: ").strip().upper()

                if resposta in ("S", "N"):
                    # Converte S/N para True/False
                    resultados[tarefa["id"]] = (resposta == "S")
                    break
                else:
                    print("    ⚠  Digite apenas S ou N.")

    return resultados


def pedir_observacao():
    """Pergunta se o cuidador quer adicionar uma observação livre."""
    print("\n" + "─" * 50)
    print("  Alguma observação sobre o dia de hoje?")
    print("  (pressione Enter para pular)")
    obs = input("  ✏  ").strip()
    return obs if obs else None


def mostrar_resumo_do_dia(resultados, observacao):
    """
    Exibe um resumo visual do checklist preenchido.
    Calcula a porcentagem de tarefas concluídas.
    """
    total = len(resultados)
    concluidas = sum(1 for feito in resultados.values() if feito)
    # sum() com expressão geradora conta quantos valores são True
    porcentagem = (concluidas / total) * 100

    linha_separadora()
    print(f"\n  ✅  {concluidas} de {total} tarefas concluídas ({porcentagem:.0f}%)\n")

    # Mostra ícone diferente para concluído / pendente
    grupos = agrupar_por_categoria(TAREFAS)
    for categoria, tarefas_do_grupo in grupos.items():
        print(f"  {categoria}:")
        for tarefa in tarefas_do_grupo:
            icone = "✓" if resultados[tarefa["id"]] else "✗"
            print(f"    {icone}  {tarefa['nome']}")
        print()

    if observacao:
        print(f"  📝  Obs: {observacao}\n")

    linha_separadora()


# ─── Menu principal ─────────────────────────────────────────────────────────

def menu_principal():
    """Exibe o menu inicial e retorna a opção escolhida."""
    exibir_cabecalho()
    print()
    print("  1.  Preencher checklist de hoje")
    print("  2.  Ver resumo da semana")
    print("  3.  Ver histórico completo")
    print("  4.  Sair")
    print()
    linha_separadora()

    while True:
        opcao = input("  Escolha uma opção [1-4]: ").strip()
        if opcao in ("1", "2", "3", "4"):
            return opcao
        print("  ⚠  Opção inválida. Digite um número de 1 a 4.")


def verificar_checklist_hoje():
    """
    Verifica se o checklist já foi preenchido hoje.
    Retorna True se já existe registro de hoje.
    """
    historico = carregar_historico()
    hoje = datetime.now().strftime("%Y-%m-%d")

    for registro in historico:
        if registro.get("data") == hoje:
            return True
    return False


# ─── Ponto de entrada do programa ───────────────────────────────────────────

def main():
    """
    Função principal — controla o fluxo do app.
    Tudo começa aqui quando você roda: python main.py
    """
    while True:
        opcao = menu_principal()

        if opcao == "1":
            # Verifica se já preencheu hoje
            if verificar_checklist_hoje():
                limpar_tela()
                linha_separadora()
                print("\n  ⚠  Você já preencheu o checklist hoje!")
                print("  Quer preencher novamente? Isso substituirá o registro atual.")
                confirmar = input("  Continuar? [S/N]: ").strip().upper()
                if confirmar != "S":
                    continue

            # Executa o checklist e salva
            resultados = executar_checklist()
            observacao = pedir_observacao()
            mostrar_resumo_do_dia(resultados, observacao)

            # Monta o registro completo para salvar
            registro = {
                "data": datetime.now().strftime("%Y-%m-%d"),
                "hora": datetime.now().strftime("%H:%M"),
                "resultados": resultados,
                "observacao": observacao,
            }
            salvar_registro(registro)
            print("\n  💾  Registro salvo com sucesso!\n")

        elif opcao == "2":
            mostrar_resumo_semanal()

        elif opcao == "3":
            historico = carregar_historico()
            limpar_tela()
            linha_separadora()
            print(f"\n  📋  Histórico completo ({len(historico)} registros)\n")

            if not historico:
                print("  Nenhum registro encontrado ainda.\n")
            else:
                for reg in historico[-10:]:  # mostra os últimos 10
                    total = len(reg["resultados"])
                    feitos = sum(1 for v in reg["resultados"].values() if v)
                    print(f"  {reg['data']} {reg['hora']}  —  {feitos}/{total} tarefas")
                    if reg.get("observacao"):
                        print(f"    📝 {reg['observacao']}")
            linha_separadora()

        elif opcao == "4":
            print("\n  Até logo! Cuide bem. 💙\n")
            break  # sai do loop while e encerra o programa

        input("\n  [Enter para continuar]")


# Essa condição garante que main() só roda quando você executa
# o arquivo diretamente (python main.py), não quando outro
# arquivo importa este módulo.
if __name__ == "__main__":
    main()

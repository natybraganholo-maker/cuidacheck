"""
relatorio.py — Módulo de relatórios
=====================================
Gera resumos e análises do histórico de cuidados.

Conceitos usados:
- Funções com múltiplos retornos
- Manipulação de listas e dicionários
- Cálculos com dados (média, contagem)
- Formatação de strings com f-strings
"""

from dados import registros_da_semana
from datetime import datetime


# Importa as tarefas do main para não duplicar a definição
# Isso é um padrão importante: definir dados em um só lugar
NOMES_TAREFAS = {
    "medicacao_manha":   "Medicação da manhã",
    "medicacao_noite":   "Medicação da noite",
    "cafe_manha":        "Café da manhã feito",
    "almoco":            "Almoço feito",
    "jantar":            "Jantar feito",
    "hidratacao":        "Água / hidratação",
    "banho":             "Banho / higiene pessoal",
    "exercicio":         "Exercício / caminhada",
    "conversa":          "Conversa / companhia",
    "consulta_pendente": "Consulta ou exame pendente?",
}


def calcular_estatisticas(registros):
    """
    Calcula estatísticas a partir de uma lista de registros.

    Retorna um dicionário com:
    - total_dias: quantos dias têm registro
    - media_conclusao: % média de tarefas concluídas por dia
    - por_tarefa: {id: % de dias em que foi feita}
    - dias_completos: dias com 100% de conclusão
    """
    if not registros:
        return None

    total_dias = len(registros)
    porcentagens_diarias = []
    contagem_por_tarefa = {}  # {id: número de dias concluído}

    for registro in registros:
        resultados = registro.get("resultados", {})

        if not resultados:
            continue

        # Calcula % de conclusão do dia
        total = len(resultados)
        feitos = sum(1 for v in resultados.values() if v)
        porcentagens_diarias.append((feitos / total) * 100)

        # Conta quantas vezes cada tarefa foi feita
        for id_tarefa, feito in resultados.items():
            if id_tarefa not in contagem_por_tarefa:
                contagem_por_tarefa[id_tarefa] = 0
            if feito:
                contagem_por_tarefa[id_tarefa] += 1

    # Calcula média de conclusão
    if porcentagens_diarias:
        media = sum(porcentagens_diarias) / len(porcentagens_diarias)
    else:
        media = 0

    # Converte contagens em porcentagens
    porcentagem_por_tarefa = {}
    for id_tarefa, contagem in contagem_por_tarefa.items():
        porcentagem_por_tarefa[id_tarefa] = (contagem / total_dias) * 100

    # Conta dias com 100% de conclusão
    dias_completos = sum(1 for p in porcentagens_diarias if p == 100)

    return {
        "total_dias": total_dias,
        "media_conclusao": media,
        "por_tarefa": porcentagem_por_tarefa,
        "dias_completos": dias_completos,
    }


def identificar_alertas(stats):
    """
    Analisa as estatísticas e gera alertas para tarefas críticas
    que estão sendo negligenciadas.

    Tarefas de saúde com menos de 80% de adesão geram alerta.
    """
    if not stats:
        return []

    TAREFAS_CRITICAS = ["medicacao_manha", "medicacao_noite", "hidratacao"]
    alertas = []

    for id_tarefa in TAREFAS_CRITICAS:
        porcentagem = stats["por_tarefa"].get(id_tarefa, 0)
        if porcentagem < 80:
            nome = NOMES_TAREFAS.get(id_tarefa, id_tarefa)
            alertas.append({
                "tarefa": nome,
                "porcentagem": porcentagem,
            })

    return alertas


def mostrar_resumo_semanal():
    """
    Exibe o relatório semanal no terminal de forma visual.
    """
    registros = registros_da_semana()

    print("\n" + "─" * 50)
    print("  📊  RESUMO DOS ÚLTIMOS 7 DIAS")
    print("─" * 50)

    if not registros:
        print("\n  Nenhum registro encontrado nos últimos 7 dias.")
        print("  Preencha o checklist diário para ver estatísticas aqui.\n")
        print("─" * 50)
        return

    stats = calcular_estatisticas(registros)

    if not stats:
        print("\n  Não foi possível calcular estatísticas.\n")
        return

    # Resumo geral
    print(f"\n  📅  Dias registrados: {stats['total_dias']}/7")
    print(f"  ✅  Média de conclusão: {stats['media_conclusao']:.0f}%")
    print(f"  🌟  Dias completos (100%): {stats['dias_completos']}")

    # Barra de progresso textual
    barra = gerar_barra_progresso(stats["media_conclusao"])
    print(f"\n  {barra}")

    # Detalhamento por tarefa
    print("\n  ─ Adesão por tarefa ─────────────────────────")

    # Ordena tarefas da menor para maior adesão
    tarefas_ordenadas = sorted(
        stats["por_tarefa"].items(),
        key=lambda x: x[1]  # ordena pelo valor (porcentagem)
    )

    for id_tarefa, porcentagem in tarefas_ordenadas:
        nome = NOMES_TAREFAS.get(id_tarefa, id_tarefa)
        icone = "🟢" if porcentagem >= 80 else ("🟡" if porcentagem >= 50 else "🔴")
        # Operador ternário: valor_se_verdadeiro if condição else valor_se_falso
        print(f"  {icone}  {nome:<30} {porcentagem:.0f}%")
        # {nome:<30} alinha o texto à esquerda com 30 caracteres de largura

    # Alertas de atenção
    alertas = identificar_alertas(stats)
    if alertas:
        print("\n  ─ ⚠  Atenção ────────────────────────────────")
        for alerta in alertas:
            print(f"  • {alerta['tarefa']} está abaixo de 80% de adesão ({alerta['porcentagem']:.0f}%)")
        print()

    # Observações da semana
    obs_da_semana = [
        (r["data"], r["observacao"])
        for r in registros
        if r.get("observacao")
    ]

    if obs_da_semana:
        print("  ─ Observações da semana ──────────────────────")
        for data, obs in obs_da_semana:
            # Converte "2024-01-15" para "15/01"
            data_fmt = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m")
            print(f"  {data_fmt}  {obs}")
        print()

    print("─" * 50)


def gerar_barra_progresso(porcentagem, largura=30):
    """
    Gera uma barra de progresso textual.

    Exemplo: [████████████░░░░░░░░░░░░░░░░░░] 42%

    Parâmetros:
        porcentagem: número de 0 a 100
        largura: quantidade de caracteres da barra
    """
    preenchido = int((porcentagem / 100) * largura)
    vazio = largura - preenchido

    barra = "█" * preenchido + "░" * vazio
    return f"[{barra}] {porcentagem:.0f}%"

# CuidaCheck

Checklist diário de cuidados para familiares cuidadores de idosos.

## O problema

No Brasil, milhões de pessoas cuidam de familiares idosos de forma informal e sem nenhuma ferramenta de apoio. É fácil esquecer uma medicação, perder o histórico de uma consulta ou não perceber padrões que indicam deterioração na saúde do familiar.

O CuidaCheck resolve a parte mais básica disso: garantir que as tarefas essenciais do dia foram feitas e registradas.

## O que o app faz

- Checklist diário com tarefas de saúde, alimentação, higiene e bem-estar
- Salva histórico local em JSON
- Relatório semanal com porcentagem de adesão por tarefa
- Alertas automáticos para tarefas críticas (medicação, hidratação) com baixa adesão
- Campo de observação livre por dia

## Como rodar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/cuidacheck.git
cd cuidacheck

# Nenhuma dependência externa necessária — só Python 3.8+
python main.py
```

## Estrutura do projeto

```
cuidacheck/
├── main.py          # Ponto de entrada e fluxo principal
├── dados.py         # Leitura e escrita do histórico em JSON
├── relatorio.py     # Cálculo de estatísticas e relatório semanal
├── dados/
│   └── historico.json   # Gerado automaticamente
└── README.md
```

## Conceitos de Python praticados

| Conceito | Onde aparece |
|---|---|
| `input()` e validação | Loop de perguntas em `main.py` |
| `if/else` e operador ternário | Lógica de ícones em `relatorio.py` |
| Listas e list comprehension | Filtros em `dados.py` |
| Dicionários e dicionários aninhados | Estrutura de tarefas e registros |
| `open()`, `json.load/dump` | Persistência em `dados.py` |
| `datetime` e `timedelta` | Datas em `dados.py` e `relatorio.py` |
| Funções com parâmetros e retorno | Todos os módulos |
| `try/except` | Tratamento de arquivo em `dados.py` |
| `lambda` e `sorted()` | Ordenação em `relatorio.py` |
| Módulos separados | Organização em 3 arquivos |


---

Projeto desenvolvido como parte de um portfólio de desenvolvimento focado em soluções para cuidadores de idosos.

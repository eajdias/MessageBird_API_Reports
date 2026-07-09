# Standalone Report Generator - MessageBird Omnichannel

Ferramenta autonoma para sincronizacao de dados e geracao de relatorios avancados baseados na API Omnichannel da MessageBird. Funciona de forma completamente isolada, sem depender de ferramentas conversacionais (MCP).

## Visao Geral

| Recurso | Descricao |
|:--------|:----------|
| **Sincronizacao** | Espelha contatos, conversas e mensagens da API para SQLite local |
| **Relatorios** | Dashboards Excel com ART, NPS, SLA e metricas por agente/departamento |
| **Auditoria** | Planilhas de contatos, demandas e Ordens de Servico em PDF |
| **Setores** | Filtragem por grupos organizacionais (Comercial, Suporte, etc.) |

## Inicio Rapido

### 1. Instalacao

```
# Copiar template de ambiente
cp config/.env.example config/.env
cp config/business_config.json.example config/business_config.json

# Instalar dependencias
uv sync
```

### 2. Primeira Sincronizacao

Para um banco com dados de um periodo especifico (ex: ultimo mes):

```
uv run python main.py sync --year 2026 --month 6
```

### 3. Gerar Relatorio

```
uv run python main.py report --year 2026 --month 6

# Relatorio de periodo personalizado
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26
```

## Comandos Disponiveis

### Sincronizacao do Banco de Dados

| Comando | Descricao | Quando usar |
|:--------|:----------|:------------|
| `uv run python main.py sync` | Incremental (ultimos 60 min) | Cron job a cada hora |
| `uv run python main.py sync --messages-days 1` | Diario (ultimo dia com mensagens) | Cron job diario |
| `uv run python main.py sync --year 2026 --month 6` | Mes especifico (conversas + mensagens) | Backfill de um mes |
| `uv run python main.py sync --messages-days 7` | Ultimos N dias com mensagens | Periodo personalizado |

### Geracao de Relatorios

| Comando | Descricao | Saida |
|:--------|:----------|:------|
| `uv run python main.py report --year 2026 --month 6` | Relatorio mensal | `reports/2026/2026-06/` |
| `uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26` | Periodo personalizado | `reports/20260525_20260626/` |
| `uv run python main.py report --year 2026` | Relatorio anual consolidado | `reports/2026/` |
| `uv run python main.py total` | Todo o historico do banco | `reports/total/` |

### Filtrar por Setor

Adicione `--sector "Nome do Setor"` para gerar apenas para um grupo:

```
uv run python main.py report --year 2026 --month 6 --sector "Suporte Tecnico"
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26 --sector "Comercial"
uv run python main.py report --year 2026 --sector "Gerencia"
uv run python main.py total --sector "Financeiro"
```

## Estrutura de Saida

### Relatorio Mensal

```
reports/2026/2026-06/
  Dashboard_Executivo_GLOBAL_2026_06.xlsx    # Dashboard consolidado
  README.md                                  # Resumo executivo
  Suporte_Tecnico/
    Dashboard_Executivo_Suporte_Tecnico_2026_06.xlsx
    auditoria/
      auditoria_contatos.xlsx                # Lista de contatos
      auditoria_os.xlsx                      # Ordens de servico
      OS/                                    # PDFs individuais
  Comercial/
    ...
```

### Relatorio de Periodo Personalizado

```
reports/20260525_20260626/
  Dashboard_Executivo_GLOBAL_20260525_20260626.xlsx
  README.md
  Suporte_Tecnico/
    ...
```

### Relatorio Anual

```
reports/2026/
  Dashboard_Executivo_ANUAL_2026.xlsx        # Inclui aba "Evolucao Mensal"
  README.md
  Suporte_Tecnico/
    Dashboard_Anual_Suporte_Tecnico_2026.xlsx
    ...
```

## Ajuda

```
uv run python main.py --help
uv run python main.py report --help
uv run python main.py sync --help
```

## Documentacao Completa

- [Guia de Uso](docs/guia_de_uso.md) - Instrucoes detalhadas de cada comando
- [Configuracao](docs/configuracao.md) - Como preencher `.env` e `business_config.json`
- [Arquitetura](docs/arquitetura_e_desenvolvimento.md) - Padroes e estrutura do codigo
- [Testes Manuais](docs/testes_manuais.md) - Procedimentos de teste

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependencias)
- Chave de API da MessageBird (Bird Conversations API)

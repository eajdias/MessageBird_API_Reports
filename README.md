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

```bash
# Copiar template de ambiente
cp config/.env.example config/.env

# Editar com suas credenciais da MessageBird
nano config/.env

# Copiar template de configuracao de negocios
cp config/business_config.json.example config/business_config.json

# Editar com seus agentes e departamentos
nano config/business_config.json

# Instalar dependencias
make install
```

### 2. Primeira Sincronizacao

Para um banco com dados de um periodo especifico (ex: ultimo mes):

```bash
# Sincronizar um mes inteiro (conversas + mensagens)
make sync-monthly YEAR=2026 MONTH=6
```

### 3. Gerar Relatorio

```bash
# Relatorio mensal
make report YEAR=2026 MONTH=6

# Relatorio de periodo personalizado
make report-dates FROM=2026-05-25 TO=2026-06-26
```

## Comandos Disponiveis

### Sincronizacao do Banco de Dados

| Comando | Descricao | Quando usar |
|:--------|:----------|:------------|
| `make sync` | Incremental (ultimos 60 min) | Cron job a cada hora |
| `make sync-daily` | Diario (ultimo dia com mensagens) | Cron job diario |
| `make sync-monthly YEAR=2026 MONTH=6` | Mes especifico (conversas + mensagens) | Backfill de um mes |
| `make sync-daily --messages-days 7` | Ultimos N dias com mensagens | Periodo personalizado |

### Geracao de Relatorios

| Comando | Descricao | Saida |
|:--------|:----------|:------|
| `make report YEAR=2026 MONTH=6` | Relatorio mensal | `reports/2026/2026-06/` |
| `make report-dates FROM=2026-05-25 TO=2026-06-26` | Periodo personalizado | `reports/20260525_20260626/` |
| `make annual YEAR=2026` | Relatorio anual consolidado | `reports/2026/` |
| `make total` | Todo o historico do banco | `reports/total/` |

### Filtrar por Setor

Adicione `SECTOR="Nome do Setor"` para gerar apenas para um grupo:

```bash
make report YEAR=2026 MONTH=6 SECTOR="Suporte Tecnico"
make report-dates FROM=2026-05-25 TO=2026-06-26 SECTOR="Comercial"
make annual YEAR=2026 SECTOR="Gerencia"
make total SECTOR="Financeiro"
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

## Uso Direto via Python

Se precisar de controle fino, execute diretamente:

```bash
# Ver ajuda completa
uv run python main.py --help
uv run python main.py report --help
uv run python main.py sync --help

# Sincronizar periodo especifico
uv run python main.py sync --year 2026 --month 6

# Gerar relatorio de periodo personalizado
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26
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

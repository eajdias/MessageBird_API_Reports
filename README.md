# Standalone Report Generator — MessageBird Omnichannel

Ferramenta autônoma para sincronização de dados e geração de relatórios avançados baseados na API Omnichannel da MessageBird (Bird). Funciona de forma isolada, e foi desenhada para ser **reutilizável por qualquer empresa** — todo o comportamento de negócio é externalizado em arquivos de configuração.

## Visão Geral

| Recurso | Descrição |
|:--------|:----------|
| **Sincronização** | Espelha contatos, conversas e mensagens da API para um SQLite local (`m_bird.db`) |
| **Relatórios** | Dashboards Excel com ART, NPS, SLA e métricas por agente/departamento/grupo |
| **Auditoria** | Planilhas de contatos, demandas e Ordens de Serviço (PDF) |
| **BSC** | Balanced Scorecard com metas/pesos configuráveis por empresa |
| **Setores** | Filtragem por grupos organizacionais (`--sector`) |

## Arquivos de Configuração

Toda a parametrização de negócio vive em arquivos na **raiz** (gitignored na versão real; apenas os `.example` são versionados):

| Arquivo | Conteúdo | Editado por |
|:-------|:---------|:------------|
| `.env` | Segredos e ambiente (API key, workspace, fuso horário, frases de parsing) | TI / DevOps |
| `business_config.yaml` | Mapas operacionais: departamentos, motivos, ocorrências, idiomas, roteamento e agentes | Operacional |
| `business_bsc.yaml` | BSC/KPIs, metas, pesos, cortes de NPS e limites de métricas (SLA/ART/duração) | Gestão / RH |

> Para adaptar o projeto a outra empresa, basta editar os dois arquivos `.yaml` e o `.env` — **sem mexer em código**. Veja `docs/configuracao.md`.

## Início Rápido

### 1. Instalação

```bash
# Copiar templates de ambiente e negócio
cp .env.example .env
cp business_config.yaml.example business_config.yaml
cp business_bsc.yaml.example business_bsc.yaml

# Instalar dependências (uv cria o venv e instala tudo)
uv sync
```

Edite `.env` com suas credenciais da MessageBird e ajuste os `.yaml` para a sua operação.

### 2. Primeira Sincronização

```bash
# Mês específico (ex.: junho de 2026), baixa conversas + mensagens
uv run python main.py sync --year 2026 --month 6
```

### 3. Gerar Relatório

```bash
uv run python main.py report --year 2026 --month 6

# Período personalizado (datas livres)
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26
```

## Comandos Disponíveis

### Sincronização (`sync`)

| Comando | Descrição | Quando usar |
|:--------|:----------|:------------|
| `uv run python main.py sync` | Incremental (últimos 60 min) | Cron a cada hora |
| `uv run python main.py sync --messages-days 1` | Diário (último dia com mensagens) | Cron diário |
| `uv run python main.py sync --year 2026 --month 6` | Mês específico (conversas + mensagens) | Backfill de um mês |
| `uv run python main.py sync --messages-days 7` | Últimos N dias com mensagens | Período personalizado |

### Geração de Relatórios

| Comando | Descrição | Saída |
|:--------|:----------|:------|
| `uv run python main.py report --year 2026 --month 6` | Relatório mensal | `reports/2026/2026-06/` |
| `uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26` | Período personalizado | `reports/20260525_20260626/` |
| `uv run python main.py report --year 2026` | Relatório anual consolidado | `reports/2026/` |
| `uv run python main.py total` | Todo o histórico do banco | `reports/total/` |

Filtre por setor com `--sector "Nome do Setor"`:

```bash
uv run python main.py report --year 2026 --month 6 --sector "Suporte Tecnico"
uv run python main.py total --sector "Financeiro"
```

Opções comuns: `--config-path` (default `business_config.yaml`), `--bsc-config-path` (default `business_bsc.yaml`), `--db-path` (default `m_bird.db`), `--output-dir` (default `reports`), `--skip-os`.

## Estrutura de Saída

### Relatório Mensal

```
reports/2026/2026-06/
  Dashboard_Executivo_GLOBAL_2026_06.xlsx    # Dashboard consolidado
  README.md                                  # Resumo executivo
  Suporte_Tecnico/
    Dashboard_Executivo_Suporte_Tecnico_2026_06.xlsx
    auditoria/
      auditoria_contatos.xlsx                # Lista de contatos
      auditoria_os.xlsx                      # Ordens de serviço
      OS/                                    # PDFs individuais
  Comercial/
    ...
```

### Relatório Anual / Período / Total

Seguem o mesmo padrão, na pasta `reports/2026/`, `reports/20260525_20260626/` ou `reports/total/`.

## Skills para IA (opencode)

O projeto inclui diretrizes para o assistente de código **opencode**:
- `AGENTS.md` (raiz): visão geral do projeto e catálogo de skills.
- `.opencode/skills/`: `arch-guard`, `sync-maintainer`, `report-architect`, `add-business-metric` e `business-config`.

A skill **`business-config`** é o ponto de partida para adaptar mapas, KPIs, NPS e ambiente a uma nova empresa.

## Ajuda

```bash
uv run python main.py --help
uv run python main.py report --help
uv run python main.py sync --help
```

## Documentação Completa

- [Guia de Uso](docs/guia_de_uso.md) — instruções detalhadas de cada comando
- [Configuração](docs/configuracao.md) — como preencher `.env`, `business_config.yaml` e `business_bsc.yaml`
- [Arquitetura](docs/arquitetura_e_desenvolvimento.md) — padrões e estrutura do código
- [Testes Manuais](docs/testes_manuais.md) — procedimentos de validação

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências)
- Chave de API da MessageBird (Bird Conversations API)

# Guia de Uso: Standalone Report & Sync Tool

Este guia explica como usar cada funcionalidade da ferramenta de sincronizacao e relatorios do MessageBird Omnichannel.

---

## 1. Instalacao e Configuracao

### 1.1 Instalando Dependencias

```
uv sync
```

Isso cria um ambiente virtual isolado e instala todas as bibliotecas necessarias.

### 1.2 Configuracao Inicial

Antes de usar, configure dois arquivos:

Copie os arquivos de template:
```
cp .env.example .env
cp business_config.yaml.example business_config.yaml
cp business_bsc.yaml.example business_bsc.yaml
```
(No Windows, use `Copy-Item .env.example .env`)

Edite cada arquivo com suas credenciais e regras de negocio. Veja o guia detalhado em [configuracao.md](configuracao.md). Resuma as etapas de adaptação de configuração na skill `business-config` (`.opencode/skills/business-config`).

---

## 2. Sincronizacao do Banco de Dados

O banco local (`m_bird.db`) precisa ser sincronizado com a API da MessageBird antes de gerar relatorios.

### 2.1 Sincronizacao Incremental (Cron Job)

Puxa apenas conversas atualizadas nos ultimos 60 minutos (configuravel com `--lookback`). Ideal para rodar periodicamente:

```
uv run python main.py sync
```

### 2.2 Sincronizacao Diaria

Puxa conversas e mensagens do ultimo dia:

```
uv run python main.py sync --messages-days 1
```

### 2.3 Sincronizacao Mensal (Backfill)

Puxa **todas** as conversas e mensagens de um mes calendario especifico:

```
uv run python main.py sync --year 2026 --month 6
```

**Importante:** O sync-mensal ja cria contatos automaticamente junto com as conversas. Nao e necessario rodar um sync estrutural separado.

### 2.4 Sincronizacao de Periodo Personalizado

Para sincronizar um periodo especifico (ex:ultimos 30 dias com mensagens):

```
uv run python main.py sync --messages-days 30
```

### 2.5 Sincronizacao Estrutural Completa

Sincroniza todos os contatos, agentes e conversas (sem mensagens detalhadas):

```
uv run python main.py sync --full
```

### 2.6 Sincronizacao Completa com Mensagens

Sincroniza tudo incluindo todas as mensagens (pode demorar):

```
uv run python main.py sync --full-messages
```

### 2.7 Re-extracao de Avaliacoes (Backfill Surveys)

Re-extrai NPS e avaliacoes de conversas existentes no banco:

```
uv run python main.py sync --backfill-surveys
```

### 2.8 Flags Adicionais

| Flag | Descrição | Default |
|:-----|:----------|:--------|
| `--lookback N` | Minutos de retrocesso para sync incremental | 60 |
| `--full` | Sync estrutural completo | false |
| `--full-messages` | Sync completo incluindo todas mensagens | false |
| `--backfill-surveys` | Re-extrair NPS e avaliacoes | false |
| `--db-path` | Caminho para o banco SQLite | m_bird.db |

---

## 3. Geracao de Relatorios

### 3.1 Relatorio Mensal

Gera o relatorio para um mes calendario completo:

```
uv run python main.py report --year 2026 --month 6

# Apenas para um setor especifico
uv run python main.py report --year 2026 --month 6 --sector "Suporte Tecnico"
```

### 3.2 Relatorio de Periodo Personalizado

Gera relatorio para datas especificas:

```
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26

# Com filtro de setor
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26 --sector "Comercial"
```

### 3.3 Relatorio Anual

Consolida todo o ano em um unico dashboard com aba de "Evolucao Mensal":

```
uv run python main.py report --year 2026

# Filtrado por setor
uv run python main.py report --year 2026 --sector "Suporte Tecnico"
```

### 3.4 Relatorio Total do Sistema

Gera dashboard de **todo o historico** disponivel no banco:

```
uv run python main.py total

# Filtrado
uv run python main.py total --sector "Financeiro"
```

### 3.5 Relatorio de Qualidade dos Dados

Gera relatorio de integridade e qualidade dos dados no banco:

```
uv run python main.py quality
```

**Saidas geradas:**
- `reports/qualidade_dados/qualidade_dados.xlsx` — Metricas de integridade
- `reports/qualidade_dados/README.md` — Resumo da qualidade

**Metricas avaliadas:**
- Campos nulos ou ausentes
- Duplicatas
- Inconsistencias entre tabelas
- Cobertura de avaliacoes e NPS

---

## 4. Estrutura de Saida dos Relatorios

### Relatorio Mensal (`uv run python main.py report --year 2026 --month 6`)

```
reports/
└── 2026/
    └── 2026-06/
        ├── README.md                              # Resumo executivo
        ├── Dashboard_Executivo_GLOBAL_2026_06.xlsx # Dashboard consolidado
        ├── Suporte_Tecnico/
        │   ├── Dashboard_Executivo_Suporte_Tecnico_2026_06.xlsx
        │   └── auditoria/
        │       ├── auditoria_contatos.xlsx
        │       ├── auditoria_os.xlsx
        │       └── OS/
        │           └── OS_12345.pdf
        └── Comercial/
            └── ...
```

### Relatorio de Periodo Personalizado (`uv run python main.py report --from-date ... --to-date ...`)

```
reports/
└── 20260525_20260626/
    ├── Dashboard_Executivo_GLOBAL_20260525_20260626.xlsx
    ├── README.md
    └── ...
```

### Relatorio Anual (`uv run python main.py report --year 2026`)

```
reports/
└── 2026/
    ├── Dashboard_Executivo_ANUAL_2026.xlsx  # Inclui aba "Evolucao Mensal"
    ├── README.md
    └── ...
```

### Relatorio Total (`uv run python main.py total`)

```
reports/
└── total/
    ├── Dashboard_Executivo_TOTAL_SISTEMA.xlsx
    ├── README.md
    └── ...
```

### Relatorio de Qualidade (`uv run python main.py quality`)

```
reports/
└── qualidade_dados/
    ├── qualidade_dados.xlsx
    ├── README.md
    └── ...
```

---

## 5. Uso via CLI (Python)

Para controle fino, execute comandos diretamente:

```
uv run python main.py --help
```

---

## 6. Dicas

- **Cron Job Recomendado:** Execute `uv run python main.py sync` a cada hora e `uv run python main.py sync --messages-days 1` uma vez por dia.
- **Periodo Personalizado:** Use `uv run python main.py report --from-date ... --to-date ...` quando precisar de um corte de datas que nao segue mes calendario.
- **Filtro de Setor:** sempre passe `--sector "Nome Exato"` para gerar relatorios mais rapidos e direcionados.
- **Re-sync Seguro:** Todos os comandos de sincronizacao usam UPSERT, podendo ser executados multiplas vezes sem duplicar dados.

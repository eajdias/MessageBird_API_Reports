# Guia de Uso: Standalone Report & Sync Tool

Este guia explica como usar cada funcionalidade da ferramenta de sincronizacao e relatorios do MessageBird Omnichannel.

---

## 1. Instalacao e Configuracao

### 1.1 Instalando Dependencias

```bash
make install
```

Isso cria um ambiente virtual isolado e instala todas as bibliotecas necessarias.

### 1.2 Configuracao Inicial

Antes de usar, configure dois arquivos:

```bash
cp config/.env.example config/.env
cp config/business_config.json.example config/business_config.json
```

Edite cada arquivo com suas credenciais e regras de negocio. Veja o guia detalhado em [configuracao.md](configuracao.md).

---

## 2. Sincronizacao do Banco de Dados

O banco local (`m_bird.db`) precisa ser sincronizado com a API da MessageBird antes de gerar relatorios.

### 2.1 Sincronizacao Incremental (Cron Job)

Puxa apenas conversas atualizadas nos ultimos 60 minutos. Ideal para rodar periodicamente:

```bash
make sync
```

### 2.2 Sincronizacao Diaria

Puxa conversas e mensagens do ultimo dia:

```bash
make sync-daily
```

### 2.3 Sincronizacao Mensal (Backfill)

Puxa **todas** as conversas e mensagens de um mes calendario especifico:

```bash
# Exemplo: sincronizar junho de 2026
make sync-monthly YEAR=2026 MONTH=6
```

**Importante:** O sync-mensal ja cria contatos automaticamente junto com as conversas. Nao e necessario rodar um sync estrutural separado.

### 2.4 Sincronizacao de Periodo Personalizado

Para sincronizar um periodo especifico (ex:ultimos 30 dias com mensagens):

```bash
uv run python main.py sync --messages-days 30
```

---

## 3. Geracao de Relatorios

### 3.1 Relatorio Mensal

Gera o relatorio para um mes calendario completo:

```bash
# Relatorio de junho de 2026 para todos os setores
make report YEAR=2026 MONTH=6

# Apenas para um setor especifico
make report YEAR=2026 MONTH=6 SECTOR="Suporte Tecnico"
```

### 3.2 Relatorio de Periodo Personalizado

Gera relatorio para datas especificas:

```bash
# Periodo de 25/05 a 26/06
make report-dates FROM=2026-05-25 TO=2026-06-26

# Com filtro de setor
make report-dates FROM=2026-05-25 TO=2026-06-26 SECTOR="Comercial"
```

### 3.3 Relatorio Anual

Consolida todo o ano em um unico dashboard com aba de "Evolucao Mensal":

```bash
# Ano inteiro
make annual YEAR=2026

# Filtrado por setor
make annual YEAR=2026 SECTOR="Suporte Tecnico"
```

### 3.4 Relatorio Total do Sistema

Gera dashboard de **todo o historico** disponivel no banco:

```bash
# Todos os setores
make total

# Filtrado
make total SECTOR="Financeiro"
```

---

## 4. Estrutura de Saida dos Relatorios

### Relatorio Mensal (`make report YEAR=2026 MONTH=6`)

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

### Relatorio de Periodo Personalizado (`make report-dates FROM=... TO=...`)

```
reports/
└── 20260525_20260626/
    ├── Dashboard_Executivo_GLOBAL_20260525_20260626.xlsx
    ├── README.md
    └── ...
```

### Relatorio Anual (`make annual YEAR=2026`)

```
reports/
└── 2026/
    ├── Dashboard_Executivo_ANUAL_2026.xlsx  # Inclui aba "Evolucao Mensal"
    ├── README.md
    └── ...
```

### Relatorio Total (`make total`)

```
reports/
└── total/
    ├── Dashboard_Executivo_TOTAL_SISTEMA.xlsx
    ├── README.md
    └── ...
```

---

## 5. Uso via CLI (Python)

Para controle fino, execute comandos diretamente:

```bash
# Ver ajuda completa
uv run python main.py --help

# Sincronizacao
uv run python main.py sync --help
uv run python main.py sync --messages-days 30

# Relatorios
uv run python main.py report --help
uv run python main.py report --from-date 2026-05-25 --to-date 2026-06-26
uv run python main.py report --year 2026 --month 6 --sector "Suporte Tecnico"

# Total
uv run python main.py total
```

---

## 6. Dicas

- **Cron Job Recomendado:** Execute `make sync` a cada hora e `make sync-daily` uma vez por dia.
- **Periodo Personalizado:** Use `make report-dates` quando precisar de um corte de datas que nao segue mes calendario.
- **Filtro de Setor:** sempre passe `SECTOR="Nome Exato"` para gerar relatorios mais rapidos e direcionados.
- **Re-sync Seguro:** Todos os comandos de sincronizacao usam UPSERT, podendo ser executados multiplas vezes sem duplicar dados.

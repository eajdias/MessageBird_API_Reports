# Guia de Uso: Standalone Report & Sync Tool

Bem-vindo ao gerador de relatórios independente do MessageBird Omnichannel. Este projeto foi arquitetado para rodar de forma totalmente isolada (sem depender do servidor MCP) e é responsável por duas missões principais:

1. **Sincronizar dados** brutos (conversas, mensagens, contatos e agentes) da API do MessageBird para um banco local SQLite de altíssima performance.
2. **Gerar relatórios** mensais ou anuais super detalhados, quebrando a performance por agente, departamento, além de gerar planilhas de auditoria e Ordens de Serviço (OS) em formato PDF.

---

## 🛠️ 1. Instalação e Configuração

O projeto utiliza `uv` como gerenciador de dependências e executor. Tenha o `uv` instalado — todo o resto (incluindo o Python adequado) é gerenciado automaticamente.

### 1.1 Instalando Dependências

Para instalar as bibliotecas necessárias (como `rich` para UI do terminal, `aiosqlite` para banco, `fpdf2` para PDF, etc) em um ambiente virtual isolado, rode:

```bash
make install
```

### 1.2 Variáveis de Ambiente e Configuração

Este projeto se baseia em dois arquivos principais localizados na subpasta `config/`:

1. **`config/.env`**: Cópia do template [`config/.env.example`](../config/.env.example). Precisa conter suas chaves de API da MessageBird (`MESSAGEBIRD_API_KEY_LIVE`, `MESSAGEBIRD_WORKSPACE_ID_LIVE`, etc).
2. **`config/business_config.json`**: Mapeia as regras de negócios da sua empresa, definindo quais IDs numéricos correspondem a quais departamentos e em quais "Grupos" os agentes devem ser divididos na hora de gerar o relatório.

> **Importante:** Leia o guia detalhado em **[docs/configuracao.md](configuracao.md)** para aprender a preencher corretamente estes dois arquivos.

3. **`m_bird.db`**: O banco de dados SQLite principal será gerado automaticamente na raiz do projeto assim que a primeira sincronização for rodada.

---

## 🔄 2. Como Sincronizar o Banco de Dados

Para gerar relatórios reais, o seu banco local (`m_bird.db`) precisa estar atualizado com a nuvem. Oferecemos 3 níveis de profundidade na extração de dados:

### A) Sincronização Incremental (Recomendado)
Puxa apenas as conversas recentes (padrão: últimos 60 minutos). Excelente para rodar via *Cron Job* a cada hora.
```bash
make sync
```

### B) Sincronização Diária (Cron Job Diário)
Para garantir que as mensagens de ontem estão perfeitamente espelhadas, sem precisar varrer anos de histórico:
```bash
make sync-daily
```

### C) Sincronização Mensal (Backfill)
Caso você precise puxar **todas** as mensagens e metadados referentes apenas a um mês específico (muito útil caso algum relatório tenha dado diferença):
```bash
make sync-monthly YEAR=2026 MONTH=4
```

### D) Sincronização Completa de Estrutura
Sincroniza todos os Contatos, Agentes e Metadados das Conversas. Útil se você criou novas tags ou alterou status em massa no painel. *(Não faz o download de mensagens).*
```bash
make sync-full
```

### E) Sincronização Total (Pesado)
Além da estrutura, varre o histórico iterando sobre todas as mensagens de todas as conversas. Demora bastante, mas garante um banco local 100% fiel à nuvem.
```bash
make sync-messages
```

---

## 📊 3. Como Gerar Relatórios

A geração de relatórios lê os dados do SQLite e constrói a estrutura de pastas e planilhas de Excel. 

### A) Relatório Mensal Global
Gera o relatório do mês especificado para **todos os setores** cadastrados no `business_config.json`.
```bash
# Gera o relatório de Janeiro de 2025
make report YEAR=2025 MONTH=1
```

### B) Relatório Mensal Específico por Setor (Ágil)
Se você precisa enviar com urgência o relatório apenas para a gerência de Suporte, pode filtrar a extração, economizando tempo de processamento.
```bash
make report YEAR=2026 MONTH=1 SECTOR="Suporte Técnico"
```
*(Nota: O nome do Setor deve ser idêntico ao grupo cadastrado em `business_config.json` ou `constants.py`).*

### C) Relatório Anual Consolidado
Para fechamento do ano (Dashboard global somando todos os meses de Janeiro a Dezembro, com aba "Evolução Mensal" contendo gráficos de tendência de Chats, NPS e ART).
```bash
# Gera o relatório anual de 2024
make annual YEAR=2024

# Relatório anual filtrado por setor
make annual YEAR=2024 SECTOR="Suporte Técnico"
```
A estrutura gerada é idêntica à mensal, mas o dashboard principal recebe o nome `Dashboard_Executivo_ANUAL_2024.xlsx` e inclui uma aba extra `Evolução Mensal` com gráficos de linha mês a mês.

### D) Relatório Total do Sistema
Gera o dashboard consolidado de **todo o histórico disponível no banco** (sem filtro de data).
```bash
make total

# Total do sistema filtrado por setor
make total SECTOR="Comercial"
```
O dashboard principal é salvo em `reports/total/Dashboard_Executivo_TOTAL_SISTEMA.xlsx` com a aba "Evolução Mensal" contendo todos os meses do cache disponível.

---

## 📁 4. O que é gerado na pasta `reports/`?

### A) Relatório Mensal (`make report YEAR=2024 MONTH=2`)

```text
reports/
└── 2024/
    └── 2024-02/
        ├── README.md                              <-- Resumo executivo em Markdown
        ├── Dashboard_Executivo_GLOBAL_2024_02.xlsx <-- Dashboard consolidado (Todos os agentes)
        ├── Comercial/                             <-- Pasta individualizada do Setor
        │   ├── Dashboard_Executivo_Comercial_2024_02.xlsx
        │   └── auditoria/
        │       ├── auditoria_contatos.xlsx        <-- Lista de quem chamou no período
        │       ├── auditoria_os.xlsx              <-- Planilha bruta de Ordens de Serviço
        │       └── OS/
        │           ├── OS_10523.pdf               <-- Formulário final em PDF para a OS 10523
        │           └── OS_10540.pdf
        └── Suporte_Técnico/
            ├── Dashboard_Executivo_Suporte_Técnico_2024_02.xlsx
            └── auditoria/
                ├── auditoria_contatos.xlsx
                └── ...
```

### B) Relatório Anual (`make annual YEAR=2024`)

```text
reports/
└── 2024/
    ├── README.md                                  <-- Resumo executivo anual
    ├── Dashboard_Executivo_ANUAL_2024.xlsx          <-- Dashboard anual (5 abas, incl. Evolução Mensal)
    ├── Comercial/
    │   ├── Dashboard_Anual_Comercial_2024.xlsx
    │   └── auditoria/
    │       ├── auditoria_contatos.xlsx
    │       ├── auditoria_os.xlsx
    │       └── OS/
    │           └── *.pdf
    └── Suporte_Técnico/
        └── ...
```

### C) Relatório Total do Sistema (`make total`)

```text
reports/
└── total/
    ├── README.md                                  <-- Resumo executivo total
    ├── Dashboard_Executivo_TOTAL_SISTEMA.xlsx       <-- Dashboard total (5 abas, todo o histórico)
    ├── Comercial/
    │   ├── Dashboard_Total_Comercial.xlsx
    │   └── auditoria/
    └── Suporte_Técnico/
        └── ...
```

---

## 🧑‍💻 5. Uso Avançado via Script (Python CLI)

Se o `Makefile` não cobrir sua necessidade de automação, chame o script principal diretamente para ter controle fino sobre os parâmetros:

```bash
# Ative o virtualenv ou use uv run
uv run python main.py --help

# Ajuda dos parâmetros de sincronização
uv run python main.py sync --help

# Ajuda dos parâmetros de relatório total
uv run python main.py total --help

# Exemplo: Fazer backfill de mensagens de uma janela específica de tempo em um DB de teste
uv run python main.py sync --full-messages --year 2024 --month 1 --db-path ./test.db

# Gerar relatório total diretamente via CLI
uv run python main.py total --db-path m_bird.db --config-path config/business_config.json
```

> Todos os comandos do `Makefile` usam `uv run python` — não há dependência de caminhos fixos de Python ou virtualenv.
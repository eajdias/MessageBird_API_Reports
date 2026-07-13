# Arquitetura e Padroes de Desenvolvimento

Este documento estabelece as diretrizes para desenvolvimento e manutencao do projeto, seguindo Clean Architecture e padroes SOLID.

---

## 1. Principios Fundamentais

| Principo | Aplicacao no Projeto |
|:---------|:---------------------|
| **Clean Architecture** | Separacao estrita entre regras de negocio (Domain/Application) e detalhes tecnicos (Infrastructure/Presentation) |
| **SOLID** | SRP: classes com responsabilidade unica. OCP: aberto para extensao, fechado para modificacao. DIP: dependencias via interfaces |
| **DRY** | Liguas de calculo e conversao de datas em um unico local no Dominio |
| **KISS** | Abstracoes minimas, solucoes legiveis e diretas |

---

## 2. Estrutura de Camadas

As dependencias apontam sempre para o centro (Dominio).

### 2.1 Camada de Dominio (`domain/`)

Responsavel por toda a logica de negocio pura, sem dependencias externas.

```
domain/
├── constants.py          # SLAs, headers, mapas de departamento
├── logic.py              # Funcoes de tempo e conversao
├── entities/
│   └── report_data.py    # Dataclasses (RawConversationData, etc.)
├── strategies/
│   └── metrics_strategy.py  # Interface para calculos de metricas
├── metrics/
│   ├── frt.py            # First Response Time
│   ├── art.py            # Average Response Time
│   └── duration.py       # Duracao do atendimento
└── services/
    └── metrics_calculator.py  # NPS, SLA, medias
```

**Regra:** ZERO dependencias externas. Apenas Python standard library.

### 2.2 Camada de Aplicacao (`application/`)

Orquestracao de fluxos e transformacao de dados.

```
application/
├── interfaces/
│   ├── repository.py     # ABC para repositorios
│   └── exporter.py       # ABC para exportadores
├── use_cases/
│   ├── sync_database.py  # Sincronizacao com API
│   └── generate_report.py # Geracao de relatorios
└── services/
    ├── report_aggregator.py  # Agregacao de metricas
    ├── sub_aggregators.py    # Agregadores temporais, por topico
    └── auditoria_*.py        # Servicos de auditoria
```

**Regra:** Depende apenas do Dominio e das Interfaces.

### 2.3 Camada de Infraestrutura (`infrastructure/`)

Implementacoes tecnicas e integracao com APIs externas.

```
infrastructure/
├── api/
│   ├── client.py         # Cliente HTTP (httpx)
│   ├── config.py         # Configuracoes da API
│   └── sync.py           # Sincronizacao com MessageBird
├── database/
│   ├── init_db.py        # Schema SQLite
│   ├── connection.py     # Conexao read-only
│   ├── sync_connection.py # Conexao write (WAL)
│   ├── sqlite_repository.py # Implementacao do repositorio
│   └── queries.py        # Consultas SQL
├── exporters/
│   ├── excel_exporter.py # Exportacao Excel (xlsxwriter)
│   ├── pdf_exporter.py   # Exportacao PDF (fpdf2)
│   └── markdown_exporter.py # Exportacao README.md
└── config_loader.py      # Leitura de business_config.yaml e business_bsc.yaml
```

**Regra:** Onde frameworks e bibliotecas externas vivem. Nenhuma logica de negocio deve vazar para ca.

### 2.4 Camada de Apresentacao (`presentation/`)

```
presentation/
└── terminal.py           # Interface CLI (rich)
```

---

## 3. Padrões de Implementacao

### Tratamento de Datas e Timezones

1. **UTC no Banco:** Todos os dados armazenados em UTC
2. **Local no Relatorio:** Conversao para fuso local (UTC-3) apenas na exibicao final, em `domain/logic.py`

### Evitando God Classes

1. **Dividir:** Se uma classe de servico crescer demais, fragmentar em estrategias (ex: `HeatmapStrategy`, `SLAStrategy`)
2. **Injecao de Dependencia:** Sempre passar dependencias via construtor

### Exportadores

1. **DTOs:** Usar objetos simples (`DashboardDTO`) para transferir dados entre Aplicacao e Exportadores
2. **Formatadores Isolados:** Logica de formatacao visual fica dentro do exporter, nunca no aggregator

---

## 4. Checklist para Novos Recursos

- [ ] Logica de calculo esta em `domain/services/`?
- [ ] Novo metodo no repositorio retorna dados crus ou entidades de dominio?
- [ ] O Use Case esta orquestrando (não calculando)?
- [ ] Existem testes unitarios para a nova logica?
- [ ] DRY foi respeitado?

---

## 5. Comandos de Desenvolvimento

```
# Instalar dependencias
uv sync

# Rodar testes
uv run pytest tests/

# Sincronizar dados de teste
uv run python main.py sync --year 2026 --month 6 --db-path test.db

# Gerar relatorio de teste
uv run python main.py report --year 2026 --month 6 --db-path test.db
```

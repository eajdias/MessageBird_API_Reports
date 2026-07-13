# Configuracao

Guia completo para configurar a ferramenta de relatorios MessageBird.

---

## 1. Arquivo `.env`

Copie o arquivo de template e preencha com suas credenciais:
```
cp .env.example .env
```
(No Windows, use `Copy-Item .env.example .env`)

### Variaveis Obrigatorias

| Variavel | Descricao | Exemplo |
|:---------|:----------|:--------|
| `MESSAGEBIRD_API_KEY_LIVE` | Chave de API da MessageBird | `live_xxxxx` |
| `MESSAGEBIRD_WORKSPACE_ID_LIVE` | ID do workspace | `workspace-abc` |

### Variaveis Opcionais

| Variavel | Padrao | Descricao |
|:---------|:-------|:----------|
| `MESSAGEBIRD_DB_FILENAME` | `m_bird.db` | Nome do arquivo do banco |
| `MESSAGEBIRD_HTTP_TIMEOUT` | `30.0` | Timeout das requisicoes (segundos) |
| `MESSAGEBIRD_TIMEZONE_OFFSET` | `-3` | Offset do fuso horario (UTC). Ajuste para o fuso da sua empresa |

---

## 2. Arquivo `business_config.yaml`

E o "coracao" da configuracao de relatorios. Define como dados brutos se tornam informacoes compreensiveis.

### Estrutura Completa

```json
{
    "DEPT_MAP": {
        "1": "Suporte Tecnico",
        "2": "Comercial",
        "3": "Financeiro",
        "4": "Ouvidoria",
        "5": "Nova Instalacao | Migracao"
    },
    "REASON_MAP": {
        "1": {
            "1": "Motivo A",
            "2": "Motivo B"
        },
        "2": {
            "1": "Motivo C"
        }
    },
    "OCCURRENCE_MAP": {
        "2": {
            "1": {
                "1": "Ocorrencia X",
                "2": "Ocorrencia Y"
            }
        }
    },
    "LANG_MAP": {
        "1": "Portugues",
        "2": "English",
        "3": "Espanol"
    },
    "DEPT_ROUTING": {
        "Ouvidoria": "Ouvidoria",
        "Nova Instalação | Migração": "CS | Instalação | Migração | Ouvidoria"
    },
    "AGENTS": {
        "bird_id_do_agente": {
            "name": "Nome do Agente",
            "group": "Nome do Grupo"
        }
    }
}
```

### Descricao de Cada Campo

#### `DEPT_MAP`
Mapeia IDs de departamentos para nomes. Usado na triagem automatica (bot).

#### `REASON_MAP`
Mapeia motivos de contato por departamento. Estrutura aninhada: `departamento -> motivo_id -> nome`.

#### `OCCURRENCE_MAP`
Mapeia ocorrencias por departamento e motivo. Estrutura: `departamento -> motivo -> ocorrencia_id -> nome`.

#### `LANG_MAP`
Mapeia idiomas para nomes.

#### `DEPT_ROUTING` (opcional)
Redireciona conversas de um departamento para um grupo de relatório específico, independente do grupo do agente que atendeu. A chave é o nome do departamento (conforme `DEPT_MAP`), o valor é o nome do grupo de destino.

**Exemplo**: uma conversa com departamento "Ouvidoria" atendida por um agente do "Suporte Técnico" aparecerá na pasta "Ouvidoria" do relatório.

Se um departamento não estiver em `DEPT_ROUTING`, o comportamento padrão (grupo do agente) é mantido.

#### `AGENTS`
Mapeia agentes MessageBird para nomes e grupos. Cada entrada tem:
- **Chave**: ID do agente no MessageBird (`bird_id`)
- **name**: Nome exibido nos relatorios
- **group**: Grupo organizacional (define a pasta de saida)

### Como Configurar os Grupos de Agentes

O campo `group` em `AGENTS` define como os agentes sao agrupados nos relatorios. Agentes com o mesmo `group` aparecem na mesma pasta e dashboard.

Exemplo:
```json
"AGENTS": {
    "abc-123": { "name": "Joao Silva", "group": "Suporte Tecnico" },
    "def-456": { "name": "Maria Santos", "group": "Suporte Tecnico" },
    "ghi-789": { "name": "Pedro Costa", "group": "Comercial" }
}
```

Isso gera:
```
reports/
├── Suporte_Tecnico/
│   └── Dashboard_Executivo_Suporte_Tecnico.xlsx
└── Comercial/
    └── Dashboard_Executivo_Comercial.xlsx
```

---

## 3. Arquivo `business_bsc.yaml` (NPS, BSC e thresholds)

Centraliza os parametros de negocio que variam por empresa e devem ser ajustados sem tocar no codigo:

- **`KPI_CONFIG`**: definicao das metricas do Balanced Scorecard (metas, pesos, tipo de calculo e faixas). Cada empresa define seus proprios KPIs, metas e pesos.
- **`NPS_CONFIG`**: cortes do NPS — `promoter_min` (nota minima para promotor) e `passive_min` (minima para neutro/passivo). Detratores sao as notas abaixo de `passive_min`.
- **`METRIC_THRESHOLDS`**: limites de SLA/ART/duracao usados nos calculos (`sla_frt_minutes`, `sla_frt_seconds`, `max_art_minutes`, `max_duration_minutes`).

Exemplo:

```json
{
  "KPI_CONFIG": { "Suporte Tecnico": { "t1": [ ... ], "t2": [ ... ], "penalidades_setoriais": [ ... ] } },
  "NPS_CONFIG": { "promoter_min": 9, "passive_min": 7 },
  "METRIC_THRESHOLDS": { "sla_frt_minutes": 60, "sla_frt_seconds": 3600, "max_art_minutes": 480, "max_duration_minutes": 630 }
}
```

> **Nota:** Para reutilizar o projeto em outra empresa, basta adaptar `business_config.yaml` (mapas de departamento/motivos/agentes) e `business_bsc.yaml` (KPIs, metas e cortes). O fuso horario e credenciais ficam em `.env`.

---

## 4. Como Atualizar a Configuracao

1. Edite `business_config.yaml` e/ou `business_bsc.yaml`
2. Nao e necessario reiniciar nada
3. As mudancas refletem na proxima geracao de relatorio

> **Dica:** Agentes novos ja sao automaticamente criados no banco durante a sincronizacao. Basta adicionar o `bird_id` e `group` no `business_config.yaml` para que aparecam no relatorio correto.

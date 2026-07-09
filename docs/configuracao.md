# Configuracao

Guia completo para configurar a ferramenta de relatorios MessageBird.

---

## 1. Arquivo `.env`

Copie o arquivo de template e preencha com suas credenciais:
```
cp config/.env.example config/.env
```
(No Windows, use `Copy-Item config/.env.example config/.env`)

### Variaveis Obrigatorias

| Variavel | Descricao | Exemplo |
|:---------|:----------|:--------|
| `MESSAGEBIRD_API_KEY_LIVE` | Chave de API da MessageBird | `live_xxxxx` |
| `MESSAGEBIRD_WORKSPACE_ID_LIVE` | ID do workspace | `workspace-abc` |

### Variaveis Opcionais

| Variavel | Padrao | Descricao |
|:---------|:-------|:----------|
| `MESSAGEBIRD_ENV` | `live` | Ambiente (`live`, `test`, `production`) |
| `MESSAGEBIRD_DB_FILENAME` | `m_bird.db` | Nome do arquivo do banco |
| `MESSAGEBIRD_RESULT_LIMIT` | `20` | Itens por pagina na API |
| `MESSAGEBIRD_HTTP_TIMEOUT` | `30.0` | Timeout das requisicoes (segundos) |
| `MESSAGEBIRD_TIMEZONE_OFFSET` | `-3` | Offset do fuso horario (UTC) |
| `MESSAGEBIRD_LOG_LEVEL` | `INFO` | Nivel de log |

### Configuracao de SLA

| Variavel | Padrao | Descricao |
|:---------|:-------|:----------|
| `MESSAGEBIRD_SLA_FR_SECONDS` | `300` | Tempo maximo para primeira resposta (segundos) |
| `MESSAGEBIRD_SLA_RES_HOURS` | `24` | Tempo maximo para resolucao (horas) |
| `MESSAGEBIRD_SLA_MAX_MSGS` | `50` | Limite maximo de mensagens por conversa |

---

## 2. Arquivo `business_config.json`

E o "coracao" da configuracao de relatorios. Define como dados brutos se tornam informacoes compreensiveis.

### Estrutura Completa

```json
{
    "SYSTEM_MAP": {
        "1": "NOME_DO_SISTEMA_A",
        "2": "NOME_DO_SISTEMA_B"
    },
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
    "AGENTS": {
        "bird_id_do_agente": {
            "name": "Nome do Agente",
            "group": "Nome do Grupo"
        }
    }
}
```

### Descricao de Cada Campo

#### `SYSTEM_MAP`
Mapeia IDs de sistemas/softwares para nomes legiveis.

#### `DEPT_MAP`
Mapeia IDs de departamentos para nomes. Usado na triagem automatica (bot).

#### `REASON_MAP`
Mapeia motivos de contato por departamento. Estrutura aninhada: `departamento -> motivo_id -> nome`.

#### `OCCURRENCE_MAP`
Mapeia ocorrencias por departamento e motivo. Estrutura: `departamento -> motivo -> ocorrencia_id -> nome`.

#### `LANG_MAP`
Mapeia idiomas para nomes.

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

## 3. Como Atualizar a Configuracao

1. Edite `config/business_config.json`
2. Nao e necessario reiniciar nada
3. As mudancas refletem na proxima geracao de relatorio

> **Dica:** Agentes novos ja sao automaticamente criados no banco durante a sincronizacao. Basta adicionar o `bird_id` e `group` no `business_config.json` para que aparecam no relatorio correto.

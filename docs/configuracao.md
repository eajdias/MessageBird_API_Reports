# Configuração

Guia completo para configurar a ferramenta de relatórios MessageBird e adaptá-la a qualquer empresa.

---

## 1. Arquivo `.env`

Copie o arquivo de template e preencha com suas credenciais:

```bash
cp .env.example .env
```

(No Windows, use `Copy-Item .env.example .env`)

### Variáveis Obrigatórias

| Variável | Descrição | Exemplo |
|:---------|:----------|:--------|
| `MESSAGEBIRD_API_KEY_LIVE` | Chave de API da MessageBird | `live_xxxxx` |
| `MESSAGEBIRD_WORKSPACE_ID_LIVE` | ID do workspace | `workspace-abc` |

> As chaves de ambiente de teste (`_TEST`) também são suportadas. As de produção foram removidas — use apenas live/test.

### Variáveis Opcionais

| Variável | Padrão | Descrição |
|:---------|:-------|:----------|
| `MESSAGEBIRD_DB_FILENAME` | `m_bird.db` | Nome do arquivo do banco |
| `MESSAGEBIRD_HTTP_TIMEOUT` | `30.0` | Timeout das requisições (segundos) |
| `MESSAGEBIRD_TIMEZONE_OFFSET` | `-3` | Offset do fuso horário (UTC). **Ajuste para o fuso da sua empresa** (ex.: `-3` Brasília, `0` Lisboa, `1` Berlim) |
| `MESSAGEBIRD_BASE_URL_*` | URLs oficiais da Bird | Normalmente não precisam mudar |
| `MESSAGEBIRD_PHRASE_TRIAGEM_HEADER` / `MESSAGEBIRD_PHRASE_TICKET_HEADER` | textos padrão | Frases usadas para fazer parsing de triagem nas mensagens |
| `MESSAGEBIRD_SOFTWARE_NAMES` | `SOFTWARE_A,SOFTWARE_B` | Nomes de software para auto-tagging |

> Não há mais variáveis de SLA, canal (WhatsApp/Telegram) ou agentes manuais no `.env` — essas foram removidas por não serem utilizadas.

---

## 2. Arquivo `business_config.yaml`

É o "coração" da configuração operacional. Define como os dados brutos da API viram informações legíveis.

```yaml
# ID do departamento (na API) -> nome exibido no relatório
DEPT_MAP:
  1: "Suporte Tecnico"
  2: "Comercial"
  3: "Financeiro"
  4: "Ouvidoria"
  5: "Nova Instalacao | Migracao"

# Motivos de contato por departamento: departamento -> motivo_id -> nome
REASON_MAP:
  1:
    1: "Problemas tecnicos"
    2: "Agendamentos"
    3: "Manuais de uso (PDF ou videos)"
  2:
    1: "Falar com um consultor comercial"
    2: "Agendar uma demonstracao"

# Ocorrencias por departamento e motivo: departamento -> motivo -> ocorrencia_id -> nome
OCCURRENCE_MAP:
  1:
    1:
      1: "Ocorrencia 1"
      2: "Ocorrencia 2"

# ID do idioma (na API) -> nome exibido
LANG_MAP:
  1: "Portugues"
  2: "English"
  3: "Espanol"

# Roteamento: nome do departamento detectado -> grupo de atendimento no relatório
DEPT_ROUTING:
  "Ouvidoria": "Ouvidoria"
  "Suporte Tecnico": "Suporte Tecnico"
  "Comercial": "Comercial"
  "Financeiro": "Financeiro"
  "Nova Instalacao | Migracao": "CS | Instalacao | Migracao"

# Agentes: bird_id (string) -> { name, group }
AGENTS:
  bird_id_do_agente_1: { name: "Nome do Agente 1", group: "Suporte Tecnico" }
  bird_id_do_agente_2: { name: "Nome do Agente 2", group: "Comercial" }
```

### Descrição de Cada Campo

#### `DEPT_MAP`
Mapeia IDs de departamentos para nomes. Usado na triagem automática (bot).

#### `REASON_MAP`
Mapeia motivos de contato por departamento. Estrutura aninhada: `departamento -> motivo_id -> nome`.

#### `OCCURRENCE_MAP`
Mapeia ocorrências por departamento e motivo. Estrutura: `departamento -> motivo -> ocorrencia_id -> nome`.

#### `LANG_MAP`
Mapeia idiomas para nomes.

#### `DEPT_ROUTING` (opcional)
Redireciona conversas de um departamento para um grupo de relatório específico, independente do grupo do agente que atendeu. A chave é o nome do departamento (conforme `DEPT_MAP`); o valor é o nome do grupo de destino.

**Exemplo**: uma conversa do departamento "Ouvidoria" atendida por um agente do "Suporte Técnico" aparecerá na pasta "Ouvidoria". Se um departamento não estiver em `DEPT_ROUTING`, mantém-se o grupo do agente.

#### `AGENTS`
Mapeia agentes MessageBird para nomes e grupos:
- **Chave**: ID do agente no MessageBird (`bird_id`)
- **name**: nome exibido nos relatórios
- **group**: grupo organizacional (define a pasta de saída)

Agentes novos são criados automaticamente no banco durante a sincronização; basta adicionar o `bird_id` e o `group` para que apareçam no relatório certo.

---

## 3. Arquivo `business_bsc.yaml` (NPS, BSC e thresholds)

Centraliza os parâmetros de negócio que variam por empresa e devem ser ajustados **sem tocar no código**:

- **`KPI_CONFIG`**: definição das métricas do Balanced Scorecard (metas, pesos, tipo de cálculo e faixas). Cada empresa define seus próprios KPIs.
- **`NPS_CONFIG`**: cortes do NPS — `promoter_min` (nota mínima para promotor) e `passive_min` (mínima para neutro/passivo). **Detratores** são as notas abaixo de `passive_min`.
- **`METRIC_THRESHOLDS`**: limites usados nos cálculos (`sla_frt_minutes`, `sla_frt_seconds`, `max_art_minutes`, `max_duration_minutes`).

```yaml
KPI_CONFIG:
  "Suporte Tecnico":
    t1:
      - name: "Elogios de atendimento / Feedback"
        description: "Notas 4 e 5 são consideradas Feedback positivo."
        meta: ">40%"
        peso: 30
        tipo: "escalonado_percentual"
        niveis:
          - { min: 40, pts: 30, extra_per_unit: 0.75 }
          - { min: 35, pts: 15 }
          - { min: 30, pts: 10 }
        cap: 60
      - name: "NPS (Net Promoter Score)"
        description: "NPS individual do agente."
        meta: ">=70/63/50"
        peso: 30
        tipo: "escalonado_nps"
        niveis:
          - { min: 70, pts: 30 }
          - { min: 63, pts: 15 }
          - { min: 50, pts: 5 }
    t2:
      - { name: "Updates",      meta: 1, peso: 1, tipo: "proporcional" }
      - { name: "Treinamentos", meta: 1, peso: 1, tipo: "proporcional" }
    penalidades_setoriais:
      - name: "Ligações Perdidas (Setor)"
        description: "Penalidade setorial aplicada a todo o grupo."
        meta: 0
        peso: -2
        tipo: "penalidade"

NPS_CONFIG:
  promoter_min: 9
  passive_min: 7

METRIC_THRESHOLDS:
  sla_frt_minutes: 60
  sla_frt_seconds: 3600
  max_art_minutes: 480
  max_duration_minutes: 630
```

> **Dica:** a skill `business-config` (`.opencode/skills/business-config`) documenta passo a passo como adaptar esses arquivos para uma nova empresa.

---

## 4. Como Atualizar a Configuração

1. Edite `business_config.yaml` e/ou `business_bsc.yaml` (e `.env` se mudar credenciais/fuso).
2. Não é necessário reiniciar nada.
3. As mudanças refletem na próxima geração de relatório.

> **Segurança:** os arquivos reais (`.env`, `business_config.yaml`, `business_bsc.yaml`) são ignorados pelo Git. Apenas os `.example` são versionados — nunca comite dados reais.

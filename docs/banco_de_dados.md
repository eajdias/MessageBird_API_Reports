# Banco de Dados - Schema Completo

Este documento descreve o schema completo do banco SQLite (`m_bird.db`) utilizado pelo projeto.

---

## 1. Visão Geral

| Tabela | Registros* | Descrição |
|:-------|:-----------|:----------|
| `contacts` | ~646 | Contatos (clientes) |
| `agents` | ~12 | Agentes de atendimento |
| `conversations` | ~1.157 | Conversas/chats |
| `messages` | ~57.751 | Mensagens das conversas |
| `sync` | Variável | Histórico de sincronizações |
| `sync_errors` | Variável | Erros durante sincronização |

*Valores aproximados podem variar conforme dados sincronizados.

---

## 2. Tabelas Detalhadas

### 2.1 `contacts`

Armazena os contatos (clientes) que interagiram com a empresa.

```sql
CREATE TABLE contacts (
    cnts_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnts_name TEXT,
    cnts_phone TEXT,
    cnts_bird TEXT UNIQUE NOT NULL,
    cnts_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    cnts_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    cnts_custom1 TEXT,
    cnts_custom2 TEXT,
    cnts_custom3 TEXT,
    cnts_custom4 TEXT
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `cnts_id` | INTEGER | ID interno (autoincremento) |
| `cnts_name` | TEXT | Nome do contato |
| `cnts_phone` | TEXT | Telefone (formato E.164) |
| `cnts_bird` | TEXT | ID único no MessageBird (chave externa) |
| `cnts_created` | DATETIME | Data de criação |
| `cnts_updated` | DATETIME | Última atualização |
| `cnts_custom1-4` | TEXT | Campos customizados (reservados) |

**Índices:**
- `idx_contacts_bird` em `cnts_bird`
- `idx_contacts_phone` em `cnts_phone`

---

### 2.2 `agents`

Armazena os agentes de atendimento.

```sql
CREATE TABLE agents (
    agnt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    agnt_name TEXT,
    agnt_bird TEXT UNIQUE NOT NULL,
    agnt_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    agnt_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `agnt_id` | INTEGER | ID interno (autoincremento) |
| `agnt_name` | TEXT | Nome do agente |
| `agnt_bird` | TEXT | ID único no MessageBird (chave externa) |
| `agnt_created` | DATETIME | Data de criação |
| `agnt_updated` | DATETIME | Última atualização |

**Índices:**
- `idx_agents_bird` em `agnt_bird`

---

### 2.3 `conversations`

Armazena as conversas/chats entre clientes e agentes.

```sql
CREATE TABLE conversations (
    cnvs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cnvs_msgcount INTEGER DEFAULT 0,
    cnvs_cnts INTEGER,
    cnvs_agnt INTEGER,
    cnvs_status TEXT,
    cnvs_channel TEXT,
    cnvs_bird TEXT UNIQUE NOT NULL,
    cnvs_created DATETIME,
    cnvs_updated DATETIME,
    cnvs_last DATETIME,
    cnvs_lang INTEGER,
    cnvs_software TEXT,
    cnvs_tax_id TEXT,
    cnvs_dept INTEGER,
    cnvs_rating_agent INTEGER,
    cnvs_rating_nps INTEGER,
    cnvs_sentiment TEXT,
    cnvs_category TEXT,
    cnvs_reopened_count INTEGER DEFAULT 0,
    cnvs_contact_reason INTEGER,
    cnvs_occurrence INTEGER,
    cnvs_description TEXT,
    FOREIGN KEY (cnvs_cnts) REFERENCES contacts(cnts_id),
    FOREIGN KEY (cnvs_agnt) REFERENCES agents(agnt_id)
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `cnvs_id` | INTEGER | ID interno (autoincremento) |
| `cnvs_msgcount` | INTEGER | Número de mensagens |
| `cnvs_cnts` | INTEGER | FK para `contacts.cnts_id` |
| `cnvs_agnt` | INTEGER | FK para `agents.agnt_id` |
| `cnvs_status` | TEXT | Status (active/archived) |
| `cnvs_channel` | TEXT | UUID do canal |
| `cnvs_bird` | TEXT | ID único no MessageBird (chave externa) |
| `cnvs_created` | DATETIME | Data de criação |
| `cnvs_updated` | DATETIME | Última atualização |
| `cnvs_last` | DATETIME | Última mensagem |
| `cnvs_lang` | INTEGER | ID do idioma |
| `cnvs_software` | TEXT | Software associado |
| `cnvs_tax_id` | TEXT | CPF/CNPJ do cliente |
| `cnvs_dept` | INTEGER | ID do departamento |
| `cnvs_rating_agent` | INTEGER | Nota do agente (1-5) |
| `cnvs_rating_nps` | INTEGER | Nota NPS (0-10) |
| `cnvs_sentiment` | TEXT | Sentimento (reservado) |
| `cnvs_category` | TEXT | Categoria (reservado) |
| `cnvs_reopened_count` | INTEGER | Contador de reaberturas |
| `cnvs_contact_reason` | INTEGER | Motivo do contato |
| `cnvs_occurrence` | INTEGER | Ocorrência |
| `cnvs_description` | TEXT | Descrição/triagem |

**Índices:**
- `idx_conversations_bird` em `cnvs_bird`
- `idx_conversations_status` em `cnvs_status`
- `idx_conversations_created` em `cnvs_created`
- `idx_conversations_updated` em `cnvs_updated`

---

### 2.4 `messages`

Armazena as mensagens de cada conversa.

```sql
CREATE TABLE messages (
    msgs_id INTEGER PRIMARY KEY AUTOINCREMENT,
    msgs_cnvs INTEGER NOT NULL,
    msgs_agnt INTEGER,
    msgs_direction TEXT,
    msgs_status TEXT,
    msgs_type TEXT,
    msgs_content TEXT,
    msgs_bird TEXT UNIQUE NOT NULL,
    msgs_created DATETIME,
    msgs_updated DATETIME,
    FOREIGN KEY (msgs_cnvs) REFERENCES conversations(cnvs_id),
    FOREIGN KEY (msgs_agnt) REFERENCES agents(agnt_id)
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `msgs_id` | INTEGER | ID interno (autoincremento) |
| `msgs_cnvs` | INTEGER | FK para `conversations.cnvs_id` |
| `msgs_agnt` | INTEGER | FK para `agents.agnt_id` (NULL se bot) |
| `msgs_direction` | TEXT | Direção (sent/received) |
| `msgs_status` | TEXT | Status (delivered/read/failed) |
| `msgs_type` | TEXT | Tipo (text/image/audio/video/file) |
| `msgs_content` | TEXT | Conteúdo da mensagem |
| `msgs_bird` | TEXT | ID único no MessageBird (chave externa) |
| `msgs_created` | DATETIME | Data de criação |
| `msgs_updated` | DATETIME | Última atualização |

**Índices:**
- `idx_messages_bird` em `msgs_bird`
- `idx_messages_cnvs` em `msgs_cnvs`
- `idx_messages_created` em `msgs_created`
- `idx_messages_direction` em `msgs_direction`
- `idx_messages_cnvs_created` em `msgs_cnvs, msgs_created`
- `idx_messages_created_direction_cnvs` em `msgs_created, msgs_direction, msgs_cnvs`

---

### 2.5 `sync`

Armazena o histórico de sincronizações com a API.

```sql
CREATE TABLE sync (
    sync_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_resource TEXT NOT NULL,
    sync_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    sync_duration REAL,
    sync_records_count INTEGER,
    sync_cursor TEXT,
    sync_offset INTEGER DEFAULT 0
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `sync_id` | INTEGER | ID interno (autoincremento) |
| `sync_resource` | TEXT | Recurso sincronizado (contacts/conversations/messages) |
| `sync_created` | DATETIME | Data/hora da sincronização |
| `sync_duration` | REAL | Duração em segundos |
| `sync_records_count` | INTEGER | Número de registros processados |
| `sync_cursor` | TEXT | Cursor para paginação |
| `sync_offset` | INTEGER | Offset para paginação |

**Índices:**
- `idx_sync_resource_created` em `sync_resource, sync_created`

---

### 2.6 `sync_errors`

Armazena erros ocorridos durante sincronização.

```sql
CREATE TABLE sync_errors (
    err_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    err_resource  TEXT,
    err_code      TEXT,
    err_message   TEXT,
    err_context   TEXT,
    err_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    err_retry_count INTEGER DEFAULT 0,
    err_resolved_at DATETIME
);
```

| Coluna | Tipo | Descrição |
|:-------|:-----|:----------|
| `err_id` | INTEGER | ID interno (autoincremento) |
| `err_resource` | TEXT | Recurso afetado |
| `err_code` | TEXT | Código do erro |
| `err_message` | TEXT | Mensagem descritiva |
| `err_context` | TEXT | Contexto adicional |
| `err_at` | DATETIME | Data/hora do erro |
| `err_retry_count` | INTEGER | Número de tentativas |
| `err_resolved_at` | DATETIME | Data/hora da resolução |

---

## 3. Relacionamentos

```
contacts (1) ──── (N) conversations (1) ──── (N) messages
                        │
agents (1) ─────────────┘
        │
        └──────────────── (N) messages
```

- Cada conversa pertence a um contato (`cnvs_cnts -> cnts_id`)
- Cada conversa pode ter um agente atribuído (`cnvs_agnt -> agnt_id`)
- Cada mensagem pertence a uma conversa (`msgs_cnvs -> cnvs_id`)
- Cada mensagem pode ter um agente (`msgs_agnt -> agnt_id`)

---

## 4. Mapeamento de Campos da API

### 4.1 Canais (`cnvs_channel`)

O campo `cnvs_channel` armazena o UUID do canal. O mapeamento para nomes legíveis é feito via `CHANNEL_MAP` no `business_config.yaml`:

```yaml
CHANNEL_MAP:
  "3fa4639084614f7e9fbe121dea5a28e5": "WhatsApp"
  "79a46c93-19a2-4eed-8050-beea59b23528": "Templates/Sites"
```

### 4.2 Departamentos (`cnvs_dept`)

O campo `cnvs_dept` armazena o ID numérico do departamento. O mapeamento é feito via `DEPT_MAP` no `business_config.yaml`.

### 4.3 Motivos e Ocorrências

- `cnvs_contact_reason`: ID do motivo (mapeado via `REASON_MAP`)
- `cnvs_occurrence`: ID da ocorrência (mapeado via `OCCURRENCE_MAP`)

### 4.4 Idiomas (`cnvs_lang`)

O campo `cnvs_lang` armazena o ID numérico do idioma. O mapeamento é feito via `LANG_MAP`:

```yaml
LANG_MAP:
  1: "Português"
  2: "English"
  3: "Español"
```

---

## 5. Boas Práticas

### 5.1 Queries Comuns

**Contar conversas por período:**
```sql
SELECT COUNT(*) FROM conversations 
WHERE cnvs_created BETWEEN '2026-06-01' AND '2026-06-30';
```

**Validar avaliações:**
```sql
SELECT cnvs_bird, cnvs_rating_nps, cnvs_rating_agent 
FROM conversations 
WHERE cnvs_rating_nps IS NOT NULL 
LIMIT 10;
```

**Verificar agentes não mapeados:**
```sql
SELECT COUNT(*) FROM conversations 
WHERE cnvs_agnt IS NOT NULL 
AND cnvs_agnt NOT IN (SELECT agnt_id FROM agents);
```

### 5.2 Índices Importantes

O banco possui índices otimizados para:
- Busca por ID externo (`_bird`)
- Filtro por período (`_created`, `_updated`)
- Filtro por direção de mensagem (`msgs_direction`)
- Combinação de conversa + mensagem (`msgs_cnvs, msgs_created`)

### 5.3 Limpeza de Dados

- **Telefones "None":** O sync protege contra gravação de strings "None". Registros existentes devem ser corrigidos para `NULL`.
- **Espaços em branco:** Nomes de agentes são trimados automaticamente durante o sync.
- **Campos customizados:** `cnts_custom1-4` e `cnvs_sentiment`/`cnvs_category` estão reservados mas não populados atualmente.

---

## 6. Tabelas Não Utilizadas

As seguintes tabelas existem no schema mas não são utilizadas pelo código:

- `sqlite_sequence`: Controle interno do SQLite para autoincremento.

---

## 7. Backup e Manutenção

### 7.1 Backup

```bash
# Copiar o banco
cp m_bird.db m_bird.db.backup

# Ou usar SQLite dump
sqlite3 m_bird.db .dump > backup.sql
```

### 7.2 Restauração

```bash
# A partir de cópia
cp m_bird.db.backup m_bird.db

# A partir de dump
sqlite3 m_bird.db < backup.sql
```

### 7.3 Verificação de Integridade

```sql
-- Verificar integridade
PRAGMA integrity_check;

-- Analisar performance
ANALYZE;
```

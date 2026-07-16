# 🧪 Guia de Testes Manuais

Este documento descreve o procedimento para realizar a validação manual do sistema de relatórios e sincronização, garantindo que as métricas e o fluxo de dados estejam corretos.

## 1. Preparação do Ambiente

Antes de iniciar, certifique-se de que as dependências estão instaladas e o ambiente configurado.

```
# Instalar dependências
uv sync

# Copiar template de ambiente e editar com suas chaves de API
cp .env.example .env
```

## 2. Fluxo de Sincronização (Sync)

**Importante:** Nunca execute sincronização total (`full sync`) se o volume de dados for massivo. Utilize sempre os filtros temporais.

### Sincronização Mensal (Recomendado)
Para validar um período específico (ex: Maio de 2026):
```
uv run python main.py sync --year 2026 --month 5
```
**Critério de Aceite:**
- O log deve mostrar "Monthly synchronization completed".
- O arquivo `m_bird.db` deve ser criado/atualizado.

### Sincronização Incremental
Para buscar apenas os dados da última hora:
```
uv run python main.py sync
```

### Sincronização Completa
Para sincronizar todos os dados estruturais:
```
uv run python main.py sync --full
```

### Sincronização Completa com Mensagens
Para sincronizar tudo incluindo todas as mensagens (pode demorar):
```
uv run python main.py sync --full-messages
```

### Re-extracao de Avaliacoes (Backfill Surveys)
Para re-extrair NPS e avaliações de conversas existentes:
```
uv run python main.py sync --backfill-surveys
```

### Flags Adicionais
| Flag | Descrição | Default |
|:-----|:----------|:--------|
| `--lookback N` | Minutos de retrocesso para sync incremental | 60 |
| `--full` | Sync estrutural completo | false |
| `--full-messages` | Sync completo incluindo todas mensagens | false |
| `--backfill-surveys` | Re-extrair NPS e avaliações | false |

## 3. Geração de Relatórios

Após a sincronização, gere os arquivos de auditoria e performance.

```
uv run python main.py report --year 2026 --month 5
```

**Critério de Aceite:**
- Pasta `reports/YEAR/YEAR-MONTH/` deve ser criada.
- Arquivos `auditoria_contatos.xlsx` e `auditoria_os.xlsx` devem existir em cada subpasta de grupo.
- PDFs de Ordens de Serviço devem ser gerados na pasta `auditoria/OS`.

## 4. Relatório de Qualidade dos Dados

Gere o relatório de qualidade para verificar integridade dos dados:
```
uv run python main.py quality
```

**Critério de Aceite:**
- Pasta `reports/qualidade_dados/` deve ser criada.
- Arquivo `qualidade_dados.xlsx` deve existir.
- Arquivo `README.md` deve existir com resumo da qualidade.

## 5. Validação de Integridade (Banco de Dados)

Utilize o terminal para rodar queries rápidas e validar se o banco reflete a realidade.

### Contagem de conversas por período
```
uv run python -c "import sqlite3; c=sqlite3.connect('m_bird.db'); print(c.execute(\"SELECT count(*) FROM conversations WHERE cnvs_created BETWEEN '2026-05-01' AND '2026-05-31'\").fetchone()[0])"
```

### Validação de campos de Auditoria
Certifique-se de que os campos de avaliação estão sendo populados:
```
uv run python -c "import sqlite3; c=sqlite3.connect('m_bird.db'); [print(r) for r in c.execute(\"SELECT cnvs_bird, cnvs_rating_nps, cnvs_rating_agent FROM conversations WHERE cnvs_rating_nps IS NOT NULL LIMIT 10\").fetchall()]"
```

## 6. Checklist de Qualidade

Ao abrir os relatórios Excel, verifique:
- [ ] **Aba Resumo:** O nome da aba deve estar correto (máx. 31 caracteres).
- [ ] **Métricas ART:** Valores em minutos coerentes (não devem ser negativos ou excessivamente altos sem motivo).
- [ ] **Cálculo de NPS:** Validar se a fórmula `(Promotores - Detratores) / Total` bate com a coluna "NPS Real".
- [ ] **SLA:** Validar se a porcentagem de SLA reflete o atendimento dentro do threshold (padrão 60 min, veja `METRIC_THRESHOLDS.sla_frt_minutes` em `business_bsc.yaml`).

## 7. Troubleshooting

- **ModuleNotFoundError:** Certifique-se de usar `uv sync` primeiro e prefixar comandos com `uv run`.
- **InvalidWorksheetName:** O sistema trunca automaticamente para 31 chars, mas nomes de grupos (definidos em `business_config.yaml` / `business_bsc.yaml`) muito similares podem gerar conflito de arquivos.
- **SQLite Error (No such table):** Execute `uv run python main.py sync` para disparar a inicialização do schema.
- **Dados de avaliação ausentes:** Use `--backfill-surveys` para re-extrair NPS e avaliações de conversas existentes.

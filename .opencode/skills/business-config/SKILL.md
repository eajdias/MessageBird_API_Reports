---
name: business-config
description: Adaptar a configuração de negócio para uma nova empresa (mapas, KPIs, NPS, thresholds e ambiente) sem mexer em código.
---

# Skill: Configuração de Negócio (business-config)

Esta skill orienta como tornar o projeto utilizável por outra empresa apenas editando
arquivos de configuração, sem alterar o código. Use-a sempre que a tarefa envolver
mapas de departamento/motivos/agentes, KPIs do BSC, cortes de NPS, limites de métricas
ou variáveis de ambiente.

## Gatilhos
- Onboarding de um novo cliente/empresa no projeto.
- Adição/remoção de departamentos, motivos, ocorrências ou agentes.
- Mudança de metas, pesos ou regras de pontuação do BSC.
- Ajuste de cortes de NPS ou de limites (SLA/ART/duração).
- Correção de fuso horário ou de credenciais de API.

## Procedimento

1. **Mapas operacionais — `business_config.yaml`** (carregado por `load_and_configure_business`):
   - `DEPT_MAP`, `REASON_MAP`, `OCCURRENCE_MAP`, `LANG_MAP`: chaves são **inteiros** (IDs da API).
   - `DEPT_ROUTING`: nome detectado -> grupo exibido no relatório.
   - `AGENTS`: chave é o `bird_id` (string) -> `{ name, group }`. Agentes novos são criados
     automaticamente no banco durante a sincronização; basta cadastrar o `bird_id`/`group`.

2. **BSC / NPS / thresholds — `business_bsc.yaml`** (carregado por `load_bsc_config`):
   - `KPI_CONFIG`: um bloco por departamento com `t1` (métricas individuais), `t2` (apoio)
     e `penalidades_setoriais`. Cada métrica tem `name`, `description`, `meta`, `peso`, `tipo`
     e, quando aplicável, `niveis`/`cap`.
   - `tipo` suportados: `proporcional`, `escalonado_percentual`, `escalonado_nps`,
     `penalidade_taxa`, `penalidade`, `sim_nao_assiduidade`, `"-"`.
   - `NPS_CONFIG`: `promoter_min` (mínimo p/ promotor) e `passive_min` (mínimo p/ neutro;
     **abaixo disso é detrator**).
   - `METRIC_THRESHOLDS`: `sla_frt_minutes`, `sla_frt_seconds`, `max_art_minutes`,
     `max_duration_minutes`.

3. **Ambiente — `.env`** (carregado por `python-dotenv` via `load_dotenv`):
   - `MESSAGEBIRD_TIMEZONE_OFFSET`: offset em horas vs UTC (ex.: `-3` Brasília). **Fuso NÃO
     vai em YAML**, fica no `.env`.
   - Credenciais (`MESSAGEBIRD_API_KEY_LIVE`, `WORKSPACE_ID_LIVE`, `BASE_URL_*`, `DB_FILENAME`).

4. **Carregamento**: `main.py` aceita `--config-path` (default `business_config.yaml`) e
   `--bsc-config-path` (default `business_bsc.yaml`); ambos são lidos pelo `config_loader`.

5. **Validar**: rode `uv run python main.py total` e confira se o relatório reflete os
   novos nomes/KPIs; `uv run python main.py report --year <ano> --month <mes>` para um mês.

## Pitfalls e Shields
- **Segurança**: `business_config.yaml`, `business_bsc.yaml` e `.env` são **gitignored**
  (só os `.example` são versionados). Nunca remova o ignore nem comite dados reais.
- **Consistência**: as chaves de departamento em `KPI_CONFIG` devem bater com `DEPT_ROUTING`/
  `DEPT_MAP`; caso contrário o BSC pode não encontrar o departamento.
- **NPS**: detrator = nota < `passive_min`. Se mudar `promoter_min`, mantenha
  `promoter_min >= passive_min`.
- **YAML**: valores que começam com `>`/`<` ou contêm `:` devem estar entre aspas; use
  `null` (não `None`) para "sem teto" em `cap`.

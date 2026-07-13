# Plano: Dashboard Executivo Gerencial (estilo Power BI)

> Objetivo: tornar a visualização de dados o mais fácil possível para a gerência,
> seguindo o princípio de *dashboard = 1 tela, só destaques, cores de status (RAG),
> detalhe em drill-down* (Microsoft Learn – dashboards Power BI) e o padrão
> `report-architect` do projeto (Executive-First, cores sóbrias, formatação
> condicional com thresholds de `domain/constants.py`).

## Decisões (confirmadas com o usuário)
- Escopo: melhorar **Visão Geral + BSC**.
- Thresholds de cor (verde/âmbar/vermelho): definidos em **`business_bsc.yaml`** (gestor ajusta sem código).
- Narrativa executiva automática: **Sim**.
- Criar aba dedicada **`Resumo Executivo`** (padrão `mcp_bird`), antes da Visão Geral.

## Princípios aplicados
1. **RAG (Red-Amber-Green)** nos KPIs principais para leitura em segundos.
2. **Tela-resumo condensada** (6 tiles + 1 frase) para quem não é analista.
3. **Drill-down mantido**: BSC / Qualidade / Demanda continuam como detalhamento.
4. **Sem inflar o `ReportAggregator`**: status de cor calculado no exporter a
   partir de `general_metrics` + `EXEC_TARGETS` (alinhado ao skill `report-architect`).
5. **DRY**: estilos de RAG centralizados num helper privado.

## Mudanças por arquivo

### 1. `business_bsc.yaml` (e `.example`)
Novo bloco `EXEC_TARGETS` no final do arquivo:
```yaml
# Metas de cor (RAG) do dashboard executivo.
# direction: "higher" = quanto maior melhor; "lower" = quanto menor melhor.
EXEC_TARGETS:
  nps_real:           { green: 70, amber: 50, direction: higher }
  sla_compliance:     { green: 90, amber: 80, direction: higher }
  csat_elogio:        { green: 40, amber: 30, direction: higher }   # % elogio / total atendimentos
  art_medio:          { green: 15, amber: 30, direction: lower }
  duracao_media:      { green: 30, amber: 60, direction: lower }
  cobertura_avaliados: { green: 60, amber: 40, direction: higher }  # % chats avaliados (nota)
  cobertura_nps:       { green: 60, amber: 40, direction: higher }  # % atendimentos com NPS
```
(`total_chats` fica sem RAG — é volume.)

### 2. `domain/constants.py`
- Adicionar `DEFAULT_EXEC_TARGETS` (mesmo conteúdo acima) e
  `EXEC_TARGETS = DEFAULT_EXEC_TARGETS` na seção de configuração dinâmica.

### 3. `infrastructure/config_loader.py`
- Em `load_bsc_config`: ler `"EXEC_TARGETS"` de `bsc_config` e injetar em
  `constants.EXEC_TARGETS` (mesmo padrão do `KPI_CONFIG`).

### 4. `infrastructure/exporters/excel_exporter.py`
- **Nova aba `Resumo Executivo`** (`_write_exec_summary_tab`), primeira tab em
  `export_executive_dashboard` e `export_annual_dashboard`:
  - Faixa de 6 tiles RAG: NPS Real, SLA, CSAT/Elogio, ART Médio, Volume de Chats, Cobertura.
  - 1–3 linhas de **narrativa automática** (gerada de `general_metrics` + `prev_month_metrics`).
  - Donut NPS compacto (reaproveita `dto.nps_distribution`).
- **Visão Geral (`_write_dashboard_tab`)**: colorir cada card com RAG conforme
  `EXEC_TARGETS` (reaproveita `COLOR_ACCENT/WARNING/ALERT`).
- **BSC (`_write_bsc_tab`)**: aplicar `conditional_format` no **TOTAL KPI** de cada
  agente por sinal (verde ≥ 0, vermelho < 0).
- Helper privado `_rag_color(target_key, value)` para decidir a cor.

### 5. `tests/exporters/test_exporter_style.py`
- Adicionar `"Resumo Executivo"` aos nomes seguros (`test_tab_names_no_special_chars`).
- Testar presença de `EXEC_TARGETS` em `constants` e carga pelo `config_loader`.

## Verificação
- `uv run pytest tests/exporters/ tests/domain/`
- Gerar relatório de exemplo e inspecionar abas **Resumo Executivo**, **Visão Geral** e **BSC**
  (cores RAG, narrativa e TOTAL KPI colorido).

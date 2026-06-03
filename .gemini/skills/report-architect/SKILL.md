---
name: report-architect
description: Especialista em Dashboards Executivos e visualização de dados profissional seguindo o padrão mcp_bird.
---

# Skill: Arquiteto de Relatórios (report-architect)

Esta skill foca na excelência visual e estrutural dos relatórios gerados pelo sistema, garantindo valor de negócio para o usuário final.

## Gatilhos
- Modificação de exportadores de Excel (`infrastructure/exporters/`).
- Criação de novos componentes visuais (Gráficos, Heatmaps).
- Atualização da interface de `ReportExporter`.

## Procedimento

1.  **Design Executive-First**: 
    - Implemente layouts que utilizem `merge_range`, cores sóbrias e headers profissionais.
    - Referência: Aba "Resumo Executivo" do projeto original `mcp_bird`.

2.  **Definir DTO de Interface**: 
    - Antes de codificar a infraestrutura, defina o `DashboardDTO` na camada de aplicação. 
    - A infraestrutura deve apenas consumir este DTO.

3.  **Implementar via Sub-Agregadores**: 
    - Não infle o `ReportAggregator`. 
    - Divida a agregação em estratégias isoladas: `TemporalAggregator`, `SLAAggregator`, `TopicAggregator`.

4.  **Aplicar Formatação Condicional**: 
    - Use os thresholds de SLA definidos em `domain/constants.py` para destacar células (vermelho/verde) dinamicamente.

## Pitfalls e Shields
- **DRY**: Não duplique lógica de formatação. Centralize estilos comuns em métodos privados no `ExcelExporter`.
- **YAGNI**: Não crie abas de dados de apoio que não serão utilizadas por gráficos ou auditoria real.
- **Created vs Resolved**: O dashboard oficial do MessageBird conta tickets "Resolvidos" no período. Consultas baseadas em `cnvs_created` podem causar discrepâncias, pois ignoram tickets abertos anteriormente mas resolvidos no mês atual. Prefira filtrar por `cnvs_updated` e `status` para métricas de produtividade.

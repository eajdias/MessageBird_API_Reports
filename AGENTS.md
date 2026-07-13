# Project: Omnichannel Reporting Tool (Bird API)

Este projeto segue rigorosamente a **Clean Architecture**. O opencode deve usar o `AGENTS.md` raiz e as skills em `.opencode/skills/` para instruções detalhadas conforme o contexto da tarefa.

## 🏗️ Estrutura de Mandatos (Navegação)
- `domain/`: Regras de pureza, Entidades e Lógica Canônica.
- `application/`: Orquestração, Use Cases, Interfaces e DTOs.
- `infrastructure/`: Detalhes técnicos, Repositórios e Exporters (Excel/PDF).
- `presentation/`: Ferramentas e pontos de entrada CLI.
- Arquivos de configuração na raiz: `.env` (segredos), `business_config.yaml` (mapas de negócio) e `business_bsc.yaml` (NPS/BSC/thresholds).
- `tests/`: Padrões de teste e isolamento de banco.
- `docs/`: Guia de arquitetura e evolução dos relatórios.

## 🧠 Ativação de Skills
Carregue a skill correspondente quando a tarefa se encaixar no seu propósito:
- `arch-guard`: revisões arquiteturais e criação/refatoração de código.
- `report-architect`: evoluir Dashboards/Excel e exportadores.
- `sync-maintainer`: mexer na pipeline de sincronização MessageBird -> SQLite.
- `add-business-metric`: adicionar ou alterar métricas de negócio (NPS, SLA, FRT, etc.).
- `business-config`: adaptar a configuração para uma nova empresa (mapas, KPIs, NPS, thresholds, ambiente) sem mexer em código.

Cada skill está em `.opencode/skills/<nome>/SKILL.md` e descreve gatilhos, procedimento e armadilhas.

**Mandato Global:** NUNCA vaze lógica de negócio para a infraestrutura ou dependências para o domínio.

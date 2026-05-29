# Project: Omnichannel Reporting Tool (Bird API)

Este projeto segue rigorosamente a **Clean Architecture**. O Gemini CLI deve usar os arquivos `GEMINI.md` locais para instruções detalhadas conforme navega pelas pastas.

## 🏗️ Estrutura de Mandatos (Navegação)
- `domain/`: Regras de pureza, Entidades e Lógica Canônica.
- `application/`: Orquestração, Use Cases, Interfaces e DTOs.
- `infrastructure/`: Detalhes técnicos, Repositórios e Exporters (Excel/PDF).
- `presentation/`: Ferramentas MCP e pontos de entrada CLI.
- `config/`: Gestão de ambiente e segredos.
- `tests/`: Padrões de teste e isolamento de banco.
- `docs/`: Guia de arquitetura e evolução dos relatórios.

## 🧠 Ativação de Skills (`activate_skill`)
- `arch-guard`: Ativar para revisões arquiteturais.
- `report-architect`: Ativar para evoluir Dashboards/Excel.
- `sync-maintainer`: Ativar para mexer na sincronização.
- `add-business-metric`: Ativar para novas métricas.

**Mandato Global:** NUNCA vaze lógica de negócio para a infraestrutura ou dependências para o domínio.

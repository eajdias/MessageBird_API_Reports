# Mandatos da Camada de Aplicação (Orchestration)

Esta camada define o "O que o sistema faz" sem dizer "Como".

## 📏 Regras Estritas
1.  **Interfaces:** Dependa apenas de classes abstratas definidas em `interfaces/`.
2.  **Agregação:** O `ReportAggregator` deve ser o maestro, delegando cálculos pesados para o Domínio e transformações específicas para sub-agregadores.
3.  **DTOs:** Converta entidades de domínio em DTOs antes de passar para os Exporters da Infraestrutura.
4.  **Serviços:** Se um serviço atingir +300 linhas, aplique o princípio de segregação.

## 🛡️ Proteções
- NUNCA instancie classes de infraestrutura (como `SqliteRepository`) aqui; use injeção de dependência via construtor.

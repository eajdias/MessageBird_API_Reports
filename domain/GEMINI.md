# Mandatos da Camada de Domínio (Pure Business Logic)

Esta camada contém as regras de ouro que nunca mudam com a tecnologia.

## 📏 Regras Estritas
1.  **Pureza Total:** Sem importações de outras camadas ou libs externas (exceto stdlib).
2.  **Cálculos (`services/`):** Todos os cálculos de KPI (NPS, SLA) devem ser puras funções estáticas no `MetricsCalculator`.
3.  **Tempo (`logic.py`):** Centralizar manipulação de timestamps e timezone (Offset -3) aqui.
4.  **Configuração (`constants.py`):** Mapeamento de departamentos e headers de relatórios.

## 🛡️ Proteções
- Se precisar de uma lib externa para um cálculo, a interface fica aqui, mas a implementação vai para `infrastructure`.
- Use `dataclasses` para garantir tipos fortes.

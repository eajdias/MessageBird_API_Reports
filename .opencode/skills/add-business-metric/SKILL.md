---
name: add-business-metric
description: Procedimento para adicionar uma nova métrica de negócio ao projeto mbird_eajdias, seguindo a arquitetura refatorada (Clean Architecture).
---

# Adicionando Métricas de Negócio

Este guia descreve como adicionar um novo cálculo de métrica ao projeto, garantindo que a lógica permaneça centralizada e testável.

## Gatilhos
- Solicitação para calcular NPS, SLA, FRT ou novas métricas customizadas.
- Alteração de regras de cálculo existentes.

## Procedimento

1.  **Implementar o Cálculo no Domínio**:
    Adicione o método estático em `domain/services/metrics_calculator.py`.
    - Priorize cálculos em Python sobre lógicas de SQL.
    - Garanta que o método seja testável sem dependências externas.
    - Use `Optional[float]` para lidar com dados ausentes.

2.  **Atualizar Cabeçalhos de Relatório**:
    Em `domain/constants.py`, adicione o nome da métrica em `AGENTS_HEADER`, `DEPARTMENTS_HEADER` ou `GROUPS_HEADER` conforme necessário.

3.  **Integrar no Agregador de Aplicação**:
    Em `application/services/report_aggregator.py`, atualize `aggregate_statistics` (ou crie um novo método) para processar a lista de conversas e invocar a `MetricsCalculator`.

4.  **Ajustar Mapeamento na Infraestrutura**:
    Em `infrastructure/database/sqlite_repository.py`, certifique-se de que os dados brutos necessários para o novo cálculo estão sendo extraídos e passados para a camada de aplicação.

5.  **Validar com Testes Unitários**:
    Adicione casos de teste em `tests/domain/services/test_metrics_calculator.py` para cobrir a nova lógica.

## Pitfalls e Shields
- **Nomenclatura**: Use nomes consistentes (ex: sufixo `_min` para tempos em minutos).
- **Timezones**: Lembre-se que o timezone canonical é -3 (definido em `domain/logic.py`).
- **DRY**: Nunca implemente lógica de cálculo diretamente no repositório ou no expositor.

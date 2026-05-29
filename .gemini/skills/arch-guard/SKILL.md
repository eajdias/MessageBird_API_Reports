---
name: arch-guard
description: Guardião da integridade arquitetural (Clean Architecture) e princípios SOLID para o projeto mbird_eajdias.
---

# Skill: Guardião da Arquitetura (arch-guard)

Esta skill deve ser ativada antes de qualquer implementação ou durante revisões de código para garantir que a fundação do projeto permaneça sólida.

## Gatilhos
- Criação de novos arquivos ou pastas.
- Refatoração de lógica existente.
- Revisão de Pull Requests ou propostas de design.

## Procedimento

1.  **Validar Dependências Cruzadas**: 
    - Verifique se o `domain/` está livre de dependências externas.
    - Garanta que as camadas superiores apontam apenas para o centro (Domain -> Application -> Infrastructure/Presentation).

2.  **Analisar Coesão e Acoplamento (SRP)**: 
    - Avalie se uma classe de serviço está acumulando muitas responsabilidades. 
    - Se houver muitos métodos privados ou "and" no nome da classe, force a fragmentação via **Composição**.

3.  **Detectar Vazamento de Camadas (Leakage)**: 
    - Impeça que detalhes de infraestrutura (SQL, libs de Excel como `xlsxwriter`, APIs externas) apareçam em Use Cases ou Entidades.

4.  **Verificar Lógica Canônica**: 
    - Toda manipulação de tempo e cálculos de negócio deve usar exclusivamente as utilidades do Domínio (`domain/logic.py` e `domain/services/`).

## Pitfalls e Shields
- **Escudo**: NUNCA permitir casts agressivos (ex: `any` em TS ou casts forçados em Python) ou supressão de warnings de linter/tipo.
- **Erro Comum**: Tentar resolver problemas de performance na aplicação em vez de otimizar a camada de infraestrutura (repositório).

---
name: sync-maintainer
description: Mantenedor da pipeline de sincronização MessageBird -> SQLite, focando em performance e integridade.
---

# Skill: Mantenedor de Sincronização (sync-maintainer)

Esta skill supervisiona a ingestão de dados, garantindo que o banco de dados local reflita fielmente e eficientemente a API externa.

## Gatilhos
- Alteração nos comandos de sincronização (`main.py` e `presentation/terminal.py`).
- Adição de novos campos da API MessageBird.
- Mudanças no esquema do banco de dados `m_bird.db`.

## Procedimento

1.  **Garantir Modo WAL**: 
    - Valide se as conexões `aiosqlite` estão configuradas com `PRAGMA journal_mode=WAL` para permitir leituras e escritas concorrentes.

2.  **Validar Lógica Incremental**: 
    - Utilize o campo `cnvs_updated` para baixar apenas o que mudou desde a última sincronização bem-sucedida.

3.  **Mapeamento Canônico**: 
    - Atualize os resolvers em `domain/constants.py` para garantir que campos complexos da API sejam normalizados para nomes de domínio amigáveis.

## Pitfalls e Shields
- **Segurança**: Bloqueie qualquer tentativa de logar `api_key` ou `organization_id` em mensagens de erro ou logs de depuração.
- **Integridade**: Use transações para garantir que falhas de rede no meio de um lote de mensagens não deixem o banco em estado inconsistente.

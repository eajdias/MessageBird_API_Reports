# Mandatos de Configuração e Ambiente

Gestão de variáveis, segredos e inicialização.

## 📏 Regras Estritas
1.  **Segredos:** NUNCA comite arquivos `.env`. Use `.env.example` como template.
2.  **Loading:** Configurações dinâmicas devem ser carregadas via `domain/constants.py:load_business_config`.
3.  **Inicialização:** O esquema do banco é definido em `infrastructure/database/init_db.py`.

## 🛡️ Proteções
- Valide a existência das chaves de API essenciais no startup do sistema.

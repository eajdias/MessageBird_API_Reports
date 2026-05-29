# Mandatos de Testes e Qualidade

Padrões para garantir que o sistema continue funcionando após mudanças.

## 📏 Regras Estritas
1.  **Isolamento de Banco:** Use a fixture `isolated_db` para garantir que o banco real `m_bird.db` nunca seja alterado.
2.  **Mocks:** Use `respx` para simular respostas da API MessageBird.
3.  **Cobertura:** Novas métricas em `domain/services/` exigem testes unitários exaustivos.
4.  **Integração:** Testes em `tests/integration/` devem validar o fluxo UseCase -> Repositório Mock.

## 🧪 Estrutura
- `tests/domain/`: Testes unitários de lógica pura.
- `tests/integration/`: Fluxos de componentes.

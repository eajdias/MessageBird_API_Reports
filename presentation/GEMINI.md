# Mandatos de Apresentação (Tools & CLI)

Ponto de contato com o usuário (MCP Tools e Shell).

## 📏 Regras Estritas
1.  **Ferramentas MCP:** Devem ser wrappers finos que chamam Use Cases da camada de Aplicação.
2.  **Parsing:** Validação de argumentos de entrada e formatação de saída para o usuário (Rich/JSON).
3.  **CLI Scripts:** Scripts em `scripts/` ou root devem seguir o padrão de logging do projeto.

## 🛠️ Ferramentas Principais
- `presentation/tools/`: Implementações de ferramentas expostas via MCP Server.
- `main.py`: Entrada principal do servidor.

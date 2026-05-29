# Mandatos da Camada de Infraestrutura (Technical Details)

Aqui vivem os detalhes "sujos" e mutáveis (Banco, Arquivos, Redes).

## 📏 Regras Estritas
1.  **Isolamento:** Bibliotecas (`xlsxwriter`, `aiosqlite`, `requests`) devem estar contidas e nunca expostas em assinaturas de métodos públicos.
2.  **Persistência:** Otimizações SQL, índices e modo WAL do SQLite são definidos aqui.
3.  **Exportação:** Lógica de "design" (fontes, cores, gráficos do Excel) pertence exclusivamente aos `Exporters`.
4.  **Conformidade:** Implementar rigorosamente as interfaces definidas na `Application`.

## 🛡️ Proteções
- Se uma biblioteca for trocada, apenas esta pasta deve sofrer alterações.

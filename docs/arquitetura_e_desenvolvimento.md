# Guia de Arquitetura e Padrões de Desenvolvimento (Omnichannel MCP)

Este documento estabelece as diretrizes fundamentais para o desenvolvimento e manutenção do projeto, integrando princípios de **Clean Architecture**, **Context7 Recommendations** e padrões **SOLID**.

---

## 1. Princípios de Engenharia (Core Mandates)

O desenvolvimento deve ser regido rigorosamente pelos seguintes princípios:

| Princípio | Descrição e Aplicação no Projeto |
| :--- | :--- |
| **Clean Architecture** | Separação estrita entre regras de negócio (Domain/Application) e detalhes técnicos (Infrastructure/Presentation). |
| **SOLID** | **SRP**: Classes com responsabilidade única. **OCP**: Aberto para extensão, fechado para modificação. **LSP/ISP/DIP**: Interfaces claras e inversão de dependência. |
| **DRY (Don't Repeat Yourself)** | Lógicas de cálculo de métricas e conversão de datas devem residir em um único local no Domínio. |
| **KISS (Keep It Simple, Stupid)** | Evitar abstrações excessivas. Preferir soluções legíveis e diretas. |
| **YAGNI (You Ain't Gonna Need It)** | Implementar apenas o necessário para os requisitos atuais. Evitar "future-proofing" especulativo. |
| **SoC (Segregation of Concerns)** | A camada de aplicação não deve saber da existência de bibliotecas como `xlsxwriter` ou `aiosqlite`. |

---

## 2. Estrutura de Camadas

O projeto é organizado radialmente, onde as dependências apontam sempre para o centro (Domínio).

### 2.1 Camada de Domínio (`domain/`)
*   **Entities:** Modelos de dados puros (`dataclasses`). Ex: `RawConversationData`, `ProcessedReportData`.
*   **Services:** Lógica matemática e regras de negócio puras. Ex: `MetricsCalculator`.
*   **Logic:** Funções utilitárias canônicas para tempo e conversões.
*   **Constants:** Definições de negócio (Headers, SLAs, Mapas de Departamento).
*   **Rigor:** **ZERO** dependências externas. Apenas Python standard library.

### 2.2 Camada de Aplicação (`application/`)
*   **Use Cases:** Orquestradores de fluxo. Não contêm lógica de cálculo, apenas chamam o Domínio e Infraestrutura.
*   **Services:** Agregadores e transformadores de dados. Devem usar **Composição** para evitar "God Classes".
*   **Interfaces:** Contratos (Abstract Base Classes) para repositórios e exportadores.
*   **Rigor:** Depende apenas do Domínio e das Interfaces.

### 2.3 Camada de Infraestrutura (`infrastructure/`)
*   **Database:** Implementações específicas de persistência (`sqlite_repository.py`).
*   **Exporters:** Implementações de saída (Excel, PDF, Markdown).
*   **Rigor:** Onde os frameworks e bibliotecas externas vivem. Nenhuma lógica de negócio deve ser "vazada" para cá.

### 2.4 Camada de Apresentação (`presentation/`)
*   **Tools:** Implementação das ferramentas MCP (Model Context Protocol).
*   **CLI:** Scripts de execução direta.

---

## 3. Padrões de Implementação Recomendados (Context7)

### A. Evitando "God Classes"
Ao expandir os relatórios ou o sincronizador:
1.  **Divide and Conquer:** Se uma classe de serviço atingir muitos métodos de agregação, fragmente-a em pequenas estratégias (ex: `HeatmapStrategy`, `SLAStrategy`).
2.  **Injeção de Dependência:** Sempre passe dependências via construtor para facilitar testes e substituições.

### B. Tratamento de Datas e Timezones
1.  **UTC no Banco:** Dados em repouso devem estar em UTC.
2.  **Local no Relatório:** A conversão para o Timezone local (Offset -3) deve ocorrer apenas na camada de Domínio (`logic.py`) ou no momento da exibição final.

### C. Evolução de Relatórios
1.  **DTOs (Data Transfer Objects):** Use objetos simples para transferir dados entre a Aplicação e os Exporters.
2.  **Formatadores Isolados:** A lógica de "como pintar uma célula de vermelho" deve estar dentro do `ExcelExporter` e nunca no `ReportAggregator`.

---

## 4. Checklist de Novos Recursos

- [ ] A lógica de cálculo está no `domain/services/`?
- [ ] O novo método no repositório retorna dados crus ou entidades de domínio?
- [ ] O Use Case está orquestrando ou calculando? (Deve apenas orquestrar).
- [ ] Existem testes unitários para a nova lógica de domínio?
- [ ] O princípio DRY foi respeitado na manipulação dos novos dados?

---
*Este guia é um documento vivo e deve ser atualizado conforme a arquitetura evolui.*

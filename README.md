# Standalone Report Generator - MessageBird Omnichannel

Este projeto é uma ferramenta autônoma para sincronização de dados e geração de relatórios avançados baseados na API Omnichannel da MessageBird. Ele foi extraído do projeto base para funcionar de forma completamente isolada, sem depender de ferramentas conversacionais (Model Context Protocol).

## 🚀 Propósito

O objetivo deste módulo é garantir que gestores possam puxar dados granulares, emitir laudos e realizar análises de SLA (Service Level Agreement) em um ambiente controlado, de forma automatizada (via CRON jobs) ou manual via CLI.

Sua arquitetura foi construída baseada no padrão **Clean Architecture**, dividindo responsabilidades em camadas:
- **Domain:** Lógicas puras de fuso horário, limites SLA e mapeamentos corporativos.
- **Application:** Os Casos de Uso (ex: `GenerateReportUseCase`, `SyncDatabaseUseCase`), serviços de agregação e serviços de auditoria.
- **Infrastructure:** Conexão com SQLite (`aiosqlite`), clientes de API (`httpx`) e exportadores nativos (`xlsxwriter`, `fpdf2`).
- **Presentation:** Uma interface de terminal CLI rica em detalhes (via `rich`).

## 📚 Como Começar

O fluxo principal está automatizado via `Makefile`.

1. **Copie o template de ambiente** e preencha suas credenciais:
   ```bash
   cp config/.env.example config/.env
   ```
2. **Instale as dependências** (com lockfile reproduzível via `uv.lock`):
   ```bash
   make install
   ```
3. **Leia a Documentação Completa:**
   Para instruções detalhadas de como usar os filtros de setor, emitir Ordens de Serviço (OS) e atualizar o banco de dados, consulte o guia oficial:

   👉 **[Ler o Guia de Uso (docs/guia_de_uso.md)](docs/guia_de_uso.md)**

## ✨ Principais Funcionalidades

- **Sincronização Bidirecional:** Conecta na API da MessageBird e espelha contatos, conversas e mensagens de forma incremental.
- **Isolamento por Setor:** Permite gerar pastas de relatórios divididas por departamentos organizacionais (Comercial, Suporte, Diretoria), evitando que áreas acessem dados que não lhes pertencem.
- **Dashboard Global (Excel):** Uma tabela complexa mostrando ART, NPS e conformidade de SLA.
- **Auditoria Detalhada:** Relatórios de contatos, demanda horária e Ordens de Serviço, processados por serviços de aplicação dedicados.
- **Faturas em PDF:** Geração de Protocolos/Ordens de Serviço em `.pdf` por cada atendimento.
- **Build Reproduzível:** Gerenciamento de dependências via `uv.lock`, garantindo versões consistentes em todos os ambientes.
- **Testes de Integração:** Pipeline completo validado (`process_all` → `aggregate_statistics` → `build_excel_rows`).

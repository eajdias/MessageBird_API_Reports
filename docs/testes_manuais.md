# 🧪 Guia de Testes Manuais

Este documento descreve o procedimento para realizar a validação manual do sistema de relatórios e sincronização, garantindo que as métricas e o fluxo de dados estejam corretos.

## 1. Preparação do Ambiente

Antes de iniciar, certifique-se de que as dependências estão instaladas e o ambiente configurado.

```bash
# Instalar dependências
make install

# Validar variáveis de ambiente
cp config/.env.example config/.env
# Edite config/.env com suas chaves de API
```

## 2. Fluxo de Sincronização (Sync)

**Importante:** Nunca execute sincronização total (`full sync`) se o volume de dados for massivo. Utilize sempre os filtros temporais.

### Sincronização Mensal (Recomendado)
Para validar um período específico (ex: Maio de 2026):
```bash
make sync-monthly YEAR=2026 MONTH=5
```
**Critério de Aceite:**
- O log deve mostrar "Monthly synchronization completed".
- O arquivo `m_bird.db` deve ser criado/atualizado.

### Sincronização Incremental
Para buscar apenas os dados da última hora:
```bash
make sync
```

## 3. Geração de Relatórios

Após a sincronização, gere os arquivos de auditoria e performance.

```bash
make report YEAR=2026 MONTH=5
```

**Critério de Aceite:**
- Pasta `reports/YEAR/YEAR-MONTH/` deve ser criada.
- Arquivos `auditoria_contatos.xlsx` e `auditoria_os.xlsx` devem existir em cada subpasta de grupo.
- PDFs de Ordens de Serviço devem ser gerados na pasta `auditoria/OS`.

## 4. Validação de Integridade (Banco de Dados)

Utilize o terminal para rodar queries rápidas e validar se o banco reflete a realidade.

### Contagem de conversas por período
```bash
sqlite3 m_bird.db "SELECT count(*) FROM conversations WHERE cnvs_created BETWEEN '2026-05-01' AND '2026-05-31';"
```

### Validação de campos de Auditoria
Certifique-se de que os campos de avaliação estão sendo populados:
```bash
sqlite3 m_bird.db "SELECT cnvs_bird, cnvs_rating_nps, cnvs_rating_agent FROM conversations WHERE cnvs_rating_nps IS NOT NULL LIMIT 10;"
```

## 5. Checklist de Qualidade

Ao abrir os relatórios Excel, verifique:
- [ ] **Aba Resumo:** O nome da aba deve estar correto (máx. 31 caracteres).
- [ ] **Métricas ART:** Valores em minutos coerentes (não devem ser negativos ou excessivamente altos sem motivo).
- [ ] **Cálculo de NPS:** Validar se a fórmula `(Promotores - Detratores) / Total` bate com a coluna "NPS Real".
- [ ] **SLA:** Validar se a porcentagem de SLA reflete o atendimento dentro do threshold (ex: 5 min).

## 6. Troubleshooting

- **ModuleNotFoundError:** Certifique-se de usar `make` ou prefixar comandos com `uv run`.
- **InvalidWorksheetName:** O sistema trunca automaticamente para 31 chars, mas nomes de grupos no `business_config.json` muito similares podem gerar conflito de arquivos.
- **SQLite Error (No such table):** Execute `make sync` (ou qualquer sync) para disparar a inicialização do schema.

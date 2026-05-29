# Configuração Avançada (Standalone)

Para garantir que o gerador de relatórios seja 100% independente do projeto principal, todas as suas configurações estão isoladas na pasta `config/`. 

Esta pasta não é rastreada pelo Git para proteger os dados sensíveis da sua empresa. Antes de rodar a sua primeira sincronização, você precisará configurar dois arquivos:

## 1. O arquivo `.env`

O projeto inclui um template em `config/.env.example` com todas as variáveis necessárias documentadas. Para começar:

```bash
cp config/.env.example config/.env
```

Em seguida, edite `config/.env` preenchendo as credenciais da API da MessageBird:

```env
MESSAGEBIRD_API_KEY_LIVE="sua_chave_live_aqui"
MESSAGEBIRD_WORKSPACE_ID_LIVE="seu_workspace_id_aqui"
```

**(Opcional):** Você também pode mapear IDs fixos para o nome de certos Agentes. Isso resolve casos em que a API da MessageBird não consiga popular o nome adequadamente na tabela.
```env
MESSAGEBIRD_AGENT_1="cb13645b-d36c-48be-8f35-xxxx:Agente Exemplo A"
MESSAGEBIRD_AGENT_2="cb13645b-d36c-48be-8f35-yyyy:Agente Exemplo B"
```

## 2. O arquivo `business_config.json`

O arquivo `business_config.json` (também dentro de `config/`) é o coração do motor de relatórios. É através dele que o sistema sabe como transformar dados brutos (ex: `cnvs_dept = 1`) em relatórios compreensíveis (ex: "Departamento de Suporte Técnico").

Exemplo da estrutura que deve ser criada em `config/business_config.json`:

```json
{
  "DEPT_MAP": {
    "1": "Suporte Técnico",
    "2": "Comercial",
    "3": "Financeiro",
    "4": "Ouvidoria",
    "5": "Customer Success"
  },
  "AGENT_GROUPS": {
    "Suporte Técnico": [
      "Agente Exemplo A",
      "Agente Exemplo B",
      "Agente Exemplo C"
    ],
    "Comercial": [
      "Consultor Exemplo A",
      "Consultor Exemplo B"
    ],
    "Internacional": [
      "Representante Exemplo A"
    ]
  }
}
```

### Por que mapear os Setores (`AGENT_GROUPS`)?
Ao criar a divisão `AGENT_GROUPS`, você habilita o comando `--sector` no terminal.
Por exemplo, ao configurar o grupo "Comercial" acima, você poderá gerar os relatórios apenas para os agentes daquela lista, economizando tempo de extração:

```bash
make report YEAR=2024 MONTH=5 SECTOR="Comercial"
```

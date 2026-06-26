import json
import os
from domain.services.metrics_calculator import MetricsCalculator

# ── ART / SLA ────────────────────────────────────────────────────────────────
SLA_FRT_THRESHOLD_SECONDS = 3600
SLA_FRT_THRESHOLD_MINUTES = 60
MAX_ART_MINUTES = 480       # 8 horas — máximo aceitável para Average Response Time
MAX_DURATION_MINUTES = 630  # 10h30 — máximo aceitável para duração total de chat

# ── Agent report headers ──────────────────────────────────────────────────────

AGENTS_HEADER = [
    "Dept maior atendimento",
    "Grupo",
    "Nome do Agente",
    "Total de Chats",
    "% do Departamento",
    "Elogios (nota 4-5)",
    "% Elogios",
    "Feedback Negativo (nota 1-2)",
    "% Feedback Negativo",
    "Total de Msgs",
    "Msgs/Chat",
    "Nota Técnica Média",
    "NPS Médio",
    "NPS Real",
    "ART Técnico (min)",
    "SLA Compliance (%)",
    "Duração Média (min)",
    "Clientes Únicos",
    "Retornantes",
]

DEPARTMENTS_HEADER = [
    "Departamento",
    "Total de Chats",
    "% do Total",
    "Total de Msgs",
    "ART Médio (min)",
    "SLA Compliance (%)",
    "Duração Média (min)",
    "NPS Médio",
    "NPS Real",
    "Nota Técnica Média",
    "Clientes Únicos",
    "Retornantes",
]

GROUPS_HEADER = [
    "Grupo",
    "Total de Chats",
    "Total de Msgs",
    "ART Médio (min)",
    "SLA Compliance (%)",
    "Duração Média (min)",
    "NPS Médio",
    "NPS Real",
    "Nota Técnica Média",
    "Clientes Únicos",
    "Retornantes",
]

# ── Audit report headers ──────────────────────────────────────────────────────

CONTACTS_HEADER = [
    "Agente mais Participativo",
    "Cliente",
    "Telefone",
    "Chats no Mês",
    "Msgs no Mês",
    "Nota Média",
    "NPS Média",
    "Datas",
    "Atendimento pelos Agentes",
]

CHATS_HEADER = [
    "Dia",
    "Maior Demanda",
    "Chats Iniciados",
    "Chats Concluidos",
    "Chats Pendentes",
    "Mensagens Trocadas",
    "Agent Chat MVP",
    "Agent Msgs MVP",
    "Duração Média Chats (min)",
    "Msgs em Média por Chat",
    "ART Técnico (min)",
    "ART Cliente (min)",
    "NPS Médio",
    "Nota Técnica Média",
    "Dept maior atendimento",
    "Clientes Únicos",
    "Retornantes",
]

DEMAND_HEADER = [
    "Hora do dia",
    "Novos Chats",
    "Msgs Recebidas",
    "Msgs Enviadas",
    "Média de Novos Chats",
]

OS_HEADER = [
    "ID Bird",
    "Data de Início",
    "Agente",
    "Grupo",
    "Cliente",
    "Telefone",
    "Email",
    "Documento",
    "Sistema",
    "Departamento",
    "Motivo do Contato",
    "Ocorrência",
    "Nota Técnico",
    "Nota NPS",
    "Reaberturas",
    "Descrição do Problema",
    "Duração (min)",
    "ID BD"
]

# ── Annual report headers ─────────────────────────────────────────────────────

ANNUAL_HEADER = [
    "Mês",
    "Total de Chats",
    "Total de Msgs",
    "ART Médio (min)",
    "SLA Compliance (%)",
    "Duração Média (min)",
    "NPS Real",
    "Nota Técnica Média",
    "Elogios",
    "Feedback Negativo",
    "Clientes Únicos",
    "Retornantes",
]

# ── Default Maps ─────────────────────────────────────────────────────────────
DEFAULT_DEPT_MAP = {
    1: "Suporte Técnico",
    2: "Comercial",
    3: "Financeiro",
    4: "Ouvidoria",
    5: "Customer Success",
}

DEFAULT_REASON_MAP = {
    1: {1: "Problemas técnicos", 2: "Agendamentos", 3: "Manuais de uso (PDF ou vídeos)"},
    2: {1: "Falar com um consultor comercial", 2: "Agendar uma demonstração"},
    3: {1: "Boleto", 2: "Nota Fiscal", 3: "Sistema bloqueado", 4: "Mensagem de cobrança", 5: "Não consta"},
    4: {1: "Reclamação", 2: "Sugestão", 3: "Elogio"},
    5: {1: "Instalações"},
}

DEFAULT_OCCURRENCE_MAP = {
    1: {
        1: {1: "Hardware", 2: "Captura de imagem", 3: "Configuração", 4: "Arquivos", 5: "Licença", 6: "Não consta"},
        2: {1: "Reinstalação", 2: "Atualização (v1.0.0)", 3: "Migração", 4: "Treinamento"},
    },
    2: {1: {1: "Software A", 2: "Software B", 3: "Software C", 4: "Software D"}},
    5: {1: {1: "Coleta de dados"}},
}

DEFAULT_LANG_MAP = {1: "Português", 2: "English", 3: "Español"}

DEFAULT_KPI_CONFIG = {
    "Suporte Técnico": {
        "t1": [
            {
                "name": "Elogios de atendimento / Feedback",
                "description": "Notas 4 e 5 são consideradas Feedback positivo.",
                "metric": "% em cima do total de avaliados com nota",
                "meta": ">40%", "peso": 30, "tipo": "escalonado_percentual",
                "niveis": [{"min": 40, "pts": 30, "extra_per_unit": 0.75}, {"min": 35, "pts": 15}, {"min": 30, "pts": 10}],
                "cap": 60,
            },
            {
                "name": "NPS (Net Promoter Score)",
                "description": "Pontuação do NPS individual do agente. Cálculo oficial: ((Promotores - Detratores) / Total) × 100",
                "metric": "NPS individual do agente",
                "meta": ">=70/63/50", "peso": 30, "tipo": "escalonado_nps",
                "niveis": [{"min": 70, "pts": 30}, {"min": 63, "pts": 15}, {"min": 50, "pts": 5}],
            },
            {
                "name": "Feedback Negativo (Penalidade)",
                "description": "Notas 1 e 2 são consideradas Feedback negativos.",
                "metric": "% em cima do total de avaliados com nota",
                "meta": "≤10%", "peso": -5, "tipo": "penalidade_taxa",
                "threshold": 10, "cap": None, "extra_peso": -1,
            },
            {"name": "Atendimentos | Ligações Finalizados", "description": "Quantidade total de chats encerrados no mês.", "metric": "Individual de chats encerrados no mês", "meta": 150, "peso": 10, "tipo": "proporcional"},
            {"name": "Instalações e Migrações", "description": "Apenas tickets finalizados (inserção manual).", "metric": "Tickets finalizados", "meta": 10, "peso": 30, "tipo": "proporcional"},
            {"name": "Assiduidade (sem faltas)", "description": "Dias de falta ou atrasos não justificados.", "metric": "Dias de falta ou atraso", "meta": 0, "peso": 35, "tipo": "sim_nao_assiduidade"},
            {"name": "Indicação Comercial", "description": "Leads ou oportunidades geradas pelo suporte para o comercial.", "metric": "Indicações realizadas", "meta": 10, "peso": 50, "tipo": "proporcional"},
            {"name": "Indicação Comercial - Vendida", "description": "Leads gerados pelo suporte que resultaram em vendas.", "metric": "Vendas efetivadas", "meta": 10, "peso": 100, "tipo": "proporcional"},
            {"name": "Updates, Treinamentos e Tarefas (N1 a N3)", "description": "Tarefas no geral do suporte.", "metric": "Tarefas realizadas", "meta": 50, "peso": 50, "tipo": "proporcional", "is_automatic_sum": True},
        ],
        "t2": [
             {"name": "Updates",      "meta": 1, "peso": 1,   "tipo": "proporcional"},
             {"name": "Treinamentos", "meta": 1, "peso": 1,   "tipo": "proporcional"},
             {"name": "Tarefa N1",    "meta": 1, "peso": 2,   "tipo": "proporcional"},
             {"name": "Tarefa N2",    "meta": 1, "peso": 3,   "tipo": "proporcional"},
             {"name": "Tarefa N3",    "meta": 1, "peso": 5,   "tipo": "proporcional"},
             {"name": "Avaliação Média", "meta": "-", "peso": "-", "tipo": "-"},
             {"name": "Mensagens Totais", "meta": "-", "peso": "-", "tipo": "-"},
        ],
        "penalidades_setoriais": [
            {"name": "Ligações Perdidas (Setor)", "description": "Não é individual e sim para o setor.", "metric": "Ligações perdidas pelo grupo no mês", "meta": 0, "peso": -2, "tipo": "penalidade"},
        ],
    },
}

# ── Dynamic Configuration ──────────────

DEPT_MAP = DEFAULT_DEPT_MAP
REASON_MAP = DEFAULT_REASON_MAP
OCCURRENCE_MAP = DEFAULT_OCCURRENCE_MAP
LANG_MAP = DEFAULT_LANG_MAP
AGENTS = {}
KPI_CONFIG = DEFAULT_KPI_CONFIG

# ── Helper functions ──────────────────────────────────────────────────────────

def get_agent_group(agent_name: str | None) -> str:
    if not agent_name:
        return "N/A"
    norm_name = agent_name.strip().strip("'").strip('"').strip()
    
    # Procura pelo nome no novo dicionário AGENTS
    for _, info in AGENTS.items():
        if info["name"] == norm_name:
            return info["group"]
            
    return "OUTROS"

def _to_int(val) -> int | None:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None

def resolve_dept(dept_id) -> str:
    d = _to_int(dept_id)
    return DEPT_MAP.get(d, str(dept_id or "N/A")) if d is not None else str(dept_id or "N/A")

def resolve_reason(dept_id, reason_id) -> str:
    d = _to_int(dept_id)
    if d == 5:
        return "Instalações"
    r = _to_int(reason_id)
    if r is None:
        return "Contato Direto"
    label = REASON_MAP.get(d or 0, {}).get(r)
    return label if label is not None else "Contato Direto"

def resolve_occurrence(dept_id, reason_id, occ_id) -> str:
    d = _to_int(dept_id)
    if d == 5:
        return "Coleta de dados"
    r = _to_int(reason_id)
    o = _to_int(occ_id)
    if d is None or o is None:
        return "Outros"
    reason_occs = OCCURRENCE_MAP.get(d, {}).get(r, {})
    if not reason_occs:
        return "Outros"
    return reason_occs.get(o, "Outros")

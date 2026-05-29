import os

from domain import constants

def get_api_key():
    return os.getenv("MESSAGEBIRD_API_KEY_LIVE") or os.getenv("MESSAGEBIRD_API_KEY_TEST")

def get_workspace_id():
    return os.getenv("MESSAGEBIRD_WORKSPACE_ID_LIVE") or os.getenv("MESSAGEBIRD_WORKSPACE_ID_TEST")

def get_base_url_conversations():
    return os.getenv("MESSAGEBIRD_BASE_URL_CONVERSATIONS", "https://conversations.messagebird.com/v1")

def get_base_url_contacts():
    return os.getenv("MESSAGEBIRD_BASE_URL_CONTACTS", "https://contacts.messagebird.com/v2")

def get_base_url_bird():
    return os.getenv("MESSAGEBIRD_BASE_URL_BIRD", "https://api.bird.com")

HTTP_TIMEOUT = float(os.getenv("MESSAGEBIRD_HTTP_TIMEOUT", "30.0"))

PHRASE_TRIAGEM_HEADER = os.getenv("MESSAGEBIRD_PHRASE_TRIAGEM_HEADER", "=== Dados da Triagem ===")
PHRASE_TICKET_HEADER = os.getenv("MESSAGEBIRD_PHRASE_TICKET_HEADER", "=== Informações Ticket ===")
SOFTWARE_NAMES = os.getenv("MESSAGEBIRD_SOFTWARE_NAMES", "SOFTWARE_A,SOFTWARE_B").split(",")
DB_FILENAME = os.getenv("MESSAGEBIRD_DB_FILENAME", "m_bird.db")

def get_known_agents():
    """Load known agents from loaded business config (constants.AGENTS)."""
    return {bird_id: info["name"] for bird_id, info in constants.AGENTS.items()}

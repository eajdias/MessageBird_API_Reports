import json
import os
from domain import constants

def load_and_configure_business(config_path: str):
    """Carrega configuração de negócio e injeta no Domínio."""
    if not os.path.exists(config_path):
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            custom_config = json.load(f)
            
            # Helper para converter chaves string para int onde necessário
            def _keys_to_int(d):
                if not isinstance(d, dict): return d
                return {int(k) if k.isdigit() else k: _keys_to_int(v) for k, v in d.items()}

            if "DEPT_MAP" in custom_config:
                constants.DEPT_MAP = _keys_to_int(custom_config["DEPT_MAP"])
            if "REASON_MAP" in custom_config:
                constants.REASON_MAP = _keys_to_int(custom_config["REASON_MAP"])
            if "OCCURRENCE_MAP" in custom_config:
                constants.OCCURRENCE_MAP = _keys_to_int(custom_config["OCCURRENCE_MAP"])
            if "LANG_MAP" in custom_config:
                constants.LANG_MAP = _keys_to_int(custom_config["LANG_MAP"])
            if "AGENTS" in custom_config:
                constants.AGENTS = custom_config["AGENTS"]
            if "KPI_CONFIG" in custom_config:
                constants.KPI_CONFIG = custom_config["KPI_CONFIG"]
            if "DEPT_ROUTING" in custom_config:
                constants.DEPT_ROUTING = custom_config["DEPT_ROUTING"]
                
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")

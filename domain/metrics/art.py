from domain.strategies.metrics_strategy import MetricStrategy
from domain.entities.report_data import RawConversationData
from domain import logic, constants

class ARTCalculator(MetricStrategy):
    """
    Calcula o Average Response Time (ART) de uma conversa.
    No contexto desta aplicação, é o tempo de resposta do agente após a interação inicial.
    """
    def calculate(self, data: RawConversationData) -> float:
        # Extraído da lógica original do repositório
        first_resp_dt = None
        for m in data.msgs:
            if m.direction == "sent":
                first_resp_dt = logic.parse_datetime(m.created, apply_offset=True)
                break
        
        q_time = data.queue_time
        start_dt_obj = logic.parse_datetime(q_time, apply_offset=True) if q_time else logic.parse_datetime(data.raw_created, apply_offset=True)
        
        if not first_resp_dt or not start_dt_obj:
            return 0.0
            
        return constants.MetricsCalculator.calculate_frt(start_dt_obj, first_resp_dt) or 0.0

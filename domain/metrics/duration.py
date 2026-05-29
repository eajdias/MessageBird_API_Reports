from domain.strategies.metrics_strategy import MetricStrategy
from domain.entities.report_data import RawConversationData
from domain import logic

class DurationCalculator(MetricStrategy):
    def calculate(self, data: RawConversationData) -> float:
        first_resp_dt = None
        for m in data.msgs:
            if m.direction == "sent":
                first_resp_dt = logic.parse_datetime(m.created, apply_offset=True)
                break
        
        last_msg_dt = None
        if data.msgs:
            last_msg_dt = logic.parse_datetime(data.msgs[-1].created, apply_offset=True)
            
        raw_end = last_msg_dt or logic.parse_datetime(data.raw_updated, apply_offset=True)
        
        if first_resp_dt and raw_end and raw_end >= first_resp_dt:
            return round((raw_end - first_resp_dt).total_seconds() / 60, 2)
        return 0.0

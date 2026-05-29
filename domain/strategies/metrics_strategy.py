from abc import ABC, abstractmethod
from domain.entities.report_data import RawConversationData, ProcessedReportData

class MetricStrategy(ABC):
    @abstractmethod
    def calculate(self, data: RawConversationData) -> float:
        pass

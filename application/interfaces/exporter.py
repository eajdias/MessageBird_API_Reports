from abc import ABC, abstractmethod
from typing import List, Any, Dict
from dataclasses import dataclass

@dataclass
class DashboardDTO:
    title: str
    start_date: str
    end_date: str
    general_metrics: Dict[str, Any]
    nps_distribution: Dict[str, int]
    rating_distribution: Dict[str, int]
    heatmap_data: List[Dict[str, Any]]
    topic_data: List[Dict[str, Any]]
    occurrence_data: List[Dict[str, Any]] = None
    bsc_header: List[str] = None
    bsc_data_t1: List[List[Any]] = None
    bsc_data_t2: List[List[Any]] = None
    bsc_kpi_config: Dict[str, Any] = None
    tabular_header: List[str] = None
    tabular_data: List[List[Any]] = None
    department_data: List[List[Any]] = None
    department_header: List[str] = None
    dow_data: List[Dict[str, Any]] = None
    agent_rating_detail: List[List[Any]] = None
    agent_nps_detail: List[List[Any]] = None
    prev_month_metrics: Dict[str, Any] = None
    monthly_evolution: List[Dict[str, Any]] = None
    report_type: str = "monthly"
    period_label: str = ""

class ReportExporter(ABC):
    @abstractmethod
    def export_excel(self, filename: str, header: List[str], data: List[List[Any]], sheet_name: str = "Relatório", highlight_frt: bool = False):
        pass

    @abstractmethod
    def export_executive_dashboard(self, filename: str, dto: DashboardDTO):
        pass

    @abstractmethod
    def export_agent_detailed(self, filename: str, agent_name: str, header: List[str], data: List[List[Any]]):
        pass

    @abstractmethod
    def export_summary(self, filename: str, title: str, start_date: str, end_date: str, summary_data: Dict[str, Any], report_type: str = "monthly"):
        pass

    @abstractmethod
    def export_annual_dashboard(self, filename: str, dto: DashboardDTO):
        pass

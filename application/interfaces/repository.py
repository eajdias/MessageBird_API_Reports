from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from domain.entities.report_data import RawConversationData

class ReportRepository(ABC):
    @abstractmethod
    async def fetch_raw_data_range(self, start_date: str, end_date: str, agent_group: str = None) -> List[RawConversationData]:
        pass

    @abstractmethod
    async def fetch_auditoria_contatos_raw(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_demanda_raw(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_os_raw(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_contatos_data(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_os_data(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_chats_data(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_demanda_data(self, start_date: str, end_date: str, agent_group: str = None) -> Tuple[List[str], List[Any]]:
        pass

    @abstractmethod
    async def fetch_unmapped_counts(self) -> Tuple[int, int]:
        pass
    
    @abstractmethod
    async def fetch_all_groups(self, start_date: str, end_date: str) -> List[str]:
        pass

    @abstractmethod
    async def fetch_raw_data_all(self, agent_group: str = None) -> List[RawConversationData]:
        pass

    @abstractmethod
    async def fetch_all_groups_all(self) -> List[str]:
        pass

    @abstractmethod
    async def fetch_auditoria_contatos_raw_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def fetch_auditoria_os_raw_all(self) -> List[Dict[str, Any]]:
        pass

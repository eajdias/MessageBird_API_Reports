from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime

@dataclass
class RawMessageData:
    created: str
    direction: str
    agent_id: Optional[str]
    agent_name: Optional[str]

@dataclass
class RawConversationData:
    id: str
    contact: str
    phone: str
    contact_id: int = 0
    start_time: str = ""
    end_time: str = ""
    queue_time: Optional[str] = None
    raw_created: str = ""
    raw_updated: str = ""
    msgs: List[RawMessageData] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    rating: Optional[float] = None
    nps: Optional[float] = None
    dept_label: str = "N/A"
    contact_reason: str = "N/A"
    occurrence: str = "N/A"

@dataclass
class ProcessedReportData:
    conversation_id: str
    agent: str
    contact_id: int = 0
    frt_min: Optional[float] = None
    art_min: Optional[float] = None
    duration_min: Optional[float] = None
    rating: Optional[float] = None
    nps: Optional[float] = None
    dept_label: str = "N/A"
    contact_reason: str = "N/A"
    occurrence: str = "N/A"
    is_compliment: bool = False
    is_negative: bool = False
    msg_count: int = 0
    phone: str = ""
    start_time: str = ""
    end_time: str = ""
    raw_created: str = ""

from datetime import datetime, timedelta, time
from typing import Tuple, Optional, List, Dict, Any

# Business logic for time handling (Canonical)
TIMEZONE_OFFSET = -3

def parse_datetime(dt_string: Optional[str], apply_offset: bool = False) -> Optional[datetime]:
    if not dt_string:
        return None
    try:
        # Try different formats
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"):
            try:
                # Handle ISO-like formats with 'T' and optional fractional seconds
                if "T" in dt_string:
                    clean_str = dt_string.replace("Z", "").split(".")[0]
                    dt = datetime.strptime(clean_str, "%Y-%m-%dT%H:%M:%S")
                else:
                    dt = datetime.strptime(dt_string, fmt)
                
                if apply_offset:
                    dt += timedelta(hours=TIMEZONE_OFFSET)
                return dt.replace(tzinfo=None)
            except ValueError:
                continue
        
        # Last resort for ISO format
        dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        if apply_offset:
            dt += timedelta(hours=TIMEZONE_OFFSET)
        return dt.replace(tzinfo=None)
    except Exception:
        return None

def local_date_bounds(start_date_str: str, end_date_str: str) -> Tuple[datetime, datetime]:
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    return start_dt, end_dt

def to_utc_sqlite_string(dt: datetime) -> str:
    # Convert local to UTC for SQLite storage
    utc_dt = dt - timedelta(hours=TIMEZONE_OFFSET)
    return utc_dt.strftime("%Y-%m-%d %H:%M:%S")

def get_utc_range(start_date: str, end_date: str) -> Tuple[str, str]:
    start_dt, end_dt = local_date_bounds(start_date, end_date)
    return to_utc_sqlite_string(start_dt), to_utc_sqlite_string(end_dt)

def format_local_dt(dt_string: Optional[str]) -> Optional[str]:
    dt = parse_datetime(dt_string, apply_offset=True)
    return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

def calculate_business_duration(start_dt: datetime, end_dt: datetime) -> float:
    """
    Calculate duration in minutes between two datetimes.
    Follows canonical formula: Raw wall-clock time.
    """
    if not start_dt or not end_dt or start_dt >= end_dt:
        return 0.0

    delta = (end_dt - start_dt).total_seconds() / 60.0
    
    # Cap at 480 minutes (8 hours) as per business rules for response times
    if delta > 480:
        return 0.0
        
    return delta

def _get_val(obj, keys, default=None):
    for key in keys:
        if key in obj:
            return obj[key]
    return default

def _get_datetime(obj, keys, apply_offset=True):
    val = _get_val(obj, keys)
    return parse_datetime(val, apply_offset=apply_offset)

def calculate_time_to_first_human(messages: List[Dict[str, Any]]) -> Optional[float]:
    """Calculates minutes from last bot interaction (or ticket start) to first human agent message."""
    # Logic: Find last message before first human message. 
    # If ticket start, use ticket start time.
    # Keep it KISS: First human agent message - First received/bot message
    first_human_dt = None
    last_bot_dt = None
    
    for msg in messages:
        direction = _get_val(msg, ["direction", "msgs_direction"], "")
        created = _get_datetime(msg, ["createdDatetime", "msgs_created"])
        agent_name = _get_val(msg, ["agnt_name", "agent_name"], None)
        
        if not created: continue
        
        is_human = agent_name and not (agent_name.lower() in ["sistema", "bot", "robot"])
        
        if is_human and first_human_dt is None:
            first_human_dt = created
        elif not is_human and first_human_dt is None:
            last_bot_dt = created
            
    if first_human_dt:
        start_dt = last_bot_dt or first_human_dt # Fallback to same time if no bot msg
        return calculate_business_duration(start_dt, first_human_dt)
    return None

def calculate_ticket_duration(created_at: str, updated_at: str) -> float:
    """Calculates minutes from ticket open to ticket close."""
    c_dt = parse_datetime(created_at, apply_offset=True)
    u_dt = parse_datetime(updated_at, apply_offset=True)
    if c_dt and u_dt:
        if c_dt >= u_dt:
            return 0.0
        delta = (u_dt - c_dt).total_seconds() / 60.0
        from domain.constants import MAX_DURATION_MINUTES
        if delta > MAX_DURATION_MINUTES:
            return 0.0
        return delta
    return 0.0

def get_effective_start_time(messages: List[Any], default_start: str) -> str:
    """
    Finds the last customer message before the first agent response.
    Replaces the complex SQL 'queue_time' subquery to ensure Domain verticality.
    """
    first_agent_msg_time = None
    for m in messages:
        # Support both dict (from raw rows) and RawMessageData objects
        direction = getattr(m, 'direction', None) or m.get('msgs_direction', m.get('direction'))
        agent_id = getattr(m, 'agent_id', None) or m.get('msgs_agnt', m.get('agent_id'))
        created = getattr(m, 'created', None) or m.get('msgs_created', m.get('created'))
        
        if direction == "sent" and agent_id is not None:
            first_agent_msg_time = created
            break
            
    if not first_agent_msg_time:
        return default_start
        
    last_customer_msg_time = None
    for m in messages:
        direction = getattr(m, 'direction', None) or m.get('msgs_direction', m.get('direction'))
        created = getattr(m, 'created', None) or m.get('msgs_created', m.get('created'))
        
        if direction == "received" and created <= first_agent_msg_time:
            if not last_customer_msg_time or created > last_customer_msg_time:
                last_customer_msg_time = created
        elif created > first_agent_msg_time:
            break
            
    return last_customer_msg_time or default_start

def calculate_churn_score(last_contact_at: Optional[str]) -> float:
    """
    Business logic for contact churn score.
    Replaces SQL CASE/julianday logic to ensure Domain verticality.
    """
    if not last_contact_at:
        return 0.0
    
    # Bird timestamps are UTC. parse_datetime(..., apply_offset=False) returns naive UTC.
    dt_utc = parse_datetime(last_contact_at, apply_offset=False)
    if not dt_utc:
        return 0.0
    
    from datetime import timezone
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
    days_since = (now_utc - dt_utc).days
    
    if days_since > 60:
        return 1.0
    if days_since > 30:
        return 0.5
    return 0.0


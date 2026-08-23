import datetime
from typing import List

def log_event(logs: List[str], node_name: str, message: str) -> List[str]:
    """Appends a timestamped log entry to the state's audit trail."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] [{node_name.upper()}] {message}"
    updated_logs = list(logs) if logs else []
    updated_logs.append(entry)
    return updated_logs

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class FlowFeatures:
    """
    Lưu trữ thông tin 1 flow mạng từ Suricata
    (Dùng cho IDS / Machine Learning)
    """

    # Network info
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str

    # Time
    start_time: datetime
    end_time: datetime
    duration: float

    # Traffic volume
    src_bytes: int
    dst_bytes: int
    pkts_to_server: int
    pkts_to_client: int

    # TCP flags 
    tcp_flags: str

    # Application layer
    app_proto: str

    # Alert (label)
    alert_info: Optional[Dict] = None

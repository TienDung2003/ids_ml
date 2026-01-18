# core/flow.py
from datetime import datetime

class Flow:
    def __init__(
        self,
        src_ip=None,
        dst_ip=None,
        src_port=None,
        dst_port=None,
        protocol="TCP",
        app_proto=None,
        src_bytes=0,
        dst_bytes=0,
        flow_state=None,
        start_time=None,
        end_time=None
    ):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        self.app_proto = app_proto
        self.src_bytes = src_bytes
        self.dst_bytes = dst_bytes
        self.flow_state = flow_state
        self.start_time = start_time
        self.end_time = end_time or datetime.utcnow()

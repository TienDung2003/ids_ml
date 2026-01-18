# core/eve_to_flow.py
from datetime import datetime
from .flow import Flow

def parse_ts(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", ""))
    except Exception:
        return datetime.utcnow()

def eve_to_flow(event):
    if event.get("event_type") != "flow":
        return None

    flow = event.get("flow", {})

    return Flow(
        src_ip=event.get("src_ip"),
        dst_ip=event.get("dest_ip"),
        src_port=event.get("src_port"),
        dst_port=event.get("dest_port"),
        protocol=event.get("proto", "TCP"),
        app_proto=event.get("app_proto"),
        src_bytes=flow.get("bytes_toserver", 0),
        dst_bytes=flow.get("bytes_toclient", 0),
        flow_state=flow.get("state"),
        start_time=parse_ts(flow.get("start")),
        end_time=parse_ts(event.get("timestamp"))
    )

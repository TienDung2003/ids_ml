import json
from datetime import datetime, timezone
from typing import Optional

from .flow_features import FlowFeatures


def parse_log_line(log_line: str) -> Optional[FlowFeatures]:
    """
    Parse một dòng log từ Suricata eve.json
    Trả về FlowFeatures hoặc None
    """

    try:
        data = json.loads(log_line)

        # Chỉ xử lý flow event
        if data.get("event_type") != "flow":
            return None

        # Timestamp chính
        ts = datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        ).astimezone(timezone.utc)

        # Flow timing
        flow_data = data.get("flow", {})
        start_time = ts
        end_time = ts
        duration = 0.0

        if "start" in flow_data and "end" in flow_data:
            start_time = datetime.fromisoformat(
                flow_data["start"].replace("Z", "+00:00")
            )
            end_time = datetime.fromisoformat(
                flow_data["end"].replace("Z", "+00:00")
            )
            duration = (end_time - start_time).total_seconds()

        # TCP flags (phục vụ ML feature: flag_SF, flag_S0)
        tcp = data.get("tcp", {})

        syn = tcp.get("syn", False)
        ack = tcp.get("ack", False)
        fin = tcp.get("fin", False)
        rst = tcp.get("rst", False)

        # Default: other (REJ, RST, ACK-only, UDP, ICMP...)
        tcp_flags = "OTH"

        # NSL-KDD semantics
        if syn and not ack:
            tcp_flags = "S0"
        elif syn and ack and fin and not rst:
            tcp_flags = "SF"


       


        flow = FlowFeatures(
            src_ip=data.get("src_ip", "0.0.0.0"),
            dst_ip=data.get("dest_ip", "0.0.0.0"),
            src_port=data.get("src_port", 0),
            dst_port=data.get("dest_port", 0),
            protocol=data.get("proto", "UNK"),

            start_time=start_time,
            end_time=end_time,
            duration=duration,

            src_bytes=flow_data.get("bytes_toserver", 0),
            dst_bytes=flow_data.get("bytes_toclient", 0),
            pkts_to_server=flow_data.get("pkts_toserver", 0),
            pkts_to_client=flow_data.get("pkts_toclient", 0),

            tcp_flags= tcp_flags,

            app_proto=data.get("app_proto", ""),
            alert_info=data.get("alert")
        )

        return flow

    except Exception as e:
        print("[Parser error]", e)
        return None

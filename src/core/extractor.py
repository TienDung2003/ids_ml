# core/extractor.py
import time
from .feature_defs import SELECTED_FEATURES

class FeatureExtractor:
    def __init__(self, redis_window):
        self.redis = redis_window

    def extract(self, flow):
        features = {}

        # Duration
        if flow.start_time and flow.end_time:
            features["duration"] = (
                flow.end_time - flow.start_time
            ).total_seconds()
        else:
            features["duration"] = 0.0

        # Bytes
        features["src_bytes"] = flow.src_bytes
        features["dst_bytes"] = flow.dst_bytes

        # Protocol
        features["protocol_type_tcp"] = int(flow.protocol == "TCP")
        features["protocol_type_udp"] = int(flow.protocol == "UDP")
        features["protocol_type_icmp"] = int(flow.protocol == "ICMP")

        # Service
        features["service_http"] = int(flow.app_proto in ["http", "http2"])

        # flag_SF (KDD-style, SUY LUẬN)
        features["flag_SF"] = int(
            flow.protocol == "TCP"
            and flow.flow_state in ["established", "closed"]
            and flow.src_bytes > 0
            and flow.dst_bytes > 0
        )

        # Redis sliding window
        now = time.time()
        self.redis.add_flow(flow)

        host_key = f"host:{flow.dst_ip}"
        service_key = f"service:{flow.dst_ip}:{flow.dst_port}"

        count = self.redis.count(host_key, now)
        srv_count = self.redis.count(service_key, now)

        features["count"] = count
        features["same_srv_rate"] = srv_count / count if count > 0 else 0.0
        features["diff_srv_rate"] = (count - srv_count) / count if count > 0 else 0.0

        return features

# alerts/elastic_alert.py
from datetime import datetime
from elasticsearch import Elasticsearch

class ElasticAlertWriter:
    def __init__(self, host="http://localhost:9200", index="ids-alerts"):
        self.es = Elasticsearch(host)
        self.index = index

    def send(self, flow, pred, score, features):
        doc = {
            "@timestamp": datetime.utcnow().isoformat(),
            "src_ip": flow.src_ip,
            "dst_ip": flow.dst_ip,
            "dst_port": flow.dst_port,
            "protocol": flow.protocol,
            "prediction": pred,
            "confidence": float(score),
            "features": features
        }
        self.es.index(index=self.index, document=doc)

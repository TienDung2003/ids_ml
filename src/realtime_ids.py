# realtime_ids.py
from core.eve_reader import follow_eve
from core.eve_to_flow import eve_to_flow
from core.extractor import FeatureExtractor
from core.vectorizer import FeatureVectorizer
from redis_layer.redis_window import RedisSlidingWindow
from alerts.elastic_alert import ElasticAlertWriter
from ml.load_model import load_model

EVE_PATH = "/var/log/suricata/eve.json"

def main():
    redis_window = RedisSlidingWindow()
    extractor = FeatureExtractor(redis_window)
    vectorizer = FeatureVectorizer()
    model = load_model()

    elastic = ElasticAlertWriter()

    print("[*] IDS realtime started")

    for event in follow_eve(EVE_PATH):
        flow = eve_to_flow(event)
        if not flow:
            continue

        features = extractor.extract(flow)
        vector = vectorizer.vectorize(features)

        pred = model.predict(vector)[0]
        score = model.predict_proba(vector)[0].max()

        if pred == 1 and score > 0.8:
            elastic.send(flow, "attack", score, features)
            print(f"[ALERT] {flow.dst_ip}:{flow.dst_port} score={score:.2f}")

if __name__ == "__main__":
    main()

# redis_layer/redis_window.py
import time
import uuid
import redis

class RedisSlidingWindow:
    def __init__(self, host="localhost", port=6379, window_seconds=2):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)
        self.window = window_seconds

    def add_flow(self, flow):
        ts = time.time()
        fid = str(uuid.uuid4())

        self.r.zadd(f"host:{flow.dst_ip}", {fid: ts})
        self.r.zadd(f"service:{flow.dst_ip}:{flow.dst_port}", {fid: ts})

        self.r.expire(f"host:{flow.dst_ip}", self.window + 1)
        self.r.expire(f"service:{flow.dst_ip}:{flow.dst_port}", self.window + 1)

        return ts

    def count(self, key, now):
        return self.r.zcount(key, now - self.window, now)

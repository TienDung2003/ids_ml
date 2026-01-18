# core/eve_reader.py
import json
import time

def follow_eve(path):
    with open(path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

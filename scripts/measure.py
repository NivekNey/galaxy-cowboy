"""
Similar to apache bench but more flexible
"""
import http.client
import time
from collections import Counter
import signal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("name")


def handler(signum, frame):
    raise Exception("timeout")


if __name__ == "__main__":
    args = parser.parse_args()
    name = args.name
    conn = http.client.HTTPConnection(f"{name}:9001")

    # health

    print("## waiting for health check...")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    while True:
        try:
            conn.request("GET", "/", "")
            res = conn.getresponse()
            res.read()
            if res.status == 200:
                break
        except (ConnectionResetError, ConnectionRefusedError):
            conn = http.client.HTTPConnection(f"{name}:9001")
        time.sleep(1)
    signal.alarm(0)

    # predict x 5

    print("## performing predict...")

    with open("models/req.json") as f:
        payload = f.read()
    headers = {"Content-Type": "application/json"}

    latencies = []
    statuses = []
    for i in range(50000):
        t1 = time.time()
        conn.request("POST", "/predict", payload, headers)
        res = conn.getresponse()
        t2 = time.time()

        # warm up
        if i > 1000:
            latencies.append(t2 - t1)
            statuses.append(res.status)

        # debug
        if i == 10:
            print(f"response={res.read().decode().strip()}")
        else:
            res.read()

    latencies.sort()
    print(f"statuses={dict(Counter(statuses))}")
    p50 = latencies[int(len(latencies) * 0.50)] * 1000
    p99 = latencies[int(len(latencies) * 0.99)] * 1000
    p100 = latencies[-1] * 1000
    print(f"| name | p50 | p99 | p100 |")
    print(f"| --- | --- | --- | --- |")
    print(f"| {name} | {p50:.4f}ms | {p99:.4f}ms | {p100:.4f}ms |")

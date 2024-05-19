import os

from prometheus_client import start_http_server
from collctor import do_collect
import time

port = int(os.getenv("PORT", 9000))
refresh_rate = int(os.getenv("REFRESH_RATE", 10))

if __name__ == "__main__":
    start_http_server(port)
    print(f"Prometheus Exporter has started on port {port}, refresh rate {refresh_rate}s")
    while True:
        do_collect()
        time.sleep(refresh_rate)

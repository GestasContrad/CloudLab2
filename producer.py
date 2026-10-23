import requests
import time
from datetime import datetime

BROKER_URL = "http://127.0.0.1:6000/queue/orders"
order_id = 1

while True:
    message = {
        "order_id": order_id,
        "platform": "Wolt",
        "vendor": "Basilic Aksay",
        "timestamp": datetime.now().isoformat()
    }

    try:
        response = requests.post(BROKER_URL, json=message)
        print(f"[PRODUCER] Sent order {order_id} -> Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[PRODUCER] Broker is down, waiting...")

    order_id += 1
    time.sleep(1.5)
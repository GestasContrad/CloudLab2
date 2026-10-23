import requests
import time

BROKER_URL = "http://127.0.0.1:6000/queue/orders"

while True:
    try:
        response = requests.get(BROKER_URL)

        if response.status_code == 200:
            message = response.json()
            print(f"[CONSUMER] Processing order {message.get('order_id')} from {message.get('vendor')}...")
            time.sleep(3)
            print(f"[CONSUMER] Finished order {message.get('order_id')}")
        elif response.status_code == 204:
            print("[CONSUMER] Queue is empty, waiting...")
            time.sleep(1)

    except requests.exceptions.ConnectionError:
        print("[CONSUMER] Broker is down, waiting...")
        time.sleep(2)
import time
import threading
from datetime import datetime
from app.checker import fetch_availability
from app.config import INTERVAL, PORT
from app.routes import create_app

app = create_app()

# Function to periodically check room availability
def check_availability_periodically():
    while True:
        print(f"Checking availability at {datetime.now()}")
        fetch_availability()
        time.sleep(INTERVAL)

# Start the background thread for periodic checks
availability_thread = threading.Thread(target=check_availability_periodically)
availability_thread.daemon = True
availability_thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)

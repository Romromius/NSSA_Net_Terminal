import threading
import time

def background_task():
    while True:
        print("Background task is running...")
        time.sleep(1)

# Create and start the background thread
background_thread = threading.Thread(target=background_task, daemon=True)
background_thread.start()

# Main thread can do other work or just sleep
print("Main thread is continuing...")
while True:
    # This keeps the main thread alive
    print("Main thread is alive...")
    time.sleep(5)  # Simulate some ongoing work in the main thread

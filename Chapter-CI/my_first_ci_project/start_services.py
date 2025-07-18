#!/usr/bin/env python
import os
import subprocess
import sys
import threading
import time


def run_django():
    """Run Django development server"""
    print("Starting Django server...")
    subprocess.run([
        sys.executable, "manage.py", "runserver", "0.0.0.0:8000"
    ])


def run_websocket():
    """Run WebSocket server"""
    print("Starting WebSocket server...")
    time.sleep(2)  # Wait a bit for Django to start
    subprocess.run([
        sys.executable, "websocket_server.py"
    ])


def main():
    """Start both Django and WebSocket servers"""
    print("Starting both Django and WebSocket servers...")
    
    # Start Django in a separate thread
    django_thread = threading.Thread(target=run_django, daemon=True)
    django_thread.start()
    
    # Start WebSocket server in main thread
    try:
        run_websocket()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)


if __name__ == "__main__":
    main() 
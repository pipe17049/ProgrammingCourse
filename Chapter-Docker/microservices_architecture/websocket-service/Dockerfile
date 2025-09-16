# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir websockets

# Copy WebSocket server
COPY websocket_server.py /app/

# Expose WebSocket port
EXPOSE 8765

# Run the WebSocket service
CMD ["python", "websocket_server.py"] 
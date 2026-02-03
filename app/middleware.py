import time
import logging
from flask import request, g

# 1. Configure the Logger (Records data to a file)
logging.basicConfig(filename='thesis_metrics.log', level=logging.INFO)

def start_timer():
    """Start the stopwatch before the request is processed."""
    g.start = time.time()

def log_request(response):
    """Stop the stopwatch after the response is sent."""
    if hasattr(g, 'start'):
        diff = time.time() - g.start
        process_time_ms = diff * 1000 # Convert to milliseconds
        
        # Log format: [METHOD] Endpoint | Status | Time Taken
        log_message = f"[{request.method}] {request.path} | {response.status_code} | {process_time_ms:.2f}ms"
        
        # Print to terminal (so you can see it)
        print(f"METRIC: {log_message}")
        
        # Save to file (for your Thesis graphs)
        logging.info(log_message)
        
    return response

def setup_metrics(app):
    """Attach this timer to the Flask App."""
    app.before_request(start_timer)
    app.after_request(log_request)
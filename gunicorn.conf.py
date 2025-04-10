import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

workers = 4
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
timeout = 120
worker_class = "gthread"
threads = 2
accesslog = "-"
errorlog = "-"
loglevel = "info"
pythonpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
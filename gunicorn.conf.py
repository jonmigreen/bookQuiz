import os

workers = 4
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"
timeout = 120
worker_class = "gthread"
threads = 2
accesslog = "-"
errorlog = "-"
loglevel = "info" 
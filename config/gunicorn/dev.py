
import multiprocessing

wsgi_app = "project.wsgi:application"
loglevel = "debug"
workers = multiprocessing.cpu_count() + 1
threads = 2
bind = "0.0.0.0:8000"
reload = True
accesslog = errorlog = "/var/log/gunicorn/dev.log"
capture_output = True
daemon = True
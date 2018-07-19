web: env PYTHONPATH=$PYTHONPATH:$PWD newrelic-admin run-program gunicorn projherokureg.wsgi --log-file -
worker: python appherokureg/worker.py

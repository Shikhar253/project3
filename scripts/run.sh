# !/bin/sh
 export FLASK_APP=../app.py
exec flask run --host=0.0.0.0 --port=5000

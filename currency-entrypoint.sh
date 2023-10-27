#!/bin/sh

alembic upgrade heads
#uvicorn main:app --host 0.0.0.0 --port 8000
python3 main.py
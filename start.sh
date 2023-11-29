#!/bin/bash

exec python3 replay_scraper.py &
exec uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80
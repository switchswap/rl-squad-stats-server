#!/bin/bash

echo "[RL-Server] Starting replay scraper"
exec python3 replay_scraper.py &
echo "[RL-Server] Starting server"
exec uvicorn main:app --proxy-headers --host 0.0.0.0 --port 80
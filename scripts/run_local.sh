#!/usr/bin/env bash

set -e
python -m venv sofwareai_env
source sofwareai_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium

export $(cat .env | xargs)
python agent/main.py
#!/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  pip install -r requirements.txt
elif [[ "$OSTYPE" == "darwin"* ]]; then
  pip install -r requirements.txt
else
  pip install -r requirements_win.txt
fi

python app.py
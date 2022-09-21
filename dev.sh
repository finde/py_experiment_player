#!/usr/bin/env bash

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  pip3 install -r requirements.txt
elif [[ "$OSTYPE" == "darwin"* ]]; then
  pip3 install -r requirements.txt
else
  pip3 install -r requirements_win.txt
fi

python3 app.py
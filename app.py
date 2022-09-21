import webbrowser
import asyncio
import socket

from threading import Timer

from hypercorn.config import Config
from hypercorn.asyncio import serve

from server.main import app

config = Config()
config.bind = ["127.0.0.1:8000"]

def open_browser():
    if not config.debug:
        webbrowser.open_new('http://127.0.0.1:8000/')

if __name__ == "__main__":
    host = socket.gethostname()
    print(f"Running SAD Experiments on :: {host}")
    if (host == "Fin-AWare" or host == "Fin3DU.home"):
        config.debug = True
        config.use_reloader = True
    else:
        Timer(1, open_browser).start()
        
    asyncio.run(serve(app, config))
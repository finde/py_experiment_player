from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.requests import Request

from sys import platform

# from server.experiments.sad import experiment
if platform == "win32":
    # Windows...
    import win32gui
    import win32con    

import os

print("===================================================")

# LEGACY
# from server.experiments.sad import router as sad_router
# from server.experiments.val import router as val_router

from server.experiments.generic import Experiment
from server.core.config import settings as config
from server.sensor import test_sensor
# from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=config.PROJECT_NAME
)

# # # Set all CORS enabled origins
# # if settings.BACKEND_CORS_ORIGINS:
# #     app.add_middleware(
# #         CORSMiddleware,
# #         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
# #         allow_credentials=True,
# #         allow_methods=["*"],
# #         allow_headers=["*"],
# #     )

available_experiments = []

def setup_app():
    app.mount("/css", StaticFiles(directory="dist/css"))
    app.mount("/img", StaticFiles(directory="dist/img"))
    app.mount("/js", StaticFiles(directory="dist/js"))
    app.mount("/media", StaticFiles(directory="dist/media"))
    # app.mount("/.*", StaticFiles(directory="dist"))

    for experiment_id in os.listdir("experiments"):
        if experiment_id.startswith("."):
            continue

        experiment = Experiment(experiment_id=experiment_id)
        #setup router
        app.include_router(experiment.get_router(), prefix=f'/experiment/{experiment_id}')

        print(f"Mounting {experiment_id} assets")
        exp_output_dir = f"{config.EXP_ROOT_DIR}/{experiment_id}/{config.EXP_OUTPUT_DIR}"
        exp_assets_dir = f"{config.EXP_ROOT_DIR}/{experiment_id}/{config.EXP_ASSETS_DIR}"
        if not os.path.exists(exp_output_dir):
            os.makedirs(exp_output_dir)
        app.mount(f"/assets/{experiment_id}", StaticFiles(directory=exp_assets_dir))

        available_experiments.append(experiment_id)

@app.get("/experiments_list", response_class=JSONResponse)
async def experiments_list():        
    return JSONResponse(content={
        "experiments": available_experiments
    })

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return config.TEMPLATES.TemplateResponse("index.html", {"request": request})

@app.get("/editor")
async def test_html():
    data = {
        "status": 200
    }
    return JSONResponse(content=data)

@app.get("/test_sensor")
async def test_sensor_api():
    data = {
        "status": 200
    }
    test_sensor()
    return JSONResponse(content=data)

@app.get("/exit")
async def exit_app():
    if platform == "win32":
        handle = win32gui.FindWindow(None, r'Stress and Addiction')
        win32gui.SetForegroundWindow(handle)
        win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)
    return """closing failed"""

# LEGACY CODE
# app.include_router(sad_router, prefix='/experiment/sad')
# app.include_router(val_router, prefix='/experiment/val')

## INIT
setup_app()
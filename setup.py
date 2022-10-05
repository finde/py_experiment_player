import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    # "packages": ["os"], 
    "excludes": ["tkinter"],
    "include_files": ["dist", "experiments"],
    "optimize": 2,
    "silent": True,
    "zip_include_packages":["*"], 
    "zip_exclude_packages":[],
    "includes": ["anyio._backends", "anyio._backends._asyncio"]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(  name = "PyExperimentPlayer",
        version = "1.0",
        description = "PyExperimentPlayer v1.0",
        options = {
            "build_exe": build_exe_options,
        },
        executables = [Executable("app.py", 
            base=base,
            initScript="Console",
            targetName="PyExperimentPlayer",
            icon="dist/favicon.ico"
        )])
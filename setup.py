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
    "zip_exclude_packages":[]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

setup(  name = "SAD",
        version = "8.0",
        description = "Stress and Addiction v8.0",
        options = {
            "build_exe": build_exe_options,
        },
        executables = [Executable("app.py", 
            base=base,
            initScript="Console",
            targetName="Stress_and_Addiction",
            icon="dist/favicon.ico"
        )])
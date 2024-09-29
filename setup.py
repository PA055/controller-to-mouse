# python setup.py build run
from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "zip_include_packages": ["pywin32", "win32gui"],
}

base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="YourAppName",
    version="1.0",
    description="Your application description",

    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],

)
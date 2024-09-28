# python setup.py build run
from cx_Freeze import setup, Executable
setup(
    name="YourAppName",
    version="1.0",

    description="Your application description",

    executables=[Executable("main.py")],

)
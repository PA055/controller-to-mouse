from cx_Freeze import setup, Executable
setup(
    name="YourAppName",
    version="1.0",

    description="Your application description",

    executables=[Executable("test2.py")],

)
#python setup.py build run in cmd and change test2 to fiNal project name to get execultiable made
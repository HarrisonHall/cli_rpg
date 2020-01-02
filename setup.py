import sys



from cx_Freeze import setup, Executable

setup(
    name="CLI RPG DEMO",
    version="0.1",
    description = "You know.",
    options = {
        "build_exe" : {
            "includes" : [
                "modules.Attack",
                "modules.Exist",
                "modules.Item",
                "modules.Person",
                "modules.Player",
                "modules.Room",
                "modules.Thing"
            ]
        }
    },
    executables = [
        Executable("main.py", base="Win32GUI")
    ]
)
    

import sys

from cx_Freeze import setup, Executable

setup(
    name="CLI RPG DEMO",
    version="0.1",
    description = "You know.",
    options = {
        "build_exe" : {
            "includes" : [
            ],
            "include_files": [
                "base/","modules/"
            ],
        }
    },
    executables = [
        Executable("main.py", base="Console")
    ]
)
    

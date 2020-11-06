from pathlib import Path


#: Current version of Liberation.
VERSION = "2.2.0-preview"
if Path("buildnumber").exists():
    with open("buildnumber", "r") as file:
        VERSION += f"-{file.readline()}"

import shutil
from os import chdir, mkdir, getcwd, remove
from os import name as _name
from os.path import isdir
from os.path import join as pjoin
from subprocess import Popen

showNoti     = False
try:
    from pynotifier import Notification
    showNoti = True
except:
    pass

build_tako   = True

# Assuming we are aren't in VSC or something and are running directly from /build_scripts,
# script should run from /src.
if "build_scripts" in getcwd():
    chdir("..")

if build_tako:
    # Build Tako Package
    process = Popen(
        "pyinstaller --onefile main.py --name Tako --icon img/favicon.ico --clean --distpath .",
        shell=True
    )
    process.wait()

    if process.returncode:
        raise Exception("PyInstaller failed to build package: Tako.exe!")

    print("Successfully built package: Tako.exe!")

# Dist folder
destination = pjoin( getcwd(), "dist" )

# Make if not already existing and remove old contents
if isdir(destination):
    shutil.rmtree(pjoin( getcwd(), "dist" ))
    
# Make/remake directory
mkdir(destination)

# Defaults for distribution
defaultDirectories = [
    "datasets",
    "intrinsics",
    "log",
    "resources"
]

# Defaults for files
defaultFiles = [
    "config.json"
]

# Dirs
directories = [
    "css",
    "img",
    "js"
]

# Files
files = [
    "ui.html"
]

# Windows
if 'nt' in _name:
    files.append("Tako.exe")
    files.append("chromedriver.exe")
    icon = "favicon.ico"

# Unix/Mac
else:
    files.append("Tako")
    files.append("chromedriver")
    icon = "tako_panel.png"

processedFiles = []
processedDirs  = []

for name in defaultDirectories:
    full = pjoin(pjoin(getcwd(), "defaults"), name)
    shutil.copytree(full, pjoin(destination, name))
    print(f"Copied default dir {name} to Dist folder.")        

for name in defaultFiles:
    full = pjoin(pjoin(getcwd(), "defaults"), name)
    shutil.copy(full, pjoin(destination, name))
    print(f"Copied default file {name} to Dist folder.")     

for name in files:
    full = pjoin(getcwd(), name)
    shutil.copy(full, pjoin(destination, name))
    print(f"Copied file {name} to Dist folder.")

for name in directories:
    full = pjoin(getcwd(), name)
    shutil.copytree(full, pjoin(destination, name))
    print(f"Copied dir {name} to Dist folder.")

with open('dist/config_location.txt', 'w') as f:
    f.write("config.json")

print("Added config_location.txt with default location of \".\"")

try:
    remove("Tako.spec")
except:
    pass

try:
    remove("Tako.exe")
except:
    pass

try:
    if isdir(pjoin(getcwd(), "build")):
        shutil.rmtree(pjoin(getcwd(), "build"))
except:
    pass

if showNoti:
    Notification(
        title='Tako Package Ready',
        description=f"""
Welcome to Tako!
Your dist build is located @ {pjoin(getcwd(), 'dist')}.
        """,
        icon_path=getcwd() + '/img/' + icon, # On Windows .ico is required, on Linux - .png
        duration=10,                                 
        urgency='critical' # 'low', 'normal', 'critical'
    ).send()

_ = input("\nBuild Complete!\nHIT ENTER TO EXIT")

from json import dump, load

def setJSON(obj, file):
    with open(file, "w+") as f:
        dump(obj, f, indent=4)

def getJSON(file):
    with open(file) as f:
        return load(f)

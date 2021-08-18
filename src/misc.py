from datetime import datetime
from os.path import isfile
from json import dump, load

def setJSON(obj, file):
    with open(file, "w+") as f:
        dump(obj, f, indent=4)

def getJSON(file):
    with open(file) as f:
        return load(f)


def noww(): return str(datetime.now())

def keepRate(kept, total):
    return round(100 * ( float(kept) / float(total) ), 2)

def today():
    now = datetime.now()
    return now.strftime('%A') + ", " + now.strftime("%B") + " " +  str(now.day) + "th, " + now.strftime("%H:%M:%S")

if not isfile("intrinsics/interactions.cache"):
    with open("intrinsics/interactions.cache", "w+") as f:
        pass
else:
    with open("intrinsics/interactions.cache", "r") as fr:
        r = fr.read()
    if (len(r) > 2048):    
        with open("intrinsics/interactions.cache", "w+") as f:
                f.write(r[round(len(r) / 2):len(r)])

def putCache(tweetID):
    with open("intrinsics/interactions.cache", "a") as f:
        f.write(tweetID)

def checkCache(tweetID):
    # Return false if tweet not interacted with yet.
    with open("intrinsics/interactions.cache", "r") as f:
        return tweetID in f.read()    


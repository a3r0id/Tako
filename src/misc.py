
from datetime import datetime
from os.path import isfile

from json_stuff import getJSON

def noww(): return str(datetime.now())

def keepRate(kept, total):
    return round(100 * ( float(kept) / float(total) ), 2)

def today():
    now = datetime.now()
    return now.strftime('%A') + ", " + now.strftime("%B") + " " +  str(now.day) + "th, " + now.strftime("%H:%M:%S")

if not isfile("intrinsics/interactions.cache"):
    with open("intrinsics/interactions.cache", "w+") as f:
        pass

def putCache(tweetID):
    with open("intrinsics/interactions.cache", "a") as f:
        f.write(tweetID)

def checkCache(tweetID):
    # Return false if tweet not interacted with yet.
    with open("intrinsics/interactions.cache", "r") as f:
        return tweetID in f.read()    

def config():
    # COMBINES CONSTRAINTS + CONFIG
    buf         = getJSON("config.json")
    constraints = getJSON("resources/constraints.json")
    for key, value in constraints.items():
        buf[key] = value
    return buf


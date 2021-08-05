from asyncio    import get_event_loop
from time       import sleep
from threading  import Thread
from webbrowser import get as get_webbrowser
from logging    import basicConfig, DEBUG
from os         import getcwd

from server     import start_server
from twitterbot import Bot

basicConfig(filename="log/teko.log", level=DEBUG)

def botDaemon():
    Bot().run()

def browserThreadWorker():
    fileName = getcwd() + "/ui.html"
    """
        sleep(1)
        print("Starting Browser In 5 Seconds...")
        for i in range(5):
            sleep(1)
            print(f"Starting Browser In {int(5 - (i + 1))} Seconds...")
        #get_webbrowser('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open(fileName)  
    """
    print("Tako is live @ " + fileName)

botThread = Thread(target=botDaemon)
botThread.start()

browserThread = Thread(target=browserThreadWorker)
browserThread.start()           

while True:
    get_event_loop().run_until_complete(start_server)
    get_event_loop().run_forever()

# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/analyze-tweet-sentiment-in-python/

# https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits


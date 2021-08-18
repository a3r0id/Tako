###############################
#                             #
#  T A K O  (Dev.) v00.00.02  #
#                             #
###############################

from logging     import basicConfig, DEBUG
from selenium    import webdriver
from asyncio     import get_event_loop
from threading   import Thread
from os          import getcwd
from time        import sleep
from server      import start_server
from twitterbot  import Bot
from scheduleBot import ScheduleBot
from macros      import macros

# START LOGGING
basicConfig(filename="log/teko.log", level=DEBUG)

# CONVENTIONAL BOT THREAD
def botDaemon():
    Bot().run()

# SCHEDULER BOT THREAD
def scheduleBotDaemon():
    ScheduleBot().run()

# NOTE: STREAMBOT THREAD IS STARTED AS NEEDED

# INITIALIZE OUR PSEUDO-NATIVE APP ENVORONMENT
globalWebDriver = None
def browserDaemon():
    global globalWebDriver

    def initBrowser():
        global globalWebDriver

        opt     = webdriver.ChromeOptions()
        webCWD  = getcwd().replace('\\', '/')
        URL     = f"file:///{webCWD}/ui.html"
        # https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/common/chrome_switches.cc
        opt.add_argument("--app=" + URL)
        #opt.add_argument("--force-app-mode")
        opt.add_argument("start-maximized")
        opt.add_argument("--force-enable-night-mode")
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        globalWebDriver  = webdriver.Chrome(options=opt)
        globalWebDriver.get(URL)

    initBrowser()   
     
    while 1:
        try:
            _ = globalWebDriver.window_handles
        except:
            initBrowser()  
        sleep(1)

# INITIALIZE AUTH
macros.Auth.set()

# START THREADS
Thread(target=botDaemon).start()
Thread(target=scheduleBotDaemon).start()
Thread(target=browserDaemon).start()   

print("[Tako] This is the main window and must be closed to stop all Tako processes.")

# START SERVER
while 1:
    get_event_loop().run_until_complete(start_server)
    get_event_loop().run_forever()


### COOL IDEAS ###

# https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/analyze-tweet-sentiment-in-python/

# https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits


###############################
#                             #
#  T A K O  (Dev.) v00.00.8   #
#                             #
###############################

from logging     import basicConfig, DEBUG
from asyncio     import get_event_loop
from threading   import Thread
from os          import getcwd
from time        import sleep
from server      import start_server
from twitterbot  import Bot
from scheduleBot import ScheduleBot
from macros      import macros
from webbrowser  import open_new_tab
from os.path     import join as pjoin
from os          import mkdir

# if /log does not exist, create it
try:
    mkdir("log")
except FileExistsError:
    pass

# START LOGGING
basicConfig(filename="log/tako.log", level=DEBUG)

# CONVENTIONAL BOT THREAD
def botDaemon():
    Bot().run()

# SCHEDULER BOT THREAD
def scheduleBotDaemon():
    ScheduleBot().run()

# NOTE: STREAMBOT THREAD IS STARTED ONLY AS NEEDED

# OPEN BROWSER
def browserDaemon():
    sleep(1)
    open_new_tab(f"file://{pjoin(getcwd(), 'ui.html')}")

# INITIALIZE AUTH
macros.Auth.set()

# START THREADS
Thread(target=botDaemon).start()
Thread(target=scheduleBotDaemon).start()
Thread(target=browserDaemon).start()   

print("[Tako] This is the main window and must be closed to stop all Tako processes.")

# START SERVER
get_event_loop().run_until_complete(start_server)
get_event_loop().run_forever()





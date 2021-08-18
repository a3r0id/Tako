from  time import  sleep
from tweepy import StreamListener, Stream
from macros import macros
from threading import Thread
from json import loads, dumps
# TODO
# ADD CUSTOM RESPONSES TO BEING @'ed!

# CLASS OUR STREAM LISTENER
class MyStreamListener(StreamListener):

    """    def on_delete(self, status_id, user_id):
    print("DELETE")
    print(status_id)
    print(user_id)
    return"""

    def on_event(self, status):
        print("EVENT")
        print(status)
        return

    def on_direct_message(self, status):
        print("NEW DIRECT MESSAGE!")
        print(status)
        return

    def on_friends(self, friends):
        print("FRIENDS")
        print(friends)
        return

    def on_connect(self):
        print("CONNECT")
        macros.Que.log("[Stream] Established & listening...")
        return

    def on_limit(self, track):
        print("LIMIT")
        macros.Que.log(f"<span style=\"color: red;\">[Stream Limit Reached] Track: {str(track)}</span>")
        return

    def on_timeout(self):
        print("TIMEOUT")
        macros.Stream.running = False
        macros.Que.log(f"[Stream] Stream timeout!")
        return

    def on_disconnect(self, notice):
        print("DISCONNECT")
        macros.Stream.running = False
        macros.Que.log(f"[Stream] Stream disconnected by Twitter... Notice: {notice}")
        return False
        
    def on_warning(self, notice):
        print("WARNING")
        macros.Que.log(f"[Stream] Stream will disconnected by Twitter... Warning: {notice}")
        return

    def on_exception(self, exception):
        macros.Que.log(f"<span style=\"color: red;\">[Stream Error] Unhandled Exception: {str(exception)}</span>")
        macros.Que.log("[Stream] Killing Stream...")
        macros.Stream.currentStream = None
        macros.Stream.running = False
        macros.Que.log(f"[Stream] Stream encountered an unhandled exception... Exception: {exception}")
        return False  
    
    # ON STATUS - SEEMS TO NOT WORK WHEN OnData IS DEFINED AS WELL
    def on_status(self, status):
        print("STATUS")
        print(status)
        return

    # ON ERROR - KILLS STREAM
    def on_error(self, status_code):
        print("ERROR")
        macros.Que.log(f"<span style=\"color: red;\">[Stream Error] Status Code: {status_code}</span>")
        macros.Que.log("[Stream] Killing Stream...")
        macros.Stream.currentStream = None
        macros.Stream.running = False
        #returning False in on_error disconnects the stream
        return False     

    # ON DATA
    def on_data(self, event):

        if not macros.Stream.running:
            del macros.Stream.currentStream
            macros.Stream.currentStream = None
            macros.Que.log("[Stream] Killing Stream...")
            #returning False in on_data disconnects the stream
            return False  

        ### PROCESS THE STATUS ###
        event = loads(event)

        macros.Que.log(dumps({
            "streamEvent": event
        }))

        # > Delete Event
        if ('delete' in event):
            macros.Que.log("[Stream] User [ID: %s] just deleted status %s..." % ( event['delete']['status']['user_id_str'],  event['delete']['status']['id_str'],))
            return

        # > Conventional Tweet Event
        if ('user' in event and 'in_reply_to_user_id_str' in event):

            # Get user-object
            user = event['user']

            # This ensures it's not a reply but an actual status
            if event['in_reply_to_user_id_str'] != None:
                return

            # This ensures it's not a reply to their tweet from someone else
            if user['screen_name'] not in macros.Stream.get():
                return 

            # Do the damn thang
            if macros.Config.get()["interaction-rt"]:
                try:
                    macros.Auth.api.retweet(event['id'])  
                    macros.retweets   += 1  
                    macros.totalPulls += 1
                    macros.Que.log("Retweeted a Tweet from stream by @%s" % user['screen_name'])
                except Exception as e:
                    macros.Que.log(f"<span style=\"color: red;\">[Stream Error] {str(e)}</span>")

            # Do the damn thang, again
            if macros.Config.get()["interaction-like"]:
                try:
                    macros.Auth.api.create_favorite(event['id'])  
                    macros.likes      += 1
                    macros.totalPulls += 1
                    macros.Que.log("Liked a Tweet from stream by @%s" % user['screen_name'])
                except Exception as e:
                    macros.Que.log(f"<span style=\"color: red;\">[Stream Error] {str(e)}</span>")
        return

class Streamer(object):
    # https://github.com/tweepy/tweepy/blob/78d2883a922fa5232e8cdfab0c272c24b8ce37c4/tweepy/streaming.py
    def __init__(self):
        super().__init__()
        self.listener  = MyStreamListener()
        
    def __del__(self):
        macros.Stream.currentStream = None
        macros.Que.log("[Stream (__del__)] Killing Stream...")
        macros.Que.Alerts.alert("Killing Stream...")

        # Redundancy
        macros.Stream.running = False

    def run(self):
    
        macros.Stream.currentStream = Stream(auth = macros.Auth.api.auth, listener=self.listener)
        macros.Stream.running = True
        macros.Que.Alerts.alert("Starting Stream...")
        macros.Que.log("[Stream (__init__)] Starting Stream...")
        follow = [t for t in [macros.Auth.api.get_user(user).id_str for user in macros.Stream.get()] if type(t) == str]
        macros.Stream.currentStream.filter(follow=follow)


# Starts stream and hangs thread until stream stop is motioned to delete the object then proceeds to jump out of thread using `return`
def startStream():
    macros.Stream.currentStream = Streamer()
    macros.Stream.currentStream.run()
    while 1:
        if (not macros.Stream.running):
            del macros.Stream.currentStream
            macros.Stream.currentStream = None
            return
        sleep(1)

# Spawn the stream per users socket request
def spawnStreamThread():
    macros.Stream.start = False
    Thread(target=startStream).start()

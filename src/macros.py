from datetime import datetime
from misc import getJSON, setJSON
from validation import Config
from tweepy import OAuthHandler, API

# MAIN MACROS
class macros:

    # CHECKS FOR CONFIG FILE AND SOME BASIC VALIDATIONS
    configLocation  = Config.check()

    botLoopStarted  = False
    isQueryRunning  = False
    isRunning       = False
    stopBot         = False
    streamIsRunning = False
    stopStream      = False
    followers       = 0
    retweets        = 0
    likes           = 0
    follows         = 0
    acks            = 0
    totalPulls      = 0
    efficiencyAvg   = 0.00
    
    class Que:

        logsToSend = []

        def log(log):
            macros.Que.logsToSend.append(log)

        class add:
            hashTags  = []
            dropWords = []

        class remove:
            hashTags  = []
            dropWords = []

        class user:
            unfollow = []
            follow   = []
            block    = []

        class Data:
            data     = []
        
        class Alerts:
            alerts   = []

            def alert(message):
                macros.Que.Alerts.alerts.append(message)


    class HashTags:

        hashtags = getJSON("resources/hashtags.json")

        @staticmethod
        def get():
            return getJSON("resources/hashtags.json")

        def toString():
            return " OR ".join(macros.HashTags.get())
        
        def remove(hashTag):
            if not hashTag.startswith("#"):
                hashTag = '#' + hashTag
            setJSON([h for h in getJSON("resources/hashtags.json") if h.lower() != hashTag.lower()], "resources/hashtags.json")

        def add(hashTag):
            hashTags = getJSON("resources/hashtags.json")
            if not hashTag.startswith("#"):
                hashTag = '#' + hashTag
            if hashTag not in hashTags:
                hashTags.append(hashTag)
            setJSON(hashTags, "resources/hashtags.json")
    
    class DropPhrases:

        dropPhrases = getJSON("resources/dropPhrases.json")

        @staticmethod
        def get():
            return getJSON("resources/dropPhrases.json")

        def remove(dropPhrase):
            setJSON([h for h in getJSON("resources/dropPhrases.json") if h.lower() != dropPhrase.lower()], "resources/dropPhrases.json")

        def add(dropPhrase):
            dropPhrases = getJSON("resources/dropPhrases.json")
            if dropPhrase not in dropPhrases:
                dropPhrases.append(dropPhrase)
            setJSON(dropPhrases, "resources/dropPhrases.json")

    
    class DropHashtagIfIncludes:

        dropHashtagIfIncludes = getJSON("resources/dropHashtagIfIncludes.json")

        @staticmethod
        def get():
            return getJSON("resources/dropHashtagIfIncludes.json") 

        def remove(dropPhrase):
            setJSON([h for h in getJSON("resources/dropHashtagIfIncludes.json") if h.lower() != dropPhrase.lower()], "resources/dropHashtagIfIncludes.json")

        def add(dropPhrase):
            dropPhrases = getJSON("resources/dropHashtagIfIncludes.json")
            if dropPhrase not in dropPhrases:
                dropPhrases.append(dropPhrase)
            setJSON(dropPhrases, "resources/dropHashtagIfIncludes.json")


    class DataSets:


        class Efficiency:

            @staticmethod
            def get():
                return getJSON("datasets/efficiency.json")

            @staticmethod
            def add(data):
                buff = getJSON("datasets/efficiency.json")
                buff.append([str(datetime.now()), data])
                if len(buff) > macros.Config.get()['max_dataset_length']:
                    buff.pop(0)
                setJSON(buff, "datasets/efficiency.json")


        class LikeAndRetweets:
        
            @staticmethod
            def get():
                return getJSON("datasets/likes&retweets.json")

            @staticmethod
            def add(likes, retweets):
                buff = getJSON("datasets/likes&retweets.json")
                buff.append([str(datetime.now()), {"likes": likes, "retweets": retweets}])
                if len(buff) > macros.Config.get()['max_dataset_length']:
                    buff.pop(0)
                setJSON(buff, "datasets/likes&retweets.json")


        class Followers:
        
            @staticmethod
            def get():
                return getJSON("datasets/followers.json")

            @staticmethod
            def add(data):
                buff = getJSON("datasets/followers.json")
                buff.append([str(datetime.now()), data])
                if len(buff) > macros.Config.get()['max_dataset_length']:
                    buff.pop(0)
                setJSON(buff, "datasets/followers.json")

        class TotalPulls:
            
            @staticmethod
            def get():
                return getJSON("datasets/totalPulls.json")

            @staticmethod
            def add(data):
                buff = getJSON("datasets/totalPulls.json")
                buff.append([str(datetime.now()), data])
                if len(buff) > macros.Config.get()['max_dataset_length']:
                    buff.pop(0)
                setJSON(buff, "datasets/totalPulls.json")
        
    class Constraints:
        @staticmethod
        def get():
            return getJSON("resources/constraints.json")

        selectors = [
                ["max_dataset_length", int],
                ["interval_time_seconds", int],
                ["required_retweets", int],
                ["required_favorites", int],
                ["query_amount", int],
                ["max_hashtags", int],
                ["interaction-like", bool],
                ["interaction-rt", bool],
                ["interaction-follow", bool]
            ]

        def set(key, value):
            for i in macros.Constraints.selectors:
                if i[0] == key:
                    constraints = macros.Constraints.get()
                    constraints[key] = i[1](value)
                    setJSON(constraints, "resources/constraints.json")

    class MyTweets:

        @staticmethod
        def get():
            return getJSON("resources/scheduledTweets.json") 
                
        @staticmethod
        def add(data):
            b = getJSON("resources/scheduledTweets.json")
            b.append(data)
            setJSON(b, "resources/scheduledTweets.json")

        @staticmethod
        def remove(index):
            buff = getJSON("resources/scheduledTweets.json")
            del buff[index]
            setJSON(buff, "resources/scheduledTweets.json")

    class Stream:
        start         = False
        running       = False
        currentStream = None
    
        @staticmethod
        def get():
            return getJSON("resources/streamFollowing.json") 
                
        @staticmethod
        def add(data):
            b = getJSON("resources/streamFollowing.json")
            b.append(data)
            setJSON(b, "resources/streamFollowing.json")

        @staticmethod
        def remove(handle):
            buff = getJSON("resources/streamFollowing.json")
            buff = [i for i in buff if i != handle]
            setJSON(buff, "resources/streamFollowing.json")


    class Config:

        @staticmethod        
        def get():
            # COMBINES CONSTRAINTS + CONFIG
            buf         = getJSON(macros.configLocation)
            constraints = getJSON("resources/constraints.json")
            
            # MERGE BOTH JSON FILES
            for key, value in constraints.items():
                buf[key] = value

            return buf

    class Auth:

        auth = None
        api  = None

        @staticmethod
        def set():
            macros.Auth.auth        = OAuthHandler(macros.Config.get()['consumer'], macros.Config.get()['consumer_secret'])
            macros.Auth.auth.set_access_token(macros.Config.get()['token'], macros.Config.get()['token_secret'])
            macros.Auth.auth.secure = True
            macros.Auth.api         = API(macros.Auth.auth)    
            macros.Me.update()
            macros.Que.Alerts.alert("Authenticated To Twitter Successfully!")  

        @staticmethod
        def unset():
            macros.Auth.auth        = None
            macros.Auth.api         = None   

    class Me:

        me = None

        def update():
            macros.Me.me = macros.Auth.api.me()
            macros.followers = macros.Me.me.followers_count
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "me",
                    "json": macros.Me.me._json
                }
            })







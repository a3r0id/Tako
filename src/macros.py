from datetime import datetime

from json_stuff import getJSON, setJSON
from misc import config

# MAIN MACROS
class macros:

    botLoopStarted = False
    isQueryRunning = False
    isRunning      = False
    stopBot        = False
    followers      = 0
    retweets       = 0
    likes          = 0
    acks           = 0
    totalPulls     = 0
    efficiencyAvg  = 0.00
    
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
                if len(buff) > config()['max_dataset_length']:
                    buff = buff[ :config()['max_dataset_length'] ]
                setJSON(buff, "datasets/efficiency.json")


        class LikeAndRetweets:
        
            @staticmethod
            def get():
                return getJSON("datasets/likes&retweets.json")

            @staticmethod
            def add(likes, retweets):
                buff = getJSON("datasets/likes&retweets.json")
                buff.append([str(datetime.now()), {"likes": likes, "retweets": retweets}])
                if len(buff) > config()['max_dataset_length']:
                    buff = buff[ :config()['max_dataset_length'] ]
                setJSON(buff, "datasets/likes&retweets.json")


        class Followers:
        
            @staticmethod
            def get():
                return getJSON("datasets/followers.json")

            @staticmethod
            def add(data):
                buff = getJSON("datasets/followers.json")
                buff.append([str(datetime.now()), data])
                if len(buff) > config()['max_dataset_length']:
                    buff = buff[ :config()['max_dataset_length'] ]
                setJSON(buff, "datasets/followers.json")



        class TotalPulls:
            
            @staticmethod
            def get():
                return getJSON("datasets/totalPulls.json")

            @staticmethod
            def add(data):
                buff = getJSON("datasets/totalPulls.json")
                buff.append([str(datetime.now()), data])
                if len(buff) > config()['max_dataset_length']:
                    buff = buff[ :config()['max_dataset_length'] ]
                setJSON(buff, "datasets/totalPulls.json")
        
    class Constraints:
        selectors = [
                ["max_dataset_length", int],
                ["interval_time_seconds", int],
                ["required_retweets", int],
                ["required_favorites", int],
                ["query_amount", int]
            ]
        def set(key, value):

            configBuffer = config()
            buf = {}
            for k in macros.Constraints.selectors:
                buf[k[0]] = configBuffer[k[0]]
            buf[key] = k[1](value)
            setJSON(buf, "resources/constraints.json")
                


import tweepy
from time import sleep
from dateutil import parser
from datetime import datetime, timedelta

from macros import macros
from misc import checkCache, putCache, keepRate, config
from json_stuff import getJSON

"""
        try:
            myTweet = glb.myTweets.pop(0)
            glb.myTweetIndex += 1
            try:
                self.api.update_status(myTweet)
                print("Tweeted status #" + str(glb.myTweetIndex))
            except Exception as f:
                print(">>> [ERROR] Failed to Tweet! " + str(f))
                glb.errs += 1
                glb.errlist.append(str(f))
                print(f">>> [TWEETED]: \"{myTweet}\"")
        except IndexError:
            print(">>>[NOT TWEETING] - You have no new tweets to post!")
   
"""
  
class Bot:
    def __init__(self):

        self.auth = None

    # Authenticate to Twitter
    def setAuth(self):

        consumer        = config()['consumer']
        consumer_secret = config()['consumer_secret']
        token           = config()['token']
        token_secret    = config()['token_secret']

        self.auth = tweepy.OAuthHandler(consumer, consumer_secret)
        self.auth.set_access_token(token, token_secret)
        self.api = tweepy.API(self.auth)

        macros.Que.log("Authenticated To Twitter Successfully!")

    # Run Bot
    def run(self):
        
        #Update Auth
        self.setAuth()

        while True:
     
            ## STOP BOT [Possiblility #1]
            if (macros.stopBot == True or macros.isRunning == False):
                macros.stopBot   = False
                macros.isRunning = False
                continue

            if (not self.auth):
                macros.Que.log("[Error] Auth was not created!")
                return
            
            macros.Que.log("[Session] Starting Next Query!")
            
            macros.isQueryRunning = True
            
            for tweet in tweepy.Cursor(self.api.search, q=(macros.HashTags.toString() + ' -filter:retweets'), lang='en').items(config()['query_amount']):
                
                ## STOP BOT [Possiblility #2]
                if (macros.stopBot == True or macros.isRunning == False):
                    macros.stopBot   = False
                    macros.isRunning = False
                    continue

                # Increment totalPulls macro
                macros.totalPulls += 1

                # Check for dropworthy hashtags
                doDrop = False
                for hashtag in tweet.entities['hashtags']:
                    for drop in macros.DropHashtagIfIncludes.get():
                        if drop.lower() in hashtag['text'].lower():
                            doDrop = True

                # Check for overall bad keywords
                for item in macros.DropPhrases.get():
                    if (item.lower() in tweet.text.lower()):
                        doDrop = True

                if checkCache(str(tweet.id)):
                    doDrop = True

                if tweet.retweet_count < config()['required_retweets']:       
                    doDrop = True

                if tweet.favorite_count < config()['required_favorites']:       
                    doDrop = True

                if not doDrop:
                    putCache(str(tweet.id))
                    tweet.retweet()
                    macros.totalPulls += 1
                    macros.retweets   += 1
                    tweet.favorite()
                    macros.totalPulls += 1
                    macros.likes      += 1

            ### POST-QUERY STATS/REVIEW ###########

            # Determine efficiency ratio
            if (macros.totalPulls):
                macros.efficiencyAvg = float(keepRate(macros.retweets, macros.totalPulls))

            # Check ourself once a query
            me = self.api.get_user(config()['myHandle'])
            macros.followers = me.followers_count
            macros.totalPulls += 1


            # NOTE STATS:
            macros.DataSets.LikeAndRetweets.add(macros.likes, macros.retweets)
            macros.DataSets.Efficiency.add(macros.efficiencyAvg)
            macros.DataSets.TotalPulls.add(macros.totalPulls)
            macros.DataSets.Followers.add(macros.followers)

            # Todo: Monitor totalPulls within a 24hr period!

            
            # SEND STATS         
            macros.Que.log(
                f'[Eff: {str(macros.efficiencyAvg)}%] [Total: {macros.totalPulls}] [Retweeted: {macros.retweets}] [Liked: {macros.likes}]'
                )

            lr = macros.DataSets.LikeAndRetweets.get()
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "likesAndRetweets",
                    "x": [i[0] for i in lr],
                    "likes": [i['likes'] for i in [i[1] for i in lr] ],
                    "retweets": [i['retweets'] for i in [i[1] for i in lr] ]
                }
            })

            d = macros.DataSets.Efficiency.get()
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "dropRate",
                    "x": [i[0] for i in d],
                    "y": [i[1] for i in d]
                }
            })

            f = macros.DataSets.Followers.get()
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "followers",
                    "x": [i[0] for i in f],
                    "y": [i[1] for i in f]
                }
            })

            t = macros.DataSets.TotalPulls.get()
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "totalPulls",
                    "x": [i[0] for i in t],
                    "y": [i[1] for i in t]
                }
            })
            
            tt = macros.DataSets.TotalPulls.get()
            now = datetime.now()
            pullsBuffer = []
            for x, y in zip([i[0] for i in tt], [i[1] for i in tt]):
                then = parser.parse(x)
                if now - timedelta(hours=24) <= then <= now + timedelta(hours=24):
                    pullsBuffer.append([x, y])
            macros.Que.Data.data.append({
                "action": "dataUpdate",
                "data": {
                    "type": "totalPulls24",
                    "x": [i[0] for i in pullsBuffer],
                    "y": [i[1] for i in pullsBuffer],
                    "amount": sum([i[1] for i in pullsBuffer])
                }
            })
            ### END - POST-QUERY STATS/REVIEW ###########

            macros.isQueryRunning = False
            macros.Que.log("Sleeping for %s seconds." % config()['interval_time_seconds'])

        
            # IDLE BUT ALLOW UNIVERSAL STOP BETWEEN SECONDS
            for _ in range(config()['interval_time_seconds']):
                
                ## STOP BOT [Possiblility #3]
                if (macros.stopBot == True or macros.isRunning == False):
                    macros.stopBot   = False
                    macros.isRunning = False
                    continue
                
                sleep(1)
                        


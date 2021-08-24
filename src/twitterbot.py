
import tweepy
from time import sleep
from dateutil import parser
from datetime import datetime, timedelta

from macros import macros
from misc import checkCache, putCache, keepRate

class Bot(object):
    def __init__(self):
        self.auth = None

    # Run Bot
    def run(self):

        while True:
     
            ## STOP BOT [Possiblility #1]
            if (macros.stopBot == True or macros.isRunning == False):
                macros.stopBot   = False
                macros.isRunning = False
                sleep(1)
                continue

            macros.Que.log("[Session] Starting Next Query!")
            
            macros.isQueryRunning = True
            
            for tweet in tweepy.Cursor(macros.Auth.api.search, q=(macros.HashTags.toString() + ' -filter:retweets'), lang='en').items(macros.Config.get()['query_amount']):
                
                ## STOP BOT [Possiblility #2]
                if (macros.stopBot == True or macros.isRunning == False):
                    macros.stopBot   = False
                    macros.isRunning = False
                    continue

                # Increment totalPulls macro
                macros.totalPulls += 1

                # Check for dropworthy hashtags
                tags = 0
                doDrop = False
                for hashtag in tweet.entities['hashtags']:
                    
                    for drop in macros.DropHashtagIfIncludes.get():
                        if drop.lower() in hashtag['text'].lower():
                            doDrop = True
                    tags += 1

                # CHECK FOR TOO MANY HASHTAGS
                if tags >= macros.Config.get()['max_hashtags']:
                    doDrop = True


                # Check for overall bad keywords
                for item in macros.DropPhrases.get():
                    if (item.lower() in tweet.text.lower()):
                        doDrop = True

                #Check cache to see if we have already interacted with this tweet.
                if checkCache(str(tweet.id)):
                    doDrop = True

                # Check rt amount
                if tweet.retweet_count < macros.Config.get()['required_retweets']:       
                    doDrop = True

                # Check fav amount
                if tweet.favorite_count < macros.Config.get()['required_favorites']:       
                    doDrop = True

                # If tweet qualifies, interact with it.
                if not doDrop:
                    
                    putCache(str(tweet.id))

                    if macros.Config.get()["interaction-like"]:
                        tweet.favorite()
                        macros.totalPulls += 1
                        macros.likes      += 1

                    if macros.Config.get()["interaction-rt"]:
                        tweet.retweet()
                        macros.totalPulls += 1
                        macros.retweets   += 1

                    if macros.Config.get()["interaction-follow"]:
                        macros.Auth.api.create_friendship(tweet.user.id)  
                        macros.totalPulls += 1
                        macros.follows    += 1  


            ### POST-QUERY STATS/REVIEW ###########

            # Determine efficiency ratio
            if (macros.totalPulls):
                macros.efficiencyAvg = float(keepRate(macros.retweets, macros.totalPulls))

            # Check ourself once a query
            macros.Me.update()
            macros.totalPulls += 1


            # NOTE STATS:
            macros.DataSets.LikeAndRetweets.add(macros.likes, macros.retweets)
            macros.DataSets.Efficiency.add(macros.efficiencyAvg)
            macros.DataSets.TotalPulls.add(macros.totalPulls)
            macros.DataSets.Followers.add(macros.followers)

            
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
                    "y": [i[1] for i in t],
                    "amount": [i[1] for i in t][len([i[1] for i in t]) - 1]
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
                    "amount": [i[1] for i in pullsBuffer][len([i[1] for i in pullsBuffer]) - 1]
                }
            })
            ### END - POST-QUERY STATS/REVIEW ###########

            macros.isQueryRunning = False
            macros.Que.log("Sleeping for %s seconds." % macros.Config.get()['interval_time_seconds'])

        
            # IDLE BUT ALLOW UNIVERSAL STOP BETWEEN SECONDS
            for _ in range(macros.Config.get()['interval_time_seconds']):
                
                ## STOP BOT [Possiblility #3]
                if (macros.stopBot == True or macros.isRunning == False):
                    macros.stopBot   = False
                    macros.isRunning = False
                    continue
                
                sleep(1)
                        


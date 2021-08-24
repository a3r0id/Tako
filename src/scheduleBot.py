from misc import setJSON
from macros import macros

from datetime import datetime
from time import sleep

class ScheduleBot(object):
    def __init__(self):
        self.auth = None

    # Run Bot
    def run(self):

        while 1:

            try:
                tweets = macros.MyTweets.get()
            except:
                # Failsafe to empty JSON array if JSON read fails 
                setJSON([], "resources/scheduledTweets.json")
                continue

            # Get any tweets that need to be posted.
            myTweets = [tweet for tweet in tweets if datetime.strptime(tweet['time'], '%b %d %Y  %I:%M%p') < datetime.now()]
            
            # Overwrite the old resource with the posts we just sent off, removed.
            keepTweets = [tweet for tweet in tweets if tweet['time'] not in [t['time'] for t in myTweets] and tweet['tweet'] not in [t['tweet'] for t in myTweets]]

            if keepTweets is not None:
                setJSON(keepTweets, "resources/scheduledTweets.json")

            del keepTweets, tweets

            # Tweet the tweet/s
            for tweet in myTweets:
                macros.Auth.api.update_status(tweet['tweet'])
                macros.totalPulls += 1
                macros.Que.log(f"[Scheduled Tweets] Tweeted a Tweet! (~{tweet['time']})")

            del myTweets

            sleep(1)



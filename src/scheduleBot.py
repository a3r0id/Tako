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

            # Get any tweets that need to be posted.
            myTweets = [tweet for tweet in macros.MyTweets.get() if datetime.strptime(tweet['time'], '%b %d %Y  %I:%M%p') < datetime.now()]
            
            # Overwrite the old resource with the posts we just sent off, removed.
            keepTweets = [tweet for tweet in macros.MyTweets.get() if tweet['time'] not in [t['time'] for t in myTweets] and tweet['tweet'] not in [t['tweet'] for t in myTweets]]
            setJSON(keepTweets, "resources/scheduledTweets.json")
            del keepTweets

            # Tweet the tweet/s
            for tweet in myTweets:
                macros.Auth.api.update_status(tweet['tweet'])
                macros.totalPulls += 1
                macros.Que.log(f"[Scheduled Tweets] Tweeted a Tweet! (~{tweet['time']})")

            sleep(1)



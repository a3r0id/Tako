from json_stuff import getJSON, setJSON

class myTweets:
    def getTweets():
        schedule = getJSON("resources/scheduledTweets.json")
        for tweet in schedule:
            pass
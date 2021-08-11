# Tako (Alpha Release)
  The beginning of a legacy... Tako is a Twitter bot that selectively retweets/favorites based on Twitter content that the bot finds useful. You can currate Tako's behavior and constraints from a comfortable user-interface that live right in your browser, thanks Tako's websocket server! This is just an alpha release as there are still many bugs and I have many big plans for future Tako releases including but not limited to: stream listeners, sentiment analysis, tweet sheduling and much more!

![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/tako_panel.png)

# Install & Run Tako

> Apply for and receive [Twitter API credentials](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). 

> Extract Tako to a comfortable location on your intended device.

> Install Pip Requirements `pip install -r requirements.txt`

> Add your intended credentials to `config.json`.

> Run `main.py`.

> As instructed by `main.py`, double-click `ui.html` to open the user interface.

> Simply navigate to `Control` then hit `Start`.

> Confirm that Tako is running from the `Status` section next to `Bot:` is should read `"Running"`.

### (Image) Connected to server and bot running:
![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/delete1.png)

### (Image) Bot Control
![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/delete.png)




# Editing Your Bot

## Bot Resources:

> __Hashtags__: The hashtags you add here will determine the Tweets your bot will interact with.

> __Drop If Hashtag Includes__: Tako will ignore any Tweet that inludes any of these phrases in any of it's hashtags. (Keeps us from interacting with junk like #100daysofcode etc.). Should ALWAYS be lowercase as each hashtag will be searched in lowercase.

> __Drop If Tweet Includes__: Tako will ignore any Tweet that inludes any of these phrases within it's text. (Keeps us from interacting with junk like "check out my onlyfans + 100DaysOfCode + drug shop on the darknet" etc...). Should ALWAYS be lowercase as each tweet will be searched in lowercase.
Issue: Twitter API only includes some of the text of a tweet in API requests, larger tweets may be truncated so this feature is not completely reliable.

### (Image) Editing Bot Resources
![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/delete2.png)

## Bot Constraints:

> __Max Dataset Length__: This is the maximum amount of datapoints to keep in our dataset files. This is where our anaytics come from and are stored. If you arent concerned about performance/storage issues (ie: arent on a slow device) then you can use a higher cap.

> __Sleep Time__: Amount of time (seconds) to sleep between querys.

> __Required Retweets__: Amount of retweets a Tweet must have in order for us to interact with it.

> __Required Likes__: Amount of likes a Tweet must have in order for us to interact with it.

> __Tweets Per Query__: Amount of Tweets to pull during each query, requests can add up quickly so be sure not to set this too high else you could be rate-limited.

### (Image) Editing Bot Constraints
![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/delete3.png)


## Analytics:
![](https://github.com/hostinfodev/cdn/blob/main/img/delete5.png?raw=true)


## Known Issues:

> Sometimes you need to double-click `Start`, I am working on a fix for this.

> Once bot is started, Ack ping goes to `1`, this should not be happening...

> Darkmode is not perfect.









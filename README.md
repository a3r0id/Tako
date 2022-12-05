# Tako
Tako is a Twitter bot that selectively retweets/favorites based on Twitter content that the bot finds useful. You can curate Tako's behavior and constraints from a comfortable user-interface that runs right in your browser.

![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/tako_panel.png)

![](https://raw.githubusercontent.com/hostinfodev/cdn/main/img/tako_main.png)


# Features

> ### Query Bot
__Query Bot__ is a conventional Twitter Retweet/Like bot that uses hashtags to search for related Tweets then interacts with them. This is a proven method to build a steady following.

> ### Stream Bot
__Stream Bot__ will follow specific users and interact with their Tweets upon being posted. This is good for interacting with an influencer or your favorite people on Twitter.

> ### Tweet Scheduler
__Tweet Scheduler__ will post your Tweets at a scheduled time in the future. As long as Tako is running, the Tweet will be posted otherwise it will be posted next time Tako is started.

> ### Analytics
Tako features some basic analytics which give some insight into Tako's effectiveness and performance.


# Initial Steps

> Apply for and receive [Twitter API credentials](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). 

> Clone Tako to a comfortable location on your intended runtime device.

> Rename `EXAMPLE_config.json` to `config.json`.

> Update your config (`config.json`) with your valid Twitter API credentials. (Read & write permissions)

> Move to `/src` and pip install `requirements.txt`.

> Run `main.py`.

# Tako Basic Usage

> To start either of the bot features (query/stream) navigate to `Control` then hit `Start`.

> Confirm that Tako is running from the `Status` section, it should read `"Running"`.

### (Image) Bot Control
![](https://github.com/hostinfodev/cdn/blob/main/img/tako_control.png?raw=true)

# Editing Your Bot

## Bot Resources:

> __Hashtags__: The hashtags you add here will determine the Tweets your bot will interact with.

> __Drop If Hashtag Includes__: Tako will ignore any Tweet that includes any of these substrings in any of it's hashtags. (Keeps us from interacting with junk like #100daysofcode etc.). Should ALWAYS be lowercase as each hashtag will be searched in lowercase.

> __Drop If Tweet Includes__: Tako will ignore any Tweet that includes any of these substrings within it's text. This keeps us from interacting with junk tweets. Substrings should ALWAYS be lowercase as each tweet will be searched in lowercase.
Issue: Twitter API only includes *some* of the text of a tweet in API requests, larger tweets may be truncated so this feature is not completely reliable.

### (Image) Editing Bot Resources
![](https://github.com/hostinfodev/cdn/blob/main/img/tako_resources_hashtags.png?raw=true)

## Bot Constraints:

> __Max Dataset Length__: This is the maximum amount of data points to keep in our dataset files. This is where our analytics come from and are stored. If you arent concerned about performance/storage issues (ie: aren't on a slow device) then you can use a higher cap.

> __Sleep Time__: Amount of time (seconds) to sleep between queries.

> __Required Retweets__: Amount of retweets a Tweet must have in order for us to interact with it.

> __Required Likes__: Amount of likes a Tweet must have in order for us to interact with it.

> __Tweets Per Query__: Amount of Tweets to pull during each query, requests can add up quickly so be sure not to set this too high else you could be rate-limited.

> __Max Hashtags__: Max amount of hashtags contained in a single Tweet before we deem it spam and ignore it. 

### (Image) Editing Bot Constraints
![](https://github.com/hostinfodev/cdn/blob/main/img/tako_constraints.png?raw=true)


## Analytics:
![](https://github.com/hostinfodev/cdn/blob/main/img/tako_analytics_followers.png?raw=true)

![](https://github.com/hostinfodev/cdn/blob/main/img/tako_analytics_eff.png?raw=true)

> Also featuring analytics of your actions such as likes, requests and retweets.


# How Tako Works

> Tako is built around [Tweepy](https://www.tweepy.org/) and is presented with a clean, browser-based & user-friendly UI.

> Tako uses a local websocket server/client to pass data to and from the backend. 

## Known Issues:

> Darkmode is disabled until I can make the time to fix it.

## Changelog:

#### v00.00.8x

> Added Discord webhook support for stream listener. Forward tweets real-time to a Discord channel.

> Resolved all known errors.

> Removed dependency of chrome-driver for app mode (kiosk mode), Tako now automatically opens in your default browser. 

> Removed config_location.txt, `config.json` is expected to be located in the root folder in any case.

> Various UI changes.

#### v00.00.2x

> __Follow__ is now an interaction option, allowing Tako users to automatically follow the author of Tweets interacted with.

> Updated font.

> `macros.Auth` is now used globally. This saves requests by authenticating at startup instead of each query. Stream, Scheduler & Query Bot now share the same Oauth instance.

> Screenshot:
![](https://github.com/hostinfodev/cdn/blob/main/img/tako_00_00_22.png?raw=true)














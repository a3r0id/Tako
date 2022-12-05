from requests import post
def sendDiscordWebhook(url, message):
    return post(url, data={
        "content": message
    })
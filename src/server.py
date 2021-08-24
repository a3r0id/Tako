from stream import spawnStreamThread
import websockets
from json import dumps, loads
from macros import macros

async def server(websocket, path): 

    # RESPOND AFTER SOCKET REGISTERED
    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "HashTags",
            "data": macros.HashTags.get()
        }
    }))

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "DropPhrases",
            "data": macros.DropPhrases.get()
        }
    }))

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "dropHashtagIfIncludes",
            "data": macros.DropHashtagIfIncludes.get()
        }
    }))

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "constraints",
            "data": {
                "max_dataset_length": macros.Config.get()['max_dataset_length'],
                "interval_time_seconds": macros.Config.get()['interval_time_seconds'],
                "required_retweets": macros.Config.get()['required_retweets'],
                "required_favorites": macros.Config.get()['required_favorites'],
                "query_amount": macros.Config.get()['query_amount'],
                "max_hashtags": macros.Config.get()['max_hashtags'],
                "interaction-like": macros.Config.get()['interaction-like'],
                "interaction-rt": macros.Config.get()['interaction-rt'],
                "interaction-follow": macros.Config.get()['interaction-follow']
            }
        }
    }))

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "myTweets",
            "data": macros.MyTweets.get()
        }
    }))    

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "interactions",
            "like": macros.Config.get()['interaction-like'],
            "rt":   macros.Config.get()['interaction-rt'],
            "follow":   macros.Config.get()['interaction-follow']
        }
    }))       

    await websocket.send(dumps({
        "action": "dataUpdate",
        "data": {
            "type": "streamFollowing",
            "data": macros.Stream.get()
        }
    }))    

    # MESSAGE LOOP
    async for message in websocket:

        message = loads(message)

        # CHECK FOR QUES

        if len(macros.Que.logsToSend):
            for log in macros.Que.logsToSend:
                await websocket.send(dumps({
                    "action": "logging",
                    "data": log
                }))
        # Reset Logs Que
        macros.Que.logsToSend = []

        if len(macros.Que.Data.data):
            for d in macros.Que.Data.data:
                await websocket.send(dumps(d))
        # Reset Data Que
        macros.Que.Data.data = []

        if len(macros.Que.Alerts.alerts):
            for m in macros.Que.Alerts.alerts:
                await websocket.send(dumps({
                    "action": "alert",
                    "data": m,
                    "mode": "info"
                }))
        # Reset Logs Que
        macros.Que.Alerts.alerts = []
            
        # Process Action
        if 'action' in message:

            # START BOT
            if message['action'] == "start_bot":
                macros.isRunning = True
                macros.stopBot   = False

            # STOP BOT
            if message['action'] == "stop_bot":
                macros.isRunning = False
                macros.stopBot   = True

            # ACKS
            if message['action'] == "ack":
                macros.acks += 1
                await websocket.send(dumps({
                    "action": "ack",
                    "data": {
                        "id": message['id'],
                        "data": macros.acks,
                        "isRunning": macros.isRunning,
                        "isStreamRunning": macros.Stream.running,
                        "likes": macros.likes,
                        "retweets": macros.retweets,
                        "efficiencyAvg": macros.efficiencyAvg,
                        "totalPulls": macros.totalPulls
                    }
                }))

            if message['action'] == "set":

                if message['setter'] == "dropHashtagIfincludes":
                    macros.DropHashtagIfIncludes.add(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "dropHashtagIfIncludes",
                            "data": macros.DropHashtagIfIncludes.get()
                        }
                    }))
                
                if message['setter'].lower() == "dropphrase":
                    macros.DropPhrases.add(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "DropPhrases",
                            "data": macros.DropPhrases.get()
                        }
                    }))

                if message['setter'] == "hashtag":
                    macros.HashTags.add(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "HashTags",
                            "data": macros.HashTags.get()
                        }
                    }))

                if message['setter'] in [i[0] for i in macros.Constraints.selectors]:
                    macros.Constraints.set(message['setter'], message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))

                if message['setter'] == "myTweets":
                    p = loads(message['value'])
                    macros.MyTweets.add(p)

                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))                    

                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "myTweets",
                            "data": macros.MyTweets.get()
                        }
                    }))    

                if message['setter'] == "streamFollowing":
                    macros.Stream.add(message['value'])
                    
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
                    }))   

                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "streamFollowing",
                            "data": macros.Stream.get()
                        }
                    }))   


            if message['action'] == "remove":
    
                if message['deleter'] == "dropHashtagIfincludes":
                    macros.DropHashtagIfIncludes.remove(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Removed!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "dropHashtagIfIncludes",
                            "data": macros.DropHashtagIfIncludes.get()
                        }
                    }))

                if message['deleter'] == "dropPhrase":
                    macros.DropPhrases.remove(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Removed!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "DropPhrases",
                            "data": macros.DropPhrases.get()
                        }
                    }))                    


                if message['deleter'] == "hashtag":
                    macros.HashTags.remove(message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Removed!"
                    }))
                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "HashTags",
                            "data": macros.HashTags.get()
                        }
                    }))     

                if message['deleter'] == "myTweets":

                    macros.MyTweets.remove(int(message['value']))

                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Removed!"
                    }))  

                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "myTweets",
                            "data": macros.MyTweets.get()
                        }
                    }))     

                if message['deleter'] == "streamFollowing":

                    macros.Stream.remove(message['value'])

                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Removed!"
                    }))  

                    await websocket.send(dumps({
                        "action": "dataUpdate",
                        "data": {
                            "type": "streamFollowing",
                            "data": macros.Stream.get()
                        }
                    }))                      

            # START STREAM BOT
            if message['action'] == "startStream":
                if not macros.Stream.running:
                    spawnStreamThread()
                    
            # STOP STREAM BOT
            if message['action'] == "stopStream":
                del macros.Stream.currentStream
                macros.Stream.currentStream = None
                macros.Que.log("[Stream] Killing Stream...")
                macros.Stream.running = False      

            if message['action'] == "reAuth":
                macros.Auth.set() 
                macros.Que.log("[Auth] Re-Auth to Twitter API was succesfull!")
                macros.Que.Alerts.alert("[Auth] Re-Auth to Twitter API was succesfull!")
                
                                

# Create server object
start_server = websockets.serve(
    server,
    macros.Config.get()['server_adapter'],
    macros.Config.get()['server_port'],
    max_size=macros.Config.get()['server_max_buffer'],
    ping_timeout=None
    )


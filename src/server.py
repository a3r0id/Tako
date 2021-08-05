import websockets
from json import dumps, loads

from misc import config
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
                "max_dataset_length": config()['max_dataset_length'],
                "interval_time_seconds": config()['interval_time_seconds'],
                "required_retweets": config()['required_retweets'],
                "required_favorites": config()['required_favorites'],
                "query_amount": config()['query_amount'],
            }
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

        if len(macros.Que.logsToSend):
            for log in macros.Que.logsToSend:
                await websocket.send(dumps({
                    "action": "alert",
                    "data": message
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
                        "likes": macros.likes,
                        "retweets": macros.retweets,
                        "efficiencyAvg": macros.efficiencyAvg,
                        "totalPulls": macros.totalPulls
                    }
                }))

                """
                {
                    action: "set",
                    setter: "dropHashtagIfIncludes",
                    value: "100daysofcode"
                }
                """
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
                    print("Added " + message['value'])
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

                """
                {
                    action: "remove",
                    setter: "dropHashtagIfIncludes",
                    value: "100daysofcode"
                }
                """

                if message['setter'] in [i[0] for i in macros.Constraints.selectors]:
                    macros.Constraints.set(message['setter'], message['value'])
                    await websocket.send(dumps({
                        "action": "alert",
                        "data": "Value Set!"
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

                
                
                                

# Create server object
start_server = websockets.serve(
    server,
    "127.0.0.1",
    8401,
    max_size=9000000,
    ping_timeout=None
    )


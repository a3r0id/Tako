window.sock = new WebSocket("ws://127.0.0.1:8401");

sock.onmessage = (event) => {
    let incoming = JSON.parse(event.data);
    incomingHandlers[incoming.action](incoming.data);
    if ('action' in incoming){
        if (incoming.action != "ack"){
            window.SocketLog.log(event.data, mode="Received");
        }
    }
}

sock.onopen = (event) =>{
    $("#server-status").html("<span class=\"w3-green\">CONNECTED</span>");
    window.notify("Welcome!", mode="info")
    ackLoop();
}

sock.onerror = (event) =>{
    window.notify("Error: Websocket Closed!", mode="error");
    $("#server-status").html("<span class=\"w3-red\">ERROR</span>");
}

sock.onclose = (event) =>{
    window.notify("Websocket Closed", mode="error");
    $("#server-status").html("<span class=\"w3-red\">DISCONNECTED</span>");
}






window.SocketLog = {
    logs: [],
    log: (message, mode="Sent") =>
    {
        if (mode == "Sent"){
            mode = "<span class=\"fa fa-upload\"></span>"
        } else if (mode == "Received"){
            mode = "<span class=\"fa fa-download\"></span>"
        }
        let id = "";
        for (var i = 0; i < 10;i++){
            id += Math.floor(Math.random() * 100).toString()
        }
        // message, id, datetime
        let d = new Date();
        let datetime = d.toString();
        let ms = d.getMilliseconds();
        let dtString = datetime.split(" ")[4] + `:${ms} `;// + datetime.split(" ")[1] + " " + datetime.split(" ")[2] + " "
        window.SocketLog.logs.push([message, id, datetime])
        if (window.SocketLog.logs.length > 200){
            let deleter = window.SocketLog.logs.shift();
            $('#' + deleter[1]).remove();
        }
        $("#socket-log").append(`
        <div id="${id}">
          <span style="font-size: small;">${mode} @ ${dtString}</span>
          <div id="textarea-${id}" style="width: 100%;height: 100%;"></div>
        </div>
        `)
        setTimeout(() => {
            $('#textarea-' + id).empty().simpleJson({ jsonObject: JSON.parse(message) });
        }, 100)
    }
}



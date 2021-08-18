
var acks = {};

const makeId = () => {
    return (Math.random() * 210 / 36).toString().split('.')[1]
}

const ackLoop = () => {
    setTimeout(()=>{
        let id = makeId()
        sock.send(JSON.stringify({action: "ack", id: id}))
        let timeNow = new Date();
        acks[id] = {
            t: timeNow,
            ping: () => {
                return new Date().getTime() - acks[id].t.getTime()
            }
        }
        ackLoop();
    }, 1000); 
};


window.ackHandler = (data) =>
{
    
    let thisAckListener = acks[data.id];
    let pingMS = thisAckListener.ping();
    delete acks[data.id];

    //window.pingIndicator(pingMS);

    macros.acks          = data.data;
    macros.likes         = data.likes;
    macros.retweets      = data.retweets;
    macros.efficiencyAvg = data.efficiencyAvg;
    macros.totalPulls    = data.totalPulls;
    
    if (data.isRunning){
        $('#bot-status').html("<span class=\"w3-green\">RUNNING</span>")
    }
    else{
        $('#bot-status').html("<span class=\"w3-yellow\">NOT RUNNING</span>")
    }

    if (data.isStreamRunning){
        $('#stream-status').html("<span class=\"w3-green\">RUNNING</span>")
    }
    else{
        $('#stream-status').html("<span class=\"w3-yellow\">NOT RUNNING</span>")
    }

    

    let symbol = "-";
    let dif    = 0;
    if (pingMS > macros.lastPing){
        dif    = pingMS - macros.lastPing;
        symbol = `<span style=\"color: red;\">+${dif}</span>`
    }
    else if (pingMS < macros.lastPing){
        
        dif    = macros.lastPing - pingMS;
        symbol = `<span style=\"color: green;\">-${dif}</span>`
    }
    if (dif == 0){
        symbol = "<span>~0</span>"
    } 

    $("#server-ping").html(`${pingMS}MS (${symbol})`);

    $('#bot-likes').text(macros.likes);
    $('#bot-rts').text(macros.retweets);
    $('#bot-pulls').text(macros.totalPulls);
    $('#bot-efficiency-avg').text(`${macros.efficiencyAvg}%`);

    macros.lastPing = pingMS;
}
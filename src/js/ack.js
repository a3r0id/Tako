
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

    window.pingIndicator(pingMS);

    stats.acks          = data.data;
    stats.likes         = data.likes;
    stats.retweets      = data.retweets;
    stats.efficiencyAvg = data.efficiencyAvg;
    stats.totalPulls    = data.totalPulls;
    
    if (data.isRunning){
        $('#bot-status').html("<span class=\"w3-green\">RUNNING</span>")
    }
    else{
        $('#bot-status').html("<span class=\"w3-yellow\">IDLE</span>")
    }

    $('#bot-likes').text(stats.likes);
    $('#bot-rts').text(stats.retweets);
    $('#bot-pulls').text(stats.totalPulls);
    $('#bot-efficiency-avg').text(`${stats.efficiencyAvg}%`);
}

// QUERY BOT CONTROL
$('#botStop').on('click', () => {
    let message = JSON.stringify({
        action: "stop_bot"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Stopping bot...")
});

$('#botStart').on('click', () => {
    let message = JSON.stringify({
        action: "start_bot"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Starting bot...")
});

$('#botRestart').on('click', () => {
    let message = JSON.stringify({
        action: "stop_bot"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Stopping bot...")
    setTimeout(()=>{
        window.notify("Bot restarted...")
        let tmessage = JSON.stringify({
            action: "start_bot"
        });
        window.sock.send(tmessage)
        window.SocketLog.log(tmessage);
    }, 1000)
});


// STREAMING BOT CONTROL
$('#streamStop').on('click', () => {
    let message = JSON.stringify({
        action: "stopStream"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Stopping stream...")
});

$('#streamStart').on('click', () => {
    if (macros.streamRunning){
        window.notify("Stream already running...")
        return;
    }
    let message = JSON.stringify({
        action: "startStream"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Starting stream...")
});

$('#streamRestart').on('click', () => {
    let message = JSON.stringify({
        action: "stopStream"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Stopping stream...")
    setTimeout(()=>{
        if (macros.streamRunning){
            return;
        }
        window.notify("Stream restarted...")
        let tmessage = JSON.stringify({
            action: "startStream"
        });
        window.sock.send(tmessage);
        window.SocketLog.log(tmessage);
    }, 1000)
});

$('#edit-toggle').on('click', (e) => {
    $('.w3-modal').hide();
    $('#editor-anchor').html("");
    $('#edit-modal').show();
})

$('#constraints-toggle').on('click', (e) => {
    $('.w3-modal').hide();
    $('#constraints-anchor').html("");
    $('#constraints-modal').show()
})


window.updateInteractions = () => {
    if (macros.interactions_like){
        $('#interaction-like').prop( "checked", true );
    }
    else
    {
        $('#interaction-like').prop( "checked", false );
    }
    if (macros.interactions_rt){
        $('#interaction-rt').prop( "checked", true );
    }
    else
    {
        $('#interaction-rt').prop( "checked", false );
    }
};

$('#interaction-like').on('input', (e) => 
{
    if ($('#interaction-like').is(':checked')){
        macros.interactions_like = true
    }
    else{
        macros.interactions_like = false
    }  
    let message = JSON.stringify(
        {
            action: "set",
            setter: "interaction-like",
            value: macros.interactions_like
        }
    );
    window.sock.send(message);
    window.SocketLog.log(message);
})

$('#interaction-rt').on('change', (e) => {
    if ($('#interaction-rt').is(':checked')){
        macros.interactions_rt = true
    }
    else{
        macros.interactions_rt = false
    }  
    let message = JSON.stringify(
        {
            action: "set",
            setter: "interaction-rt",
            value: macros.interactions_rt
        }
    );
    window.sock.send(message);
    window.SocketLog.log(message);
})


$('#interactions-toggle').on('click', (e) => {
    $('.w3-modal').hide();
    $('#interactions-modal').show();
})

$('#shutdown').on('click', (e) => {
    let message = JSON.stringify({
        action: "full_shutdown"
    });
    window.sock.send(message);
    window.SocketLog.log(message);
    window.notify("Shutdown complete, goodbye!")
})

let panelToggles = [
    ['control-panel-toggle', 'control-panel', ()=>{}, ()=>{}],
    ['logging-panel-toggle', 'logging-panel', ()=>{}, ()=>{
        // Resize table on show - DOESNT WORK - TODO
        window.logTable.columns.adjust().draw();
    }],
    ['settings-toggle', 'settings', ()=>{}, ()=>{}],
    ['tweet-scheduler-toggle', 'tweet-scheduler',  ()=>{}, ()=>{}],
    ['stream-toggle', 'stream',  ()=>{}, ()=>{}],
    ['diagnostics-toggle', 'diagnostics-modal',  ()=>{}, ()=>{}]
];

const buildPanelToggles = (elements) => {

    for (let item of elements)
    {
        $(`#${item[0]}`).on('click', ()=>
        {
            if ($(`#${item[1]}`).is(':visible')){
                $(`#${item[1]}`).hide()
                item[2]()
            }
            else
            {
                $(`#${item[1]}`).show();
                item[3]()
            }
        })
    }
}

$(".w3-modal").on('click', (e) => {
    let pt2 = panelToggles.map(x => x[1]);
    if (pt2.includes(e.target.id)){
        onModalClose();
        $('#' + e.target.id).hide()
    }
})

buildPanelToggles(panelToggles);

const navViews = [
    "home",
    "control-panel-toggle",
    "logging-panel-toggle",
    "settings-toggle",
    "tweet-scheduler-toggle",
    "stream-toggle",
    "diagnostics-toggle"
];

$(".nav-tog").on('click', (e) => {
    for (let t of navViews){
        $("#" + t).removeClass('w3-blue');
    }
    $("#" + e.target.id).addClass("w3-blue");
})

let onModalClose = () => {
    $('.w3-modal').hide();
    for (let t of navViews){
        $("#" + t).removeClass('w3-blue');
    }
    $("#home").addClass("w3-blue");
};

$('#download-socket-logs').on('click', () => {
    let data = JSON.stringify(window.SocketLog.logs, null, 2);
    let href = "text/plain;charset=utf-8," + encodeURIComponent(data); 
    let element = document.createElement('a');
    element.setAttribute('href', `data: ${href}`);
    element.setAttribute('download', "tako_socket_log.json");
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
})


$('#reAuth').on('click', () => 
{

    // Stops conventional bot
    let m1 = JSON.stringify({
        action: "stop_bot"
    });

    window.sock.send(m1);
    window.SocketLog.log(m1);
    window.notify("Stopping bot...")

    // Stops StreamBot
    let m2 = JSON.stringify({
        action: "stopStream"
    });

    window.sock.send(m2);
    window.SocketLog.log(m2);
    window.notify("Stopping stream...")

    // Motions for re-authentication
    let m3 = JSON.stringify({
        action: "reAuth"
    });
    window.sock.send(m3);
    window.SocketLog.log(m3);
    window.notify("Re-authenticated to Twitter API.");

})
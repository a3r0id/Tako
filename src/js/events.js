$('#botStop').on('click', () => {
    window.sock.send(JSON.stringify({
        action: "stop_bot"
    }))
    window.notify("Stopping bot...")
});

$('#botStart').on('click', () => {
    window.sock.send(JSON.stringify({
        action: "start_bot"
    }))
    window.notify("Starting bot...")
});

$('#botRestart').on('click', () => {
    window.sock.send(JSON.stringify({
        action: "stop_bot"
    }))
    window.notify("Stopping bot...")
    setTimeout(()=>{
        window.notify("Bot restarted...")
        window.sock.send(JSON.stringify({
            action: "start_bot"
        }))
    }, 1000)
});


$('#edit-toggle').on('click', (e) => {
    if ($('#edit-modal').is(':visible')){
        $('#edit-modal').hide();
    }
    else{
        $('#editor-anchor').html("");
        $('#edit-modal').show()
    }
})

$('#constraints-toggle').on('click', (e) => {
    if ($('#constraints-modal').is(':visible')){
        $('#constraints-modal').hide();
    }
    else{
        $('#constraints-anchor').html("");
        $('#constraints-modal').show()
    }
})

$('#shutdown').on('click', (e) => {
    window.sock.send(JSON.stringify({
        action: "full_shutdown"
    }))
    window.notify("Shutdown complete, goodbye!")
})

let panelToggles = [
    ['status-panel-toggle', 'status-panel', ()=>{}, ()=>{}],
    ['actions-panel-toggle', 'actions-panel', ()=>{}, ()=>{}],
    ['control-panel-toggle', 'control-panel', ()=>{}, ()=>{}],
    ['logging-panel-toggle', 'logging-panel', ()=>{}, ()=>{
        // Resize table on show - DOESNT WORK - TODO
        window.logTable.columns.adjust().draw();
    }],
    ['settings-toggle', 'settings', ()=>{}, ()=>{}],
    ['analytics-performance-toggle', 'analytics-performance', ()=>{}, ()=>{}],
    ['analytics-interaction-toggle', 'analytics-interaction', ()=>{}, ()=>{}],
    ['analytics-usage-toggle', 'analytics-usage', ()=>{}, ()=>{}],
];

const buildPanelToggles = (elements) => {

    for (let item of elements)
    {
        $(`#${item[0]}`).on('click', ()=>
        {
            if ($(`#${item[1]}`).is(':visible')){
                $(`#${item[1]}`).hide()
                $(`#${item[0]}`).text("+");
                item[2]()
            }
            else
            {
                $(`#${item[1]}`).show();
                $(`#${item[0]}`).text("—");
                item[3]()
            }
        })
    }
}

buildPanelToggles(panelToggles);
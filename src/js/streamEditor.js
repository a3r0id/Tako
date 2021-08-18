window.StreamEditor = {
    updateStream: () => {
        $('#streamHandlesBlock').html("")
        let i = 0;
        for (let stat of macros.streamFollowing){
            $('#streamHandlesBlock').append(`
            <div class="w3-bar-item">
                <button onclick="window.StreamEditor.remove('${stat}')" class="w3-red w3-button">
                ✕</button><span>${stat}</span>
            </div>
            `);
            i++;
        }
    },
    add: (handle) => {
        let message = JSON.stringify({
            action: "set",
            setter: "streamFollowing",
            value: handle

        });
        window.sock.send(message);
        window.SocketLog.log(message);
    }, 
    remove: (handle) => {
        let message = JSON.stringify({
            action: "remove",
            deleter: "streamFollowing",
            value: handle

        });
        window.sock.send(message);
        window.SocketLog.log(message);
    }
}

$('#setStreamFollowing').on('click', () => {
    let val = $('#streamHandleInput').val();
    if (val.length < 3){
        window.notify("Invalid Twitter handle!", mode="error")
        return;
    }
    window.StreamEditor.add(val);
})


window.tweetScheduler = 
{
    add: (json) => {
        let message = JSON.stringify(
            {
                action: "set",
                setter: "myTweets",
                value: JSON.stringify(json)
            }
        );
        window.sock.send(message);
        window.SocketLog.log(message);
    },
    remove: (index) => {
        let message = JSON.stringify(
            {
                action: "remove",
                deleter: "myTweets",
                value: index
            }
        );
        window.sock.send(message);
        window.SocketLog.log(message);
    }
}


window.buildTweetScheduler = () => {
    let widget = $('#tweet-scheduler-widget');
    let buffer = "<div class=\"w3-container\"> <h3 class=\"main-font\">My Tweets</h3> <table> ";
    let index  = 0;
    for (let tweet of macros.myTweets){
        buffer += `
        <tr class="main-font">
            <td>
            <button id="myTweetDelete${index}" class="w3-button w3-red">✕</button> <span>Scheduled for ${tweet.time}</span>
            <td>
        </tr>
        <tr class="main-font">
            <td>
                <div class="w3-input">${tweet.tweet}</div>
            </td>
        </tr>
        `
        index++;
    }

    widget.html(buffer + "</table></div>");

    widget.append(`
    <div style="width: 100%;height: 30px;"></div>
    
    <div class="w3-container">
        
        <h3 class="main-font">Add A Tweet</h3>

        <div class="w3-bar">
            <div class="w3-bar-item">
                <button class="w3-button w3-green main-font" id="addToMyTweets">Save</button>
            </div>
            <div class="w3-bar-item">
                <input type="text" id="myTimePickerTweets" class="w3-button w3-blue main-font" style="color:white;" placeholder="Select Time">
            </div>
        </div>

        <div class="w3-container main-font">
            <div style="width: 100%;height: 25px;"></div>
            <textarea id="myTweetText">Hello World!</textarea>
        </div>

    </div>
    <div style="width: 100%;height: 10px;"></div>`);

    for (let index in macros.myTweets){
        setTimeout(()=>{
            $(`#myTweetDelete${index}`).on('click', (e)=>{
                window.tweetScheduler.remove(index)
            });
        }, 500)
    }

    setTimeout(()=>{

        $('#addToMyTweets').on('click', (e)=>{
            if ($('#myTimePickerTweets').val().length < 4){
                window.notify("Invalid Date!", mode="error");
                return;
            }
            window.tweetScheduler.add({time: $('#myTimePickerTweets').val(), tweet: $('#myTweetText').val()})
        });
    
        $("#myTimePickerTweets").flatpickr({
            enableTime: true,
            dateFormat: "M d Y  H:iK",
        });

    }, 500)


  
}
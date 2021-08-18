
let constraintSelectors = [
    // [selector, isInt, [int, range]]
    ["max_dataset_length", true, [25, 1000]],
    ["interval_time_seconds", true, [10, 500]],
    ["required_retweets", true, [0, 10000000]],
    ["required_favorites", true, [0, 10000000]],
    ["query_amount", true, [1, 500]],
    ["max_hashtags", true, [1, 100]]
];

for (let selector of constraintSelectors)
{
    $('#set-' + selector[0]).on('click', (e)=>
    {
        let value = $('#' + selector[0]).val();
        if (selector[1]){
            if (parseInt(value) > selector[2][1]){
                window.notify("Value too large!")
                return;
            }
            if (parseInt(value) < selector[2][0]){
                window.notify("Value too small!")
                return;
            }
        }
        let message = JSON.stringify(
            {
                action: "set",
                setter: selector[0],
                value: value
            }
        );

        window.sock.send(message);
        window.SocketLog.log(message);
    })
}

const updateConstraints = (data) => {
    for ([k, v] of Object.entries(data)){
        $('#' + k).val(v)
    }
}

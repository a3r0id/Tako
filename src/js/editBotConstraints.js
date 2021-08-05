
let constraintSelectors = [
    // [selector, isInt, [int, range]]
    ["max_dataset_length", true, [25, 1000]],
    ["interval_time_seconds", true, [10, 300]],
    ["required_retweets", true, [0, 10000000]],
    ["required_favorites", true, [0, 10000000]],
    ["query_amount", true, [1, 500]]
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
        window.sock.send(JSON.stringify(
            {
                action: "set",
                setter: selector[0],
                value: value
            }
        ));
    })
}

const updateConstraints = (data) => {
    for ([k, v] of Object.entries(data)){
        $('#' + k).val(v)
    }
}

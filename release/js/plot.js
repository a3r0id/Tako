
class Trace
{
    constructor(xData, yData, name, type, mode="markers", textArray, line, marker)
    {
        // line = {color: 'rgb(0, 0, 0)', width: 1};
        // marker = {color: 'rgb(0, 0, 0)', size: 12};
        this.xData      = xData;
        this.yData      = yData;
        this.name       = name;
        this.type       = type;
        this.mode       = mode;
        this.line       = line;
        this.marker     = marker;
        this.textArray  = textArray;
        
        this.trace = {
            x: this.xData,
            y: this.yData,
            text: this.textArray,
            name: this.name,
            type: this.type,
            line: this.line
        };
    }

    get = () => {return this.trace}
}

plot = (divId, traces, title, xAxis={}, yAxis={}, legend={}) => {

    /* x/yAxis = {
        title(string),
        showgrid(bool),
        zeroline(bool),
        range: [0.75, 5.25],
        autorange: false,
        traceorder: 'reversed',
        font: {
            size: 16
        }
    }
    */

    /*
    legend: {
        y: 0.5,
        traceorder: 'reversed',
        font: {size: 16},
        yref: 'paper'
    }
    */

    var layout = {
        title: title,
        xaxis: xAxis,
        yaxis: yAxis,
        legend: legend,
        plot_bgcolor: 'black',
        paper_bgcolor: 'black',
        font: {
            size: 10,
            color: 'white'
        }
    };

    Plotly.newPlot(divId, traces, layout);

}

window.updatePerformanceAnalytics = () => {
    let x = macros.dropRate.x;
    let y = macros.dropRate.y;
    plot("analytics-automation-keep-rate", [rtTrace = new Trace(
        x,
        y,
        "Drop Rate",
        "line",
        mode="markers",
        [],
        {color: 'rgb(255, 55, 55)', width: 1},
        {color: 'rgb(255, 55, 55)', size: 12}
    ).get()], "Average % Interacted With (Efficiency Rate)")
}

window.updatePerformanceAnalytics();


window.updateLikeRetweets = () => 
{

    likesTrace = new Trace(
        macros.likesAndRetweets.x,
        macros.likesAndRetweets.y.likes,
        "Likes",
        "line",
        mode="markers",
        [],
        {color: 'rgb(255, 55, 55)', width: 1},
        {color: 'rgb(255, 55, 55)', size: 12}
    ).get();

    retweetsTrace = new Trace(
        macros.likesAndRetweets.x,
        macros.likesAndRetweets.y.retweets,
        "Retweets",
        "line",
        mode="markers",
        [],
        {color: 'rgb(55, 255, 55)', width: 1},
        {color: 'rgb(55, 255, 55)', size: 12}
    ).get();

    plot("analytics-automation-likes-retweets", [likesTrace, retweetsTrace], "Likes & Retweets (Total)")
}

window.updateLikeRetweets();


window.updateFollowers = () => {

    plot("analytics-interaction-followers", [followersTrace = new Trace(
        macros.followers.x,
        macros.followers.y,
        "Retweets",
        "line",
        mode="markers",
        [],
        {color: 'rgb(55, 55, 255)', width: 1},
        {color: 'rgb(55, 55, 255)', size: 12}
    ).get()], "Followers (Total)")

}

window.updateFollowers();


window.updateUsage = () => {

    plot("analytics-usage-plot", [followersTrace = new Trace(
        macros.totalPullsSet.x,
        macros.totalPullsSet.y,
        "API Usage (Requests)",
        "line",
        mode="markers",
        [],
        {color: 'rgb(55, 55, 255)', width: 1},
        {color: 'rgb(55, 55, 255)', size: 12}
    ).get()], "Requests (Total)");

}

window.updateUsage();

window.updateUsageLast24 = (x, y) =>
{
    plot("analytics-usage-plot-24", [followersTrace = new Trace(
        x,
        y,
        "Today's API Usage (Requests)",
        "line",
        mode="markers",
        [],
        {color: 'rgb(55, 55, 255)', width: 1},
        {color: 'rgb(55, 55, 255)', size: 12}
    ).get()], "Requests (24 Hours)");
}

window.updateUsageLast24(macros.totalPullsLast24.x, macros.totalPullsLast24.y);
function formatBytes(a,b=2,k=1024){with(Math){let d=floor(log(a)/log(k));return 0==a?"0 Bytes":parseFloat((a/pow(k,d)).toFixed(max(0,b)))+" "+["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][d]}}

window.errors = [];
window.onerror = function(message, source, lineno, colno, error)
{
    let d = new Date();
    let datetime = d.toString();
    let ms = d.getMilliseconds();
    let dtString = datetime.split(" ")[4] + `:${ms} ` + datetime.split(" ")[1] + " " + datetime.split(" ")[2];

    let err = {
        time: datetime,
        message: message,
        source: source,
        line: lineno,
        column: colno,
        error: error
    };

    window.errors.push(err);

    let indice = window.errors.length;

    $("#errorLogAnchor").append(`
    <div id="err-${indice}">
      <span style="font-size: small;">${dtString}</span>
      <div id="errBody-${indice}" style="width: 100%;height: 100%;"></div>
    </div>
    `)

    setTimeout(() => {
        $(`#errBody-${indice}`).empty().simpleJson({jsonObject: err});
    }, 100)
};

class Debug{
    constructor(time)
    {
        this.time = time;
        this.looper = () => {

            // MEMORY
            let memory = window.performance.memory;
            $('#jsHeapSizeLimit').html(formatBytes(memory.jsHeapSizeLimit, 3));
            $('#totalJSHeapSize').html(formatBytes(memory.totalJSHeapSize, 3));
            $('#usedJSHeapSize').html(formatBytes(memory.usedJSHeapSize, 3));

            // EVENTS
            $('#eventCounts-size').html(window.performance.eventCounts.size);

            // NAVIGATION
            $('#navType').html(window.performance.navigation.type)
            $('#redirectCounts').html(window.performance.navigation.redirectCount);
            
            let origin = new Date(window.performance.timeOrigin);
            $('#timeInit').html(
                origin.toTimeString() + " " + origin.toDateString()
            );

            let now = new Date();
            $('#timeNow').html(
                now.toTimeString() + " " + now.toDateString()
            );

            let duration  = (now - origin),
            milliseconds  = Math.floor((duration % 1000) / 100),
            seconds       = Math.floor((duration / 1000) % 60),
            minutes       = Math.floor((duration / (1000 * 60)) % 60),
            hours         = Math.floor((duration / (1000 * 60 * 60)) % 24);
        
            hours         = (hours < 10)   ? "0" + hours   : hours;
            minutes       = (minutes < 10) ? "0" + minutes : minutes;
            seconds       = (seconds < 10) ? "0" + seconds : seconds;

            $('#timeElapsed').html(
                `${hours}:${minutes}:${seconds}.${milliseconds}`
            );

            // LOOP
            setTimeout(this.looper, this.time);


        };
        setTimeout(() => {
            this.looper();
        }, this.time);
    }
}

$('#download-error-logs').on('click', () => {
    let data = JSON.stringify(window.errors, null, 2);
    let href = "text/plain;charset=utf-8," + encodeURIComponent(data); 
    let element = document.createElement('a');
    element.setAttribute('href', `data: ${href}`);
    element.setAttribute('download', "tako_error_log.json");
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
})

new Debug(100);


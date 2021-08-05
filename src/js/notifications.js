window.notify = (message) =>
{

    $('.data-notify-text').css("font-family", "'Oswald', sans-serif");
    $('.data-notify-text').css("color", "whitesmoke");
    $('.notifyjs-bootstrap-base').css("background-color", "red");
    //notifyjs-bootstrap-main-font
    /*
    {
        style: 'bootstrap',
        gap: 20,
        autoHide: true,
        autoHideDelay: 5000,
        arrowShow: true,
        arrowSize: 5,
        showAnimation: 'slideDown',
        hideAnimation: 'slideUp',
        showDuration: 400,
        hideDuration: 200
    }
    */
    // MODES: success, info, warn, error
    $('#top-bar').notify(
        message, 
        {
            position:"bottom center",
            arrowShow: false,
            clickToHide: true
        }
    );
};

// Notify is rediculously broken, css/classess/position DO NOT WORK!!!!!!!!!!!!!!!!
let ttt = () => {
    if ( $('.notifyjs-wrapper').is(':visible') )
    {
        $('.notifyjs-wrapper').css("margin", "0 auto");
    }
    setTimeout(ttt, 100);
};

setTimeout(ttt, 100);

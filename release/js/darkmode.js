const darkMode = () =>
{

    // SET DARKMODE TO TRUE IN LOCALSTORAGE
    localStorage.setItem("darkmode", JSON.stringify({
        enabled: true,
        auxillary: {} // Redundant, for future updates so we dont have to overwrite the object.
    }));

    // CHECK CHECKBOX IN THE CASE THAT DARKMODE WAS AUTOMATICALLY ASSIGNED
    if (!$('#darkmode-tgl').is(':checked')){
        $('#darkmode-tgl').prop('checked', true)
    }

    // CHANGE ALL DIVS
    $('div')
        .css("background-color", "black")
        .css("color", "white");

    // FIXES BARS
    $('.bar-borders')
      .css("background-color", "")
      .css("color", "")
      //.toggleClass("bar-borders")

    // FIXES PLOTLY PRODUCTS
    $('.modebar-group').css("background-color", "white");
    $('.modebar').css("background-color", "white");
    
    setTimeout( ()=>
    {
        $('.styleMode')
          .css("color", "green")
          .css("background-color", "black")
          .css("font-family", "'BankGothic', sans-serif")

        $('[aria-controls="log-table"]')
          .css("color", "green")
          .css("background-color", "black")
          .css("font-family", "'BankGothic', sans-serif")

        $('[aria-controls="log-table"]')
            .on('input', ()=>
            {
                setTimeout( ()=>
                {
                    $('.dataTables_empty')
                      .css("color", "green")
                      .css("background-color", "black")
                      .css("font-family", "'BankGothic', sans-serif")

                }, 100)
            })  
    }, 100)
}

const lightMode = () =>
{

    // SET DARKMODE TO TRUE IN LOCALSTORAGE
    localStorage.setItem("darkmode", JSON.stringify({
        enabled: false,
        auxillary: {} // Redundant, for future updates so we dont have to overwrite the object.
    }));

    $('div')
        .css("background-color", "white")
        .css("color", "black")
        .css("font-family", "'BankGothic', sans-serif")

    setTimeout( ()=>{

        $('.styleMode')
          .css("color", "black")
          .css("background-color", "white")
          .css("font-family", "'BankGothic', sans-serif")

        $('[aria-controls="log-table"]')
          .css("color", "black")
          .css("background-color", "white")
          .css("font-family", "'BankGothic', sans-serif")

        $('[aria-controls="log-table"]')
            .on('input', ()=>
            {
                setTimeout( ()=>
                {
                    $('.dataTables_empty')
                      .css("color", "black")
                      .css("background-color", "white")
                      .css("font-family", "'BankGothic', sans-serif")

                }, 100)
            })  
    }, 100)
}

let darkModeHistory = localStorage.getItem("darkmode");

if (darkModeHistory == undefined){
    localStorage.setItem("darkmode", JSON.stringify({
        enabled: false,
        auxillary: {} // Redundant, for future updates so we dont have to overwrite the object.
    }));
}
else{
    if ( JSON.parse(darkModeHistory).enabled ){
        darkMode();
    }
}

$('#darkmode-tgl').on('change', (e) => {
    if (e.target.checked){
        darkMode();
    }
    else{
        lightMode();
    }
})
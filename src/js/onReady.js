$(document).ready(function()
{
    window.logTable = $('#log-table').DataTable({
        autoWidth: false,
        data: [
            [`[${new Date().toTimeString().split(' ')[0]}] Logging Initialized...`]
        ],
        columns: [
            { title: "Message" },
        ],
        columnDefs: [
            {
                targets: ['_all'],
                className: 'styleMode'
            }
        ]
    });
/*
    const styleLogLoop = () =>
    {
        setTimeout(() => {
            $('.mdc-data-table__cell')
              .css("background-color", "black")
              .css("color", "green");
            styleLogLoop();
        }, 100)
    }
*/
    window.updateLogsView = (newData) => {
        window.logTable.clear();
        window.logTable.rows.add(newData.reverse());
        window.logTable.draw();
        //styleLogLoop();
    }

    $(document.body).on('click', (e)=>{
        if (e.target.id == "edit-modal"){
            $('#edit-modal').hide();
        }
        if (e.target.id == "constraints-modal"){
            $('#constraints-modal').hide();
        }
    })

} );
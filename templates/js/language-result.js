var pathname = window.location.pathname
$.ajax({
    url: `/api${pathname}`,
    type: "get",
    success: function(result) {
        console.log("Results from BE:")
        console.log(result)
        var plotDiv = document.getElementById('plot');
        var traces = [
            {
                x: result.week_start,
                y: result.uk_percentage,
                stackgroup: 'one',
                name: 'Українська'

            },
            {
                x: result.week_start,
                y: result.ru_percentage,
                stackgroup: 'one',
                name: 'Російська',
                mode: 'none'
            }
        ];

        var layout = {
            title: 'Відосоток повідомлень українською і російською мовами',
            hovermode: 'x unified',
            xaxis: {
                title: 'Дата'
            },
            yaxis: {
                title: 'Відсоток повідомлень'
            }
        }

        Plotly.newPlot('myDiv', traces, layout);
    },
    error: function (xhr, ajaxOptions, thrownError) {
        if (xhr.status==404) {
            $('#file_not_found').text("Файл ще в обробці. Спробуйте, будь-ласка, пізніше.");
            $('#file_not_found').show()
        }
    }
});



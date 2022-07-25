var pathname = window.location.pathname
$.ajax({
    url: `/api${pathname}`,
    type: "get",
    success: function(result) {
        console.log("Results from BE:")
        console.log(result)
        var data = [
          {
            x: result.members,
            y: result.number_of_messages,
            type: 'bar',
            text: result.number_of_messages.map(String),
            textposition: 'outside',
            marker: {
                color: 'cyan'
            }
          }
        ];

        var layout = {
//          autosize: false,
//          width: 1500,
//          height: 1000
        }

        Plotly.newPlot('myDiv', data, layout);
    },
    error: function (xhr, ajaxOptions, thrownError) {
        if (xhr.status==404) {
            $('#file_not_found').text("Файл ще в обробці. Спробуйте, будь-ласка, пізніше.");
            $('#file_not_found').show()
        }
    }
});



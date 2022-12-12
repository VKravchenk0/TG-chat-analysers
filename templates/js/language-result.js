function createFiftyPercentLine() {
    return {
        type: 'line',
        xref: 'paper',
        x0: 0,
        x1: 1,
        y0: 50,
        y1: 50,
        yref: 'y',
        line: {
          color: 'black',
          width: 1,
          dash: 'dot'
        }
    };
}

function displayTitle(result) {
    let chatInfo = result.chat_info;
    if (chatInfo.name && getUrlParameter('showName')) {
        $('#chat-name').val(chatInfo.name);
        $('#chat-name').show()
    }
    if (chatInfo.link && getUrlParameter('showLink')) {
        $('#link').val(chatInfo.link);
        $('#link').show();
    }
    if (chatInfo.number_of_users && getUrlParameter('showNumberOfUsers')) {
        $('#number_of_users').val(chatInfo.number_of_users);
        $('#number_of_users').show();
    }
    if (chatInfo.location && getUrlParameter('showLocation')) {
        $('#location').val(chatInfo.location);
        $('#location').show();
    }
}

function displayPlot(result) {
    var plotDiv = document.getElementById('plot');
    var dataToPrint = {};
    parsedDates = parseDates(result.week_start);

    var traces = [
        {
            type: 'scatter',
            x: parsedDates,
            y: result.uk_percentage,
            stackgroup: 'one',
            name: 'Українська',
            line: {
                color: '#0057B8'
            }
        },
        {
            type: 'scatter',
            x: parsedDates,
            y: result.ru_percentage,
            stackgroup: 'one',
            name: 'Російська',
            line: {
                color: '#DA291C'
            }
        }
    ];

    var shapes = [];
    var annotations = [];

    shapes.push(createFiftyPercentLine());

    if (dateInRange(parsedDates, '24/02/2022')) {
        console.log("adding line for 24/02/2022")
        shapes.push({
            type: 'line',
            x0: parseDate('24/02/2022'),
            xref: 'x',
            y0: 0,
            x1: parseDate('24/02/2022'),
            yref: 'y',
            y1: 100,
            fillcolor: 'black',
            opacity: 0.5,
            line: {
                width: 2
            }
        });

        annotations.push({
              x: parseDate('24/02/2022'),
              y: 30,
              xref: 'x',
              yref: 'y',
              text: '24/02',
              showarrow: true,
              arrowhead: 0,
              ax: 40,
              ay: -10,
              font: {
                size: 18,
              },
        });
    }

    var layout = {
//            title: {
//                text: 'Відсоток повідомлень українською і російською мовами'
//            },
        hovermode: 'x unified',
        xaxis: {
            title: 'Дата'
        },
        yaxis: {
            title: 'Відсоток повідомлень'
        },
        shapes: shapes,
        annotations: annotations
    }

    Plotly.newPlot('myDiv', traces, layout);
}

var pathname = window.location.pathname
$.ajax({
    url: `/api${pathname}`,
    type: "get",
    success: function(result) {
        console.log("Results from BE:")
        console.log(result)

        displayTitle(result);

        displayPlot(result);
    },
    error: function (xhr, ajaxOptions, thrownError) {       if (xhr.status==404) {
            $('#file_not_found').text("Файл ще в обробці. Спробуйте, будь-ласка, пізніше.");
            $('#file_not_found').show()
        }
    }
});



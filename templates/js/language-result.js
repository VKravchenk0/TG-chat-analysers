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

function displayDescription(result) {
    if (result.chat_info && result.chat_info.description) {
        let chatInfo = result.chat_info;
        let descriptionArr = chatInfo.description.split("\n");
        descriptionArr.forEach((descLine) => {
            $('<p>', {}).html(descLine.trim()).appendTo('#result_chat_description .wrapper');
        });

        $('#result_chat_description').show()
    }
}

var pathname = window.location.pathname
$.ajax({
    url: `/api${pathname}`,
    type: "get",
    success: function(result) {
        console.log("Results from BE:")
        console.log(result)
        var plotDiv = document.getElementById('plot');
        var dataToPrint = {};
        parsedDates = parseDates(result.timespan_start);

        var traces = [
            {
                type: 'scatter',
                x: parsedDates,
                y: result.uk_percentage,
                stackgroup: 'one',
                name: 'Українська',
                line: {
                    color: '#0057B7'
                }
            },
            {
                type: 'scatter',
                x: parsedDates,
                y: result.ru_percentage,
                stackgroup: 'one',
                name: 'Російська',
                line: {
                    color: '#FF2B12'
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
                  y: 20,
                  xref: 'x',
                  yref: 'y',
                  text: '24/02/2022',
                  showarrow: true,
                  arrowhead: 3,
                  ax: 70,
                  ay: -30,
                  font: {
                    size: 18,
                  },
            });
        }

        axisTitleSize = 16;
        tickSize = 15;
        var layout = {
            title: 'Приріст використання української мови в телеграм-чатах',
            hovermode: 'x unified',
            xaxis: {
                title: {
                    text: 'Дата',
                    font: {
                        size: axisTitleSize
                    }
                },
                tickmode: "array",
                tickvals: getMonthStartsArray(parsedDates),
                tickformat: '%m/%Y', // For more time formatting types, see: https://github.com/d3/d3-time-format/blob/master/README.md
                tickfont: {
                    size: tickSize
                },
                gridcolor: '#eee',
                griddash: 'solid',
                gridwidth: 1.5
            },
            yaxis: {
                title: {
                    text: 'Відсоток повідомлень',
                    font: {
                        size: axisTitleSize
                    }
                },
                tickfont: {
                    size: tickSize
                },
                gridwidth: 1.5
            },
            shapes: shapes,
            annotations: annotations,
            legend: {
                x: 0,
                y: 4,
                traceorder: "normal"
            }
        }

        displayDescription(result);

        Plotly.newPlot('myDiv', traces, layout);
    },
    error: function (xhr, ajaxOptions, thrownError) {
        if (xhr.status==404) {
            $('#file_not_found').text("Файл ще в обробці. Спробуйте, будь-ласка, пізніше.");
            $('#file_not_found').show()
        }
    }
});



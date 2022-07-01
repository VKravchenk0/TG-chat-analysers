$.ajax({
    url: "/api/data",
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
    }
  });

/*var plotDiv = document.getElementById('plot');

var traces = [
	{x: ["2022-06-27", "2022-07-04", "2022-07-11"], y: [20, 40, 50], stackgroup: 'one'},
	{x: ["2022-06-27", "2022-07-04", "2022-07-11"], y: [80, 60, 50], stackgroup: 'one'}
];

Plotly.newPlot('myDiv', traces, {title: 'stacked and filled line chart'});
*/



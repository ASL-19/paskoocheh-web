(function () { 'use strict';

pkStats.renderToolDownloadsPerDayChart = function () {
    var tools = [];
    var days = [];
    var plotlyData = [];

    var startIsoDate = pkStats.dateToIsoDateString(pkStats.startDate);
    var endIsoDate = pkStats.dateToIsoDateString(pkStats.endDate);

    var apiUrl = '/api/v1/stats/daily/downloadpertool/?format=json&start=' + startIsoDate + '&end=' + endIsoDate;

    pkStats.loadJSON(apiUrl, function(responseText) {
        var dailyToolDownloadCountObjects = JSON.parse(responseText);

        var largestDownloadCount = 0;

        for (var i = 0; i < dailyToolDownloadCountObjects.length; i++) {
            if (dailyToolDownloadCountObjects[i].count > largestDownloadCount) {
                largestDownloadCount = dailyToolDownloadCountObjects[i].count;
            }
        }

        pkStats.counter('tool', tools, days, dailyToolDownloadCountObjects);

        for (var i = 0; i < tools.length; i++) {
            var toolData = {
                x: [],
                y: [],
                name: tools[i],
                type: 'scatter',
            };

            pkStats.countDictionary('tool', 'count', toolData, tools, days, i, dailyToolDownloadCountObjects);

            plotlyData.push(toolData);
        }

        var layout = {
            title : 'Tool downloads/day',
            font: {
                family: 'Roboto, Verdana, sans-serif',
                size: 12,
                color: '#212121'
            },
            autorange: true,
            autosize: true,
            width: pkStats.chartContainer.offsetWidth,
            height: pkStats.chartContainer.offsetHeight,
            margin: {
                l: 0,
                r: 0,
                b: 64,
                t: 64,
                pad: 0,
            },
            xaxis: {
                range: [
                    pkStats.getDayBeforeDate(pkStats.startDate),
                    pkStats.getDayAfterDate(pkStats.endDate)
                ]
            },
            yaxis: {
                range: [
                    0,
                    largestDownloadCount * 1.05
                ]
            },
            updatemenus: [{
                buttons: [{
                    label: 'Show',
                    method: 'restyle',
                    args: ['visible', true]
                }, {
                    label: 'Hide',
                    method: 'restyle',
                    args: ['visible', 'legendonly']
                }]
            }],
        };

        Plotly.newPlot(pkStats.chartContainer, plotlyData, layout);
    });
}

})();

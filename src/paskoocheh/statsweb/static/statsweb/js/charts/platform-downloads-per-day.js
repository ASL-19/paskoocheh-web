(function () { 'use strict';

pkStats.renderPlatformDownloadsPerDayChart = function () {
    var platforms = [];
    var days = [];
    var plotlyData = [];

    var startIsoDate = pkStats.dateToIsoDateString(pkStats.startDate);
    var endIsoDate = pkStats.dateToIsoDateString(pkStats.endDate);

    var apiUrl = '/api/v1/stats/daily/downloadperplatform/?format=json&start=' + startIsoDate + '&end=' + endIsoDate;

    pkStats.loadJSON(apiUrl, function(responseText) {
        var dailyPlatformDownloadCountObjects = JSON.parse(responseText);

        var largestDownloadCount = 0;

        for (var i = 0; i < dailyPlatformDownloadCountObjects.length; i++) {
            if (dailyPlatformDownloadCountObjects[i].count > largestDownloadCount) {
                largestDownloadCount = dailyPlatformDownloadCountObjects[i].count;
            }
        }

        pkStats.counter('platform', platforms, days, dailyPlatformDownloadCountObjects);

        for (var i = 0; i < platforms.length; i++) {
            var platformData = {
                x: [],
                y: [],
                name: platforms[i],
                type: 'scatter',
            };

            pkStats.countDictionary('platform', 'count', platformData, platforms, days, i, dailyPlatformDownloadCountObjects);

            plotlyData.push(platformData);
        }

        var plotlyLayout = {
            title : 'Platform downloads/day',
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

        Plotly.newPlot(pkStats.chartContainer, plotlyData, plotlyLayout);
    });
}

})();

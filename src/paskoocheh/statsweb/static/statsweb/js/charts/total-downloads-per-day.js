(function () { 'use strict';

pkStats.renderTotalDownloadsPerDayChart = function () {
    var startIsoDate = pkStats.dateToIsoDateString(pkStats.startDate);
    var endIsoDate = pkStats.dateToIsoDateString(pkStats.endDate);

    var apiUrl = '/api/v1/stats/daily/download/?format=json&start=' + startIsoDate + '&end=' + endIsoDate;

    pkStats.loadJSON(apiUrl, function(responseText) {
        var dailyDownloadCountObjects = JSON.parse(responseText);

        var downloadsPerDayTrace = {
            x: [],
            y: [],
            name: 'Total downloads/day',
            type: 'scatter',
        };

        var largestDownloadCount = 0;

        for (var i = 0; i < dailyDownloadCountObjects.length; i++) {
            downloadsPerDayTrace.x.push(dailyDownloadCountObjects[i].date);
            downloadsPerDayTrace.y.push(dailyDownloadCountObjects[i].count);

            if (dailyDownloadCountObjects[i].count > largestDownloadCount) {
                largestDownloadCount = dailyDownloadCountObjects[i].count;
            }
        }

        var plotlyData = [downloadsPerDayTrace];

        var plotlyLayout = {
            title : 'Total downloads/day',
            font: {
                family: 'Roboto, Verdana, sans-serif',
                size: 12,
                color: '#212121'
            },
            autosize: true,
            autorange: true,
            width: pkStats.chartContainer.offsetWidth,
            height: pkStats.chartContainer.offsetHeight,
            margin: {
                l: 64,
                r: 64,
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
            }
        };
        Plotly.newPlot(pkStats.chartContainer, plotlyData, plotlyLayout);
    });
};

})();

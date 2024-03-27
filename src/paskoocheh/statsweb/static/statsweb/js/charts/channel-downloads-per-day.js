(function () { 'use strict';

pkStats.renderChannelDownloadsPerDayChart = function () {
    var channels = [];
    var days = [];
    var plotlyData = [];

    var startIsoDate = pkStats.dateToIsoDateString(pkStats.startDate);
    var endIsoDate = pkStats.dateToIsoDateString(pkStats.endDate);
    var apiUrl = '/api/v1/stats/daily/downloadperchannel/?format=json&start=' + startIsoDate + '&end=' + endIsoDate;

    pkStats.loadJSON(apiUrl, function (responseText) {
        var dailyChannelDownloadCountObjects = JSON.parse(responseText);

        var largestDownloadCount = 0;

        for (var i = 0; i < dailyChannelDownloadCountObjects.length; i++) {
            if (dailyChannelDownloadCountObjects[i].count > largestDownloadCount) {
                largestDownloadCount = dailyChannelDownloadCountObjects[i].count;
            }
        }

        pkStats.counter('channel', channels, days, dailyChannelDownloadCountObjects);

        for (var i = 0; i < channels.length; i++) {
            var channelData = {
                x: [],
                y: [],
                name: channels[i],
                type: 'scatter',
            };

            pkStats.countDictionary('channel', 'count', channelData, channels, days, i, dailyChannelDownloadCountObjects);

            plotlyData.push(channelData);
        }

        var plotlyLayout = {
            title : 'Channel downloads/day',
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

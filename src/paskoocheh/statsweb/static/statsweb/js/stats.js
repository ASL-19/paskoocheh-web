(function () { 'use strict';

var yesterday = function () {
    var tempDate = new Date();
    tempDate.setDate(tempDate.getDate() - 1);
    return tempDate;
}();

var oneMonthBeforeYesterday = function () {
    var tempDate = new Date(yesterday);
    tempDate.setMonth(tempDate.getMonth() - 1);
    return tempDate;
}();

// Global container object
window.pkStats = {};

// Load the specified JSON file and execute the callback function
pkStats.loadJSON = function (jsonFilePath, callback) {
    var xobj = new XMLHttpRequest();
    xobj.open('GET', jsonFilePath, true);
    xobj.onreadystatechange = function() {
        if (xobj.readyState == 4 && xobj.status == "200") {
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
};

// http://stackoverflow.com/a/242888
pkStats.numberWithCommas = function (x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

// Sum up the download counts from totaldownload endpoint and display them at top right
pkStats.populateTotalDownloads = function (response) {
    pkStats.loadJSON('/api/v1/stats/totaldownload/?format=json', function (response) {
        var totalDownloads = 0;
        var downloadsCountsObjects = JSON.parse(response);
        var totalDownloadsSpan = document.getElementById('total-downloads');

        for (var i = 0; i < downloadsCountsObjects.length; i++) {
            var downloadCountObject = downloadsCountsObjects[i];
            totalDownloads += downloadCountObject.download_count;
        }

        totalDownloadsSpan.innerHTML = pkStats.numberWithCommas(totalDownloads);
    });
};

})();

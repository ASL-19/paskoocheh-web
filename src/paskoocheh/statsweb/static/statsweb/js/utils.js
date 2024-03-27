(function () { 'use strict';

pkStats.countDictionary = function (entityNameKey, type, dataObjects, entityNames, days, i, response) {
    for (var j = 0; j < days.length; j++) {
        dataObjects.x.push(days[j]);

        var date_found = false;

        for (var k = 0; k < response.length; k++) {
            if (response[k][entityNameKey] == entityNames[i] && response[k].date == days[j]) {
                dataObjects.y.push(response[k][type]);
                date_found = true;
                break;
            }
        }

        if (!date_found) {
            dataObjects.y.push(0);
        }
    }
};

pkStats.counter = function (entityNameKey, entityNames, days, response) {
    for (var i = 0; i < response.length; i++) {
        if (!(entityNames.indexOf(response[i][entityNameKey]) >= 0)) {
            entityNames.push(response[i][entityNameKey]);
        }
        if (!(days.indexOf(response[i].date) >= 0)) {
            days.push(response[i].date);
        }
    }
};

pkStats.dateToIsoDateString = function (date) {
    return date.toISOString().slice(0,10);
};

pkStats.getDayAfterDate = function (date) {
    var dayAfterDate = new Date(date);
    dayAfterDate.setDate(dayAfterDate.getDate() + 1);
    return dayAfterDate;
};

pkStats.getDayBeforeDate = function (date) {
    var dayBeforeDate = new Date(date);
    dayBeforeDate.setDate(dayBeforeDate.getDate() - 1);
    return dayBeforeDate;
};

})();


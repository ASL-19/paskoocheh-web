(function () { 'use strict';

// This runs when the document has been parsed. Waiting for readyState ==
// 'complete' or window load event means waiting for all resources (including
// images) to finish loading.
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    init();
} else {
    document.onreadystatechange = function () {
        if (document.readyState === 'interactive' || document.readyState === 'complete') {
            document.onreadystatechange = null;
            init();
        }
    };
}

// =======================
// === Initialize site ===
// =======================
// Runs when document is ready
function init() {
    // -----------------------------------------------
    // --- Set up global chart container reference ---
    // -----------------------------------------------
    pkStats.chartContainer = document.getElementById('chart-container');

    // ------------------------------------
    // --- Populate the total downloads ---
    // ------------------------------------
    pkStats.populateTotalDownloads();

    // -----------------------------------
    // --- Set up start and end inputs ---
    // -----------------------------------
    var today = new Date();

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

    var startPickaday = new Pikaday({
        field: document.getElementById('startDate'),
        minDate: new Date(2016, 5, 15),
        maxDate: today,
        defaultDate: oneMonthBeforeYesterday,
        setDefaultDate: true,
        format: 'YYYY-MM-DD',
        onSelect: reRenderCurrentChart,
    });

    var endPickaday = new Pikaday({
        field: document.getElementById('endDate'),
        minDate: new Date(2016, 5, 15),
        maxDate: today,
        defaultDate: yesterday,
        setDefaultDate: true,
        format: 'YYYY-MM-DD',
        onSelect: reRenderCurrentChart,
    });

    // --------------------------------------
    // --- Add event listeners to buttons ---
    // --------------------------------------
    var totalButton = document.getElementById('total-button');
    var perChannelButton = document.getElementById('per-channel-button');
    var perToolButton = document.getElementById('per-tool-button');
    var perPlatformButton = document.getElementById('per-platform-button');

    totalButton.addEventListener("click", function all() {
        removeExistingPlotlyContainerElem();
        renderCurrentChart = pkStats.renderTotalDownloadsPerDayChart;
        renderCurrentChart();
    });
    perChannelButton.addEventListener("click", function () {
        removeExistingPlotlyContainerElem();
        renderCurrentChart = pkStats.renderChannelDownloadsPerDayChart;
        renderCurrentChart();
    });
    perToolButton.addEventListener("click", function pdpa() {
        removeExistingPlotlyContainerElem();
        renderCurrentChart = pkStats.renderToolDownloadsPerDayChart;
        renderCurrentChart();
    });
    perPlatformButton.addEventListener("click", function pdpb() {
        removeExistingPlotlyContainerElem();
        renderCurrentChart = pkStats.renderPlatformDownloadsPerDayChart;
        renderCurrentChart();
    });

    // ----------------------------
    // --- Render initial chart ---
    // ----------------------------
    updateStartAndEndDates();

    var renderCurrentChart = pkStats.renderTotalDownloadsPerDayChart;
    renderCurrentChart();

    // -----------------
    // --- Functions ---
    // -----------------
    function removeExistingPlotlyContainerElem() {
        var plotlyContainerElem = pkStats.chartContainer.querySelector('.plot-container');

        if (plotlyContainerElem !== null) {
            // This causes the loading indicator to display by activating the
            // #chart-container:empty selector
            pkStats.chartContainer.removeChild(plotlyContainerElem);
        }
    }

    function reRenderCurrentChart() {
        removeExistingPlotlyContainerElem();
        updateStartAndEndDates();
        // renderCurrentChart is a reference to the render function for the active chart
        renderCurrentChart();
    }

    function updateStartAndEndDates() {
        pkStats.startDate = startPickaday.getDate();
        pkStats.endDate = endPickaday.getDate();
    }
}

})();

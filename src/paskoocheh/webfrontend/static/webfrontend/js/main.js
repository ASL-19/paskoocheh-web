(function () { 'use strict'; if (!app.jsSupported) return;

setUpConsole(app.consoleLogLevel);

// Ensure that code runs as entire document is parsed, but no sooner
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    new app.App();
} else {
    document.onreadystatechange = function () {
        if (document.readyState === 'interactive' || document.readyState === 'complete') {
            document.onreadystatechange = null;
            console.info('Document parsed – initializing', (app.platform).toUpperCase());
            new app.App();
        }
    };
}

function setUpConsole(consoleLogLevel) {
    var nullFunction = function () { return null; };

    if (typeof window.console === 'undefined') {
        window.console = {};
    }

    if (consoleLogLevel < 4 || typeof window.console.log === 'undefined') {
        window.console.log = nullFunction;
    }
    if (consoleLogLevel < 3 || typeof window.console.info === 'undefined') {
        window.console.info = nullFunction;
    }
    if (consoleLogLevel < 2 || typeof window.console.warn === 'undefined') {
        window.console.warn = nullFunction;
    }
    if (consoleLogLevel < 1 || typeof window.console.error === 'undefined') {
        window.console.error = nullFunction;
    }

    console.info('Set up console with log level ' + consoleLogLevel);
}

})();

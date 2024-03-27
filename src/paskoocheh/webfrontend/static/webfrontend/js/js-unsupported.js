(function () { 'use strict';

// This file includes code that needs to run if the site is loading with app.jsSupported === false. Every other JS file is prevented from executing if app.jsSupported === false.

if (!app.jsSupported) {
    if (document.readyState === 'interactive' || document.readyState === 'complete') {
        onDocumentInteractive();
    } else {
        document.onreadystatechange = function () {
            if (document.readyState === 'interactive' || document.readyState === 'complete') {
                document.onreadystatechange = null;
                console.info('Document parsed – running JS unsupported fallback global script');
                onDocumentInteractive();
            }
        };
    }
}

function onDocumentInteractive() {
    replicateNoscriptWrappedIframes();
}

function replicateNoscriptWrappedIframes() {
    // Replicate <iframe> elements wrapped in <noscript> tags. Browsers will only parse the contents of <noscript> tags if JavaScript is explicitly disabled, but we want the fallback for all blacklisted browsers.

    var noscriptElems = document.getElementsByTagName('noscript');

    for (var i = 0; i < noscriptElems.length; i++) {
        if (/pk-iframe-wrapper-noscript/.test(noscriptElems[i].className)) {
            var noscriptContainerClassnameAttr = noscriptElems[i].getAttribute('data-container-classname');

            var containerElem = document.createElement('div');
            if (noscriptContainerClassnameAttr !== null) {
                containerElem.className = noscriptElems[i].getAttribute('data-container-classname');
            }
            containerElem.innerHTML = decodeHtml(noscriptElems[i].innerHTML);

            noscriptElems[i].parentNode.insertBefore(containerElem, noscriptElems[i]);
        }
    }
}

function decodeHtml(html) {
    // Via https://stackoverflow.com/a/7394787/7949868
    var txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
}

})();

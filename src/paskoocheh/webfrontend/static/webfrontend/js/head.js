(function () { 'use strict';

var consoleLogLevel = document.querySelector('meta[name="pk-console-log-level"]').getAttribute('content');
var debug = document.querySelector('meta[name="pk-debug"]').getAttribute('content');
var invisibleGrecaptchaSiteKey = document.querySelector('meta[name="pk-invisible-grecaptcha-site-key"]').getAttribute('content');
var languageCode = document.querySelector('meta[name="pk-language-code"]').getAttribute('content');
var requestIsNoOp = document.querySelector('meta[name="pk-request-is-noop"]').getAttribute('content');
var versionNumber = document.querySelector('meta[name="pk-version-number"]').getAttribute('content');
var platform = document.querySelector('meta[name="platform"]').getAttribute('content');

// Container object for app global variables and constructors
window.app = {
    platform: platform,
    version: versionNumber,
    consoleLogLevel: consoleLogLevel,
    debug: (debug === 'True'),
    flickitySupported: true,
    grecaptchaScriptLoaded: false,
    invisibleGrecaptchaSiteKey: invisibleGrecaptchaSiteKey,
    jsSupported: true,
    languageCode: languageCode,
    requestIsNoOp: (requestIsNoOp === 'True'),
    shouldApplyIos11FixedFocusWorkaround: false,
    uaInfo: { /* Contains boolean browser user agent properties (populated below) */ },
};

// Use user agent to attempt to identify browser (not 100% reliable, but good for almost all cases)
var userAgent;
if (typeof(window.navigator) === 'object') {
    userAgent = window.navigator.userAgent;
} else {
    userAgent = undefined;
}

app.uaInfo.isAndroid41WebKit = (
    /Android 4\./.test(userAgent) &&
    /AppleWebKit\/534\.30/.test(userAgent)
);
app.uaInfo.isAndroid44WebKit = (
    /Android 4./.test(userAgent) &&
    /AppleWebKit\/537\.36/.test(userAgent)
);
app.uaInfo.isAndroidFirefox = (
    /Android/.test(userAgent) &&
    /Firefox/.test(userAgent)
);
app.uaInfo.isAndroidWebKit = (
    app.uaInfo.isAndroid41WebKit ||
    app.uaInfo.isAndroid44WebKit
);
app.uaInfo.isIe8 = /MSIE 8\.0/.test(userAgent);
app.uaInfo.isIe9 = /MSIE 9\.0/.test(userAgent);
app.uaInfo.isIos = (
    /iPad|iPhone|iPod/.test(userAgent) &&
    !window.MSStream
);
app.uaInfo.isIos11Pre113 = (
    app.uaInfo.isIos &&
    /OS 11_[012]/.test(userAgent)
);
app.uaInfo.isIosChrome = (
    app.uaInfo.isIos &&
    /CriOS\//.test(userAgent)
);
app.uaInfo.isIosSafari = (
    app.uaInfo.isIos &&
    !app.uaInfo.isIosChrome
);
app.uaInfo.isOperaMiniExtreme = (
    /Opera Mini/.test(userAgent) &&
    /Presto/.test(userAgent)
);

// Use browser variables to set <html> element classes. These are used sparingly for browser-specific bug fixes and fallbacks. We set the class on <html> since the <body> element doesn’t exist at this point.
if (app.uaInfo.isAndroid41WebKit) {
    document.documentElement.className += ' android-41-webkit';
}
if (app.uaInfo.isAndroid44WebKit) {
    document.documentElement.className += ' android-44-webkit';
}
if (app.uaInfo.isIos) {
    document.documentElement.className += ' ios';
}
if (app.uaInfo.isIos11Pre113) {
    app.shouldApplyIos11FixedFocusWorkaround = true;
    document.documentElement.className += ' ios-11-pre-113';
}
if (app.uaInfo.isOperaMiniExtreme) {
    document.documentElement.className += ' opera-mini-extreme';
}

// Use browser variables to blacklist certain browsers from Flickity (carousel) or all JS. If flickitySupported is false a static fallback layout will be used for carousel iamges. If jsSupported is false, all other JS will be blocked from loading, and the default fallback styles will be used.
if (
    app.uaInfo.isAndroid41WebKit ||
    app.uaInfo.isIe8 ||
    app.uaInfo.isOperaMiniExtreme
) {
    app.flickitySupported = false;
    app.jsSupported = false;
} else if (
    app.uaInfo.isIe9
) {
    app.flickitySupported = false;
    app.jsSupported = true;
    document.documentElement.className = document.documentElement.className += ' ie9';
}

// These classes are used to gate styles that are only applicable when Flickity/JS is supported.
if (app.jsSupported) {
    document.documentElement.className = document.documentElement.className.replace('js-unsupported', 'js-supported');
}
if (app.flickitySupported) {
    document.documentElement.className = document.documentElement.className.replace('flickity-unsupported', 'flickity-supported');
}

})();

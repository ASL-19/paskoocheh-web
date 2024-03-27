(function () { 'use strict'; if (!app.jsSupported) return;

var ExternalDownloadLink = function (elem) {
    this.elem = elem;
    this.elemHref = this.elem.getAttribute('href');
    this.recordReferralPath = this.elem.getAttribute('data-record-referral-path');
    this.recordReferralRequest = null;

    this.elem.addEventListener('click', this.onClick.bind(this), false);
};

ExternalDownloadLink.prototype.onClick = function (event) {
    // If the user Ctrl/Cmd/middle-clicks on the link, it probably(?) means
    // they’re opening it in a new tab. We don’t cancel the event (since
    // recordReferral will have time to run), and instruct recordReferral to
    // disable redirection on completion/timeout.
    if (
        (event.button && event.button === 1) ||  // Middle click
        event.ctrlKey ||                         // Ctrl key (Windows, Linux, Chrome OS, etc.)
        event.metaKey                            // Meta (Cmd) key (macOS)
    ) {
        this.recordReferral(false);

    // If the link was clicked normally, we cancel the mouse event since we need
    // to give recordReferral time to run. recordReferally redirects the window
    // when the request completes or times out.
    } else {
        event.preventDefault();
        this.recordReferral(true);
    }

};

ExternalDownloadLink.prototype.recordReferral = function (shouldRedirectOnCompletionOrTimeout) {
    var recordReferralUrl = location.protocol + '//' + location.host + this.recordReferralPath;
    var csrfToken = document.querySelector('meta[name="pk-csrf-token"]').getAttribute('content');

    this.recordReferralRequest = new XMLHttpRequest();

    if (shouldRedirectOnCompletionOrTimeout) {
        this.recordReferralRequest.addEventListener(
            'readystatechange',
            this.onRecordReferralReadyStateChange.bind(this)
        );
        this.recordReferralRequest.addEventListener(
            'timeout',
            this.onRecordReferralTimeout.bind(this)
        );
    }

    this.recordReferralRequest.open('POST', recordReferralUrl);
    this.recordReferralRequest.setRequestHeader('X-CSRFToken', csrfToken);
    this.recordReferralRequest.timeout = 3000;
    this.recordReferralRequest.send();
};

ExternalDownloadLink.prototype.onRecordReferralReadyStateChange = function () {
    // A readyState of 2 indicates that response headers have been recieved, so we’re safe to redirect without having to worry about prematurely cancelling the request.
    if (this.recordReferralRequest.readyState >= 2) {
        window.open(this.elemHref, '_self');
    }
};

ExternalDownloadLink.prototype.onRecordReferralTimeout = function () {
    window.open(this.elemHref, '_self');
};

app.ExternalDownloadLink = ExternalDownloadLink;

})();

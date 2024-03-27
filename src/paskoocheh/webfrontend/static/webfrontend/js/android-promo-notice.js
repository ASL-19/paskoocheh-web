(function () { 'use strict'; if (!app.jsSupported) return;

var AndroidPromoNotice = function (elem) {
    this.elem = elem;
    this.closeButtonElem = this.elem.querySelector('.js-close-button');
    this.downloadButtonElem = this.elem.querySelector('.js-download-button');
    this.isHidden = /hidden/.test(this.elem.className);

    this.closeButtonElem.addEventListener(
        'click',
        this.setHiddenCookie.bind(this),
        false
    );
    this.downloadButtonElem.addEventListener(
        'click',
        this.setHiddenCookie.bind(this),
        false
    );
};

AndroidPromoNotice.prototype.hide = function () {
    this.isHidden = true;
    this.updateDomAttributes();
};

AndroidPromoNotice.prototype.onSetHiddenCookieEndpointResponse = function (progressEvent) {
    if (progressEvent.target.status === 200) {
        this.hide();
    }
};

AndroidPromoNotice.prototype.setHiddenCookie = function () {
    var csrfToken = document.querySelector('meta[name="pk-csrf-token"]').getAttribute('content');

    var endpointRequest = new XMLHttpRequest();
    endpointRequest.addEventListener('load', this.onSetHiddenCookieEndpointResponse.bind(this));
    endpointRequest.open('PUT', '/set-android-promo-notice-hidden-cookie');
    endpointRequest.setRequestHeader('X-CSRFToken', csrfToken);
    endpointRequest.send();
};

AndroidPromoNotice.prototype.updateDomAttributes = function () {
    if (this.isHidden && !/hidden/.test(this.elem.className)) {
        this.elem.className = this.elem.className + ' hidden';
    }
};

app.AndroidPromoNotice = AndroidPromoNotice;

})();

(function () { 'use strict'; if (!app.jsSupported) return;

var Overlay = function (overlayElem) {
    this.isOpen = false;
    this.overlayElem = overlayElem;
    this.overlayBox = overlayElem.querySelector('.js-overlay-box');
    // this.overlayCloseButton = overlayElem.querySelector('.js-overlay-close-button');
    this.overlayHeading = overlayElem.querySelector('.js-overlay-heading');
    this.overlaySlug = overlayElem.getAttribute('data-pk-overlay-slug');
    this.returnFocusElem = null;

    document.addEventListener('focus', this.retainFocus.bind(this), true);
    document.addEventListener('overlaycloserequest', this.onOverlayCloseRequest.bind(this), false);
    document.addEventListener('overlayopenrequest', this.onOverlayOpenRequest.bind(this), false);

    window.addEventListener('paskkeydown', this.onPaskKeyDown.bind(this), false);
};

Overlay.prototype.retainFocus = function (event) {
    if (this.isOpen && !this.overlayElem.contains(event.target)) {
        event.stopPropagation();
        // this.overlayCloseButton.pkFocus();
    }
};

Overlay.prototype.onOverlayCloseRequest = function (event) {
    if (event.overlaySlug === this.overlaySlug) {
        this.close();
    }
};

Overlay.prototype.onOverlayOpenRequest = function (event) {
    if (event.overlaySlug === this.overlaySlug) {
        if (typeof event.returnFocusElem !== 'undefined' && event.returnFocusElem) {
            this.returnFocusElem = event.returnFocusElem;
        }

        this.open();
    }
};

Overlay.prototype.onPaskKeyDown = function (event) {
    if (this.isOpen && event.key === 'Escape') {
        this.close();
        event.stopImmediatePropagation();
    }
};

Overlay.prototype.close = function () {
    this.isOpen = false;
    this.updateDomAttributes();

    if (this.returnFocusElem !== null) {
        if (app.uaInfo.isIos11Pre113) {
            var scrollYTarget = this.returnFocusElem.offsetTop - (window.innerHeight / 2);
            window.scrollTo(0, scrollYTarget);
        }
        this.returnFocusElem.pkFocus();
    } else {
        document.querySelector('h1').pkFocus();
    }

    this.overlayBox.scrollTop = 0;

    this.returnFocusElem = null;
};

Overlay.prototype.open = function () {
    this.isOpen = true;
    this.updateDomAttributes();
    this.overlayHeading.pkFocus();

    var event;

    try  {
        event = new Event('pkoverlayopen');
    } catch (e) {
        event = document.createEvent('Event');
        event.initEvent('pkoverlayopen', false, false);
    }

    event.overlayElem = this.overlayElem;

    window.dispatchEvent(event);
};

Overlay.prototype.updateDomAttributes = function () {
    if (
        this.isOpen && !/ is-open/.test(this.overlayElem.className)
    ) {
        this.overlayElem.className = this.overlayElem.className + ' is-open';
    } else if (
        !this.isOpen && / is-open/.test(this.overlayElem.className)
    ) {
        this.overlayElem.className = this.overlayElem.className.replace(' is-open', '');
    }
};

app.Overlay = Overlay;

})();

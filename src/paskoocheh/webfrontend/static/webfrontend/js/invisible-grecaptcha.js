(function () { 'use strict'; if (!app.jsSupported) return;

var InvisibleGrecaptcha = function (containerElem) {
    this.containerElem = containerElem;
    this.parentFormElem = document.getElementById(this.containerElem.getAttribute('data-pk-invisible-grecaptcha-form-slug') + '-form');
    this.parentFormSubmitElem = document.getElementById(this.containerElem.getAttribute('data-pk-invisible-grecaptcha-form-slug') + '-submit');
    this.grecaptchaRendered = false;
    this.grecaptchaId = null;

    window.addEventListener('pkoverlayopen', this.initOnParentOverlayOpen.bind(this), false);

    if (this.parentFormElem !== null) {
        this.parentFormElem.addEventListener('pkformsubmit', this.executeGrecaptcha.bind(this), false);
    }

    if(this.containerElem && this.containerElem.getAttribute('data-pk-invisible-grecaptcha-form-slug') === 'contact') {
        this.init();
    }
};

InvisibleGrecaptcha.prototype.initOnParentOverlayOpen = function (event) {
    if (event.overlayElem.contains(this.containerElem)) {
        this.init();
    }
};

InvisibleGrecaptcha.prototype.init = function () {
    if (app.grecaptchaScriptLoaded) {
        this.renderGrecaptcha();
    } else if (!app.grecaptchaScriptTagAdded) {
        window.addEventListener('grecaptchaready', this.renderGrecaptcha.bind(this), false);
        this.loadGrecaptchaScript();
    }
};

InvisibleGrecaptcha.prototype.loadGrecaptchaScript = function () {
    var script = document.createElement('script');
    script.type = 'application/javascript';
    script.src = 'https://www.google.com/recaptcha/api.js?onload=pkDispatchGrecaptchaLoadedEvent&render=explicit';

    if (!app.debug) {
        script.src += ('&hl=' + app.languageCode);
    }

    script.setAttribute('async', '');
    script.setAttribute('defer', '');

    document.body.appendChild(script);

    app.grecaptchaScriptTagAdded = true;
};

InvisibleGrecaptcha.prototype.renderGrecaptcha = function () {
    if (this.grecaptchaRendered) {
        return;
    }

    this.grecaptchaRendered = true;

    this.grecaptchaId = grecaptcha.render(
        this.containerElem, {
            sitekey: app.invisibleGrecaptchaSiteKey,
            size: 'invisible',
            callback: this.onGrecaptchaCallback.bind(this)
        }
    );
};

InvisibleGrecaptcha.prototype.executeGrecaptcha = function () {
    grecaptcha.execute(this.grecaptchaId);
};

InvisibleGrecaptcha.prototype.onGrecaptchaCallback = function (responseToken) {
    if (responseToken !== null && responseToken.length > 0) {
        var formGrecaptchaSuccessEvent;
        try  {
            formGrecaptchaSuccessEvent = new Event('pkformgrecaptchasuccess');
        } catch (e) {
            formGrecaptchaSuccessEvent = document.createEvent('Event');
            formGrecaptchaSuccessEvent.initEvent('pkformgrecaptchasuccess', false, false);
        }

        this.parentFormElem.dispatchEvent(formGrecaptchaSuccessEvent);
    }
};

app.InvisibleGrecaptcha = InvisibleGrecaptcha;

// Note: This function needs to attached directly to window since the Google
// recaptcha script callback happens on window and doesn’t work with object
// properties.
window.pkDispatchGrecaptchaLoadedEvent = function () {
    app.grecaptchaScriptLoaded = true;

    var event;
    try  {
        event = new Event('grecaptchaready');
    } catch (e) {
        event = document.createEvent('Event');
        event.initEvent('grecaptchaready', false, false);
    }

    window.dispatchEvent(event);
};

})();

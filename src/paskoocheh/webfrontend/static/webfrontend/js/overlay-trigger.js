(function () { 'use strict'; if (!app.jsSupported) return;

var OverlayTrigger = function (triggerElem) {
    this.triggerElem = triggerElem;
    this.overlaySlug = triggerElem.getAttribute('data-pk-overlay-trigger-slug');
    this.eventName = 'overlay' + triggerElem.getAttribute('data-pk-overlay-trigger-action') + 'request';

    this.triggerElem.addEventListener('click', this.dispatchOverlayRequestEvent.bind(this), false);
};

OverlayTrigger.prototype.dispatchOverlayRequestEvent = function (event) {
    if (event.target !== this.triggerElem) return false;

    // Android WebKit doesn’t support Event constructor, so we fall back to old deprecated method if necessary
    var overlayEvent;
    try  {
        overlayEvent = new Event(this.eventName);
    } catch (e) {
        overlayEvent = document.createEvent('Event');
        overlayEvent.initEvent(this.eventName, false, false);
    }

    overlayEvent.overlaySlug = this.overlaySlug;
    overlayEvent.returnFocusElem = this.triggerElem;
    document.dispatchEvent(overlayEvent);
};

app.OverlayTrigger = OverlayTrigger;

})();

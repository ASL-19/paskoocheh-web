(function () { 'use strict'; if (!app.jsSupported) return;

var GlobalFocusChangeEventDispatcher = function () {
    this.previousFocusDestination = null;

    document.addEventListener('focusin', this.onGlobalFocus.bind(this), true);
    document.addEventListener('focusout', this.onGlobalBlur.bind(this), true);
};

GlobalFocusChangeEventDispatcher.prototype.onGlobalFocus = function (event) {
    this.fireFocusChangeEvent.call(this, event.target);
};

GlobalFocusChangeEventDispatcher.prototype.onGlobalBlur = function (event) {
    this.fireFocusChangeEvent.call(this, event.relatedTarget);
};

GlobalFocusChangeEventDispatcher.prototype.fireFocusChangeEvent = function (focusTarget) {
    if (focusTarget !== this.previousFocusDestination) {
        // Android WebKit doesn’t support Event constructor, so we fall back to old deprecated method if necessary

        var event;
        try  {
            event = new Event('paskfocuschange');
        } catch (e) {
            event = document.createEvent('Event');
            event.initEvent('paskfocuschange', false, false);
        }

        event.focusDestination = focusTarget;
        document.dispatchEvent(event);

        this.previousFocusDestination = focusTarget;
    }
};

app.GlobalFocusChangeEventDispatcher = GlobalFocusChangeEventDispatcher;

})();

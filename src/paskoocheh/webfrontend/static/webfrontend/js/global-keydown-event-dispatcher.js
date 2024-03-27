(function () { 'use strict'; if (!app.jsSupported) return;

var GlobalKeydownEventDispatcher = function () {
    this.mainHeaderSearchInputElem = document.getElementById('main-header-search-input');

    window.addEventListener('keydown', this.onKeydown.bind(this), false);
};

GlobalKeydownEventDispatcher.prototype.onKeydown = function (event) {
    // KeyboardEvent.keyCode is deprecated, but KeyboardEvent.key browser support is still spotty
    if (
        (
            typeof event.key !== 'undefined' &&
            event.key === 'Escape'
        ) ||
        (
            typeof event.keyCode !== 'undefined' &&
            event.keyCode === 27
        )
    ) {
        event.preventDefault();
        this.firePaskKeydownEvent.call(this, 'Escape');
    } else if (
        (
            (
                typeof event.key !== 'undefined' &&
                event.key === '/'
            ) ||
            (
                typeof event.keyCode !== 'undefined' &&
                event.keyCode === 191
            )
        ) &&
        document.activeElement !== this.mainHeaderSearchInputElem
    ) {
        event.preventDefault();
        this.firePaskKeydownEvent.call(this, 'ForwardSlash');
    }
};

GlobalKeydownEventDispatcher.prototype.firePaskKeydownEvent = function (key) {
    // Android WebKit doesn’t support Event constructor, so we fall back to old deprecated method if necessary
    var event;
    try  {
        event = new Event('paskkeydown');
    } catch (e) {
        event = document.createEvent('Event');
        event.initEvent('paskkeydown', false, false);
    }

    event.key = key;

    window.dispatchEvent(event);
};

app.GlobalKeydownEventDispatcher = GlobalKeydownEventDispatcher;

})();

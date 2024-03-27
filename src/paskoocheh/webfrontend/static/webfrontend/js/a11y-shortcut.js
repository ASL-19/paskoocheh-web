(function () { 'use strict'; if (!app.jsSupported) return;

var A11yShortcut = function (elem) {
    this.targetElem = document.getElementById(elem.getAttribute('href').replace('#', ''));

    elem.addEventListener('click', this.onClick.bind(this), false);
};

A11yShortcut.prototype.onClick = function (event) {
    event.preventDefault();
    this.targetElem.pkFocus();
};

app.A11yShortcut = A11yShortcut;

})();

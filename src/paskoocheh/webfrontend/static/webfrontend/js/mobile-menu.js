(function () { 'use strict'; if (!app.jsSupported) return;

var MobileMenu = function (elem) {
    this.menuElement = elem;
    this.backgroundElement = document.getElementsByClassName('pk-mobile-menu-background')[0];
    this.triggerElement = document.getElementsByClassName('pk-mobile-menu-trigger')[0];

    this.isOpen = false;

    this.backgroundElement.addEventListener('click', this.closeAndFocusTriggerElem.bind(this), false);
    this.triggerElement.addEventListener('click', this.toggle.bind(this), false);

    document.addEventListener('paskfocuschange', this.onPaskFocusChange.bind(this), true);

    this.menuElement.className = this.menuElement.className + ' component-initialized';

    var listItemLinkElems = this.menuElement.getElementsByClassName('js-menu-list-item-link');
    for (var i = 0; i < listItemLinkElems.length; i++) {
        listItemLinkElems[i].addEventListener('click', this.onListItemLinkClick.bind(this), false);
    }

    this.platformListToggle = document.getElementById('platform-list-toggle');
    this.appCategoryListToggle = document.getElementById('app-category-list-toggle');

};

MobileMenu.prototype.onPaskFocusChange = function (event) {
    if (
        event.focusDestination === null ||
        event.focusDestination === this.triggerElement
    ) {
        return;
    }

    this.isOpen = this.menuElement.contains(event.focusDestination);

    this.updateDomAttributes();
};

MobileMenu.prototype.onListItemLinkClick = function (event) {
    /*
    This method is called when menu links are clicked to ensure the menu won’t
    remain visible in the retained BFCache[1] page state.

    Note that while the menu is visibly hidden, focus is retained, so if
    the user navigates via tab or screen reader, the menu will reappear.
    This is desirable since focus is ordinarily retained for BFCache
    pages.

    [1] https://stackoverflow.com/a/2639165/7949868
    */

    if (this.isOpen && !this.platformListToggle.contains(event.target) && !this.appCategoryListToggle.contains(event.target)) {
        this.toggle();
    }
};

MobileMenu.prototype.toggle = function (event) {
    if (typeof event !== 'undefined') {
        event.preventDefault();
    }

    if (this.isOpen) {
        this.isOpen = false;
        this.updateDomAttributes();
    } else {
        document.getElementById('navigation').pkFocus();
    }
};

MobileMenu.prototype.closeAndFocusTriggerElem = function () {
    this.isOpen = false;
    this.updateDomAttributes();
    this.triggerElement.pkFocus();
};

MobileMenu.prototype.addBackgroundVisibleClass = function () {
    this.backgroundElement.className = this.backgroundElement.className += ' visible';
};

MobileMenu.prototype.removeBackgroundVisibleClass = function () {
    this.backgroundElement.className = this.backgroundElement.className.replace(' visible', '');
};

MobileMenu.prototype.updateDomAttributes = function () {
    if (
        this.isOpen &&
        !/ mobile-menu-visible/.test(document.documentElement.className)
    ) {
        document.documentElement.className = document.documentElement.className + ' mobile-menu-visible';
        this.addBackgroundVisibleClass();
    } else if (
        !this.isOpen &&
        / mobile-menu-visible/.test(document.documentElement.className)
    ) {
        $('.pk-mobile-menu-cross').hide();
        $('.pk-mobile-menu-trigger').show();
        document.documentElement.className = document.documentElement.className.replace(' mobile-menu-visible', '');
        window.setTimeout(this.removeBackgroundVisibleClass.bind(this), 300);
    }
};

app.MobileMenu = MobileMenu;

})();

(function () { 'use strict'; if (!app.jsSupported) return;

var App = function () {
    this.init();
};

App.prototype.init = function () {
    var i;

    HTMLElement.prototype.pkFocus = this.pkFocus;
    HTMLElement.prototype.pkUnfocus = this.pkUnfocus;

    this.mainHeaderSearchInputElem = document.getElementById('main-header-search-input');

    window.setPlatformCookie = this.setPlatformCookie;
    window.pkGetCookie = this.getCookie;

    var urlParams = new URLSearchParams(document.location.search);
    if(urlParams.get('platform')) {
        this.setPlatformCookie(urlParams);
    }

    window.globalPlatform = $('input[name=globalplatformslug]').val();

    window.addEventListener('paskkeydown', this.focusH1IfEscKeyPressed.bind(this), false);
    window.addEventListener('mousedown', this.hideFocusOutlinesOnMouseDown.bind(this), false);
    window.addEventListener('keydown', this.showFocusOutlinesOnKeyDown.bind(this), false);

    // Components not attached to elements
    new app.GlobalFocusChangeEventDispatcher();
    new app.GlobalKeydownEventDispatcher();

    // Components attached to single elements
    var mainHeaderElem = document.getElementsByClassName('pk-main-header')[0];
    new app.MainHeader(mainHeaderElem);

    var MobileMenuElem = document.getElementsByClassName('pk-mobile-menu')[0];
    new app.MobileMenu(MobileMenuElem);
    // new app.PlatformSelect();

    var androidPromoNoticeElem = document.querySelector('.pk-android-promo-notice');
    if (androidPromoNoticeElem) {
        new app.AndroidPromoNotice(androidPromoNoticeElem);
    }

    // Components attached to multiple elements
    var a11yShortcutElems = document.getElementsByClassName('pk-a11y-shortcut');
    for (i = 0; i < a11yShortcutElems.length; i++) {
        new app.A11yShortcut(a11yShortcutElems[i]);
    }

    var expandableListElems = document.getElementsByClassName('pk-expandable-list');
    for (i = 0; i < expandableListElems.length; i++) {
        new app.ExpandableList(expandableListElems[i]);
    }

    var externalDownloadLinkElems = document.getElementsByClassName('pk-external-download-link');
    for (i = 0; i < externalDownloadLinkElems.length; i++) {
        new app.ExternalDownloadLink(externalDownloadLinkElems[i]);
    }

    var invisibleGrecaptchaElems = document.getElementsByClassName('pk-invisible-grecaptcha');
    for (i = 0; i < invisibleGrecaptchaElems.length; i++) {
        new app.InvisibleGrecaptcha(invisibleGrecaptchaElems[i]);
    }

    var overlayElems = document.getElementsByClassName('pk-overlay');
    for (i = 0; i < overlayElems.length; i++) {
        new app.Overlay(overlayElems[i]);
    }

    var overlayTriggerElems = document.getElementsByClassName('pk-overlay-trigger');
    for (i = 0; i < overlayTriggerElems.length; i++) {
        new app.OverlayTrigger(overlayTriggerElems[i]);
    }

    var formValidationElems = document.getElementsByClassName('pk-form-validated');
    for (i = 0; i < formValidationElems.length; i++) {
        new app.FormValidation(formValidationElems[i]);
    }

    var videoWrapperElems = document.getElementsByClassName('pk-video-wrapper');
    for (i = 0; i < videoWrapperElems.length; i++) {
        new app.VideoWrapper(videoWrapperElems[i]);
    }

    var bundledAppNoticeElems = document.getElementsByClassName("pk-bundled-app-notice");
    for (i = 0; i < bundledAppNoticeElems.length; i++) {
      new app.BundledAppNotice(bundledAppNoticeElems[i]);
    }

    if (app.flickitySupported) {
        var carouselContainerElements = document.getElementsByClassName('pk-images-carousel');

        try {
            if (carouselContainerElements.length > 0) {
                for (i = 0; i < carouselContainerElements.length; i++) {
                    new app.ImagesCarousel(carouselContainerElements[i]);
                }
            }
        } catch (e) {
            console.warn('Failed to initialize Flickity carousel – applying fallback layout');
            document.documentElement.className = document.documentElement.className.replace('flickity-supported', '');
            document.documentElement.className += ' flickity-unsupported';
        }
    } else {
        console.info('Skipping Flickity initialization since this browser is blacklisted');
    }

    var displayOnlyRatingOptions = {
        min:0,
        max:5,
        step:0.5,
        stars: 5,
        size:'xxs',
        readOnly: true,
        displayOnly: true,
        theme:'unicode',
        showCaption: false,
        rtl: true,
    }

    var interactiveRatingOptions = {
        min:0,
        max:5,
        step:1,
        stars: 5,
        size:'xxs',
        theme:'unicode',
        showCaption: false,
        rtl: true,
    }

    var loadStars = function() {
        $.each($("input[name='stars']"), function () {
            // Initialize star-rating input
            $(this).rating(displayOnlyRatingOptions);

            // Update with rating value
            $(this).rating('update', $(this).data('rating-val'));
        });
        $('.stars-container').show();

        // review rating input in toolversion review overlay form
        $('.pk-form-field.rating.stars').rating(interactiveRatingOptions);
    }

    app.loadStars = loadStars;

    app.loadStars();
};

App.prototype.focusH1IfEscKeyPressed = function (event) {
    if (event.key !== 'Escape') {
        return;
    }

    var openOverlaysCollection = document.getElementsByClassName('pk-overlay is-open');
    if (
        // No overlays are open
        openOverlaysCollection.length === 0 &&
        // Search input isn’t focussed OR search input is focussed and blank
        (
            document.activeElement !== this.mainHeaderSearchInputElem ||
            (
                document.activeElement === this.mainHeaderSearchInputElem &&
                this.mainHeaderSearchInputElem.value === ''
            )
        )
    ) {
        var h1sCollection = document.getElementsByTagName('h1');

        if (h1sCollection.length > 0) {
            h1sCollection[0].pkFocus();
        }
    }
};

App.prototype.pkFocus = function (retainScrollPosition) {
    this.setAttribute('tabindex', '-1');

    if (retainScrollPosition === true) {
        // This effectively retains scroll position by immediately
        // scrolling to the original position after focus() is called
        var preFocusScrollY = window.pageYOffset;
        this.focus();
        window.scrollTo(0, preFocusScrollY);
    } else {
        this.focus();
    }

    this.addEventListener('blur', this.pkUnfocus);
};

App.prototype.pkUnfocus = function () {
    this.removeAttribute('tabindex');

    this.removeEventListener('blur', this.pkUnfocus);
};

App.prototype.hideFocusOutlinesOnMouseDown = function () {
    // console.info('Mousedown detected - hiding focus outlines');
    if (document.documentElement.className.indexOf(' focus-outlines-hidden') === -1) {
        document.documentElement.className = document.documentElement.className + ' focus-outlines-hidden';
    }
};

App.prototype.showFocusOutlinesOnKeyDown = function () {
    // console.info('Keydown detected – showing focus outlines');
    if (
        document.documentElement.className.indexOf(' focus-outlines-hidden') !== -1 &&
        document.activeElement.tagName !== 'INPUT' &&
        document.activeElement.tagName !== 'TEXTAREA'
    ) {
        document.documentElement.className = document.documentElement.className.replace(' focus-outlines-hidden', '');
    }
};

App.prototype.getCookie = function (cookieName) {
    // Via https://stackoverflow.com/a/15724300/7949868
    var value = '; ' + document.cookie;
    var parts = value.split('; ' + cookieName + '=');
    if (parts.length == 2) return parts.pop().split(';').shift();
};


App.prototype.setPlatformCookie = function (urlParams) {
    var data = {
        'platform': urlParams.get('platform'),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    };

    $.post('/set-platform', data, function(data) {
        var httpResponse = $(data)
        var newPlatformBox = httpResponse.find('#global-platform-box').html();
        var appCategoriesMenu = httpResponse.find('#app-category-menu').html();

        var mainLogoLink = httpResponse.find('#main-logo-link').attr('href');

        // update URLs of app categories menu and the main logo's URL as well as update the global platform box text
        $('#main-logo-link').attr('href', mainLogoLink);
        $('#global-platform-box').html(newPlatformBox);
        $('#app-category-menu').html(appCategoriesMenu);

        window.globalPlatform = urlParams.get('platform');

        window.updateHeaderActiveItems(urlParams);
    });
}

app.App = App;

})();

(function () { 'use strict'; if (!app.jsSupported) return;

// Partial URLSearchParams polyfill for IE
(function (w) {

    w.URLSearchParams = w.URLSearchParams || function (searchString) {
        var self = this;
        self.searchString = searchString;
        self.get = function (name) {
            var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(self.searchString);
            if (results == null) {
                return null;
            }
            else {
                return decodeURI(results[1]) || 0;
            }
        };
    }

})(window)

var MainHeader = function (elem) {

    var contentWrapper = $('.content-wrapper');

    var appCategoriesLink = $('.app-categories-link');
    var platformsLink = $('.pk-platform-select');

    var appCategoriesSection = $('.app-category-menu');
    var platformsSection = $('.platform-menu');

    var tip = $('.arrow-up');

    var url = null;
    var prevUrl = document.location.pathname + document.location.search;

    var urlParams = new URLSearchParams(document.location.search);

    $('#main-header').add('#app-category-menu').add('#platform-menu').on('click', 'a.nav-link', function(event) {
        if (!app.uaInfo.isIe9) {
            event.stopPropagation();
            event.preventDefault();

            url = $(this).attr('href');

            if(url.indexOf('contact') !== -1) {
                window.location.href = url;
            } else if (url !== prevUrl) {
                window.history.pushState({}, '', url);

                $('#content').css('visibility','hidden');
                $('#loading').show();
                urlParams = new URLSearchParams(document.location.search);

                window.updateHeaderActiveItems(urlParams);

                // update global_platform cookie if there is a platform param in the new URL and no app category param
                if(urlParams.get('platform') && !urlParams.get('category')) {
                    window.setPlatformCookie(urlParams);
                }

                // AJAX get
                loadContent(url);

                prevUrl = url;
            }
        }
    });

    var loadContent = function (url) {
        $.get(url, onLoaded).fail(onFail);
    }

    var onLoaded = function (data) {
        var htmlResponseObj = $(data);

        var newContent = htmlResponseObj.filter('#content').html();
        var newTitle = htmlResponseObj.filter('title').text();

        document.title = newTitle;
        $('#content').css('visibility','visible');
        closeMenu();
        $('#content').html(newContent);
        app.loadStars();
        $('#loading').hide();

        // reload carousel on platform switch and update the global-platform-box
        if(urlParams.get('platform') && !urlParams.get('category')) {
            reloadCarousel();
        }
    }

    var onFail = function() {
        window.location.href = url;
    }

    window.updateHeaderActiveItems = function (urlParams) {

        $('.nav-link.active').removeClass('active');
        $('.item-thumbnail').removeClass('tinted');
        $('.item-thumbnail-container').removeClass('no-filter');

        appCategoriesLink.removeClass('active');
        if(urlParams.get('platform') && urlParams.get('category')) {
            appCategoriesLink.addClass('active');
        }

        var activeLinks = $('.nav-link[data-slug="'+window.globalPlatform+'"]')
                            .add('.nav-link[data-slug="'+urlParams.get('category')+'"]')
                            .add('.nav-link[href="'+document.location.pathname+document.location.search+'"]');

        activeLinks.each(function () {
            var activeIconElements = $(this).find('img');
            if($(this).attr('id') !== 'main-logo-link' || activeIconElements.attr('class') !== 'logo-img') {
                $(this).addClass('active');
                if(activeIconElements.parent().attr('class') === 'platform-logo-container' || window.app.platform === 'zanga') {
                    // For Zanga, the active category icon gets tinted
                    // Active platform icon gets tinted for both apps
                    activeIconElements.addClass('tinted');
                } else {
                    // For Paskoocheh, the active category icon parent (container)'s grey filter gets removed
                    activeIconElements.parent().addClass('no-filter');
                }
            }
        })

    }

    // on browser back click
    window.onpopstate = function() {
        var url = document.location.pathname + document.location.search;
        urlParams = new URLSearchParams(document.location.search);
        updateHeaderActiveItems(urlParams);
        loadContent(url);

        // update global_platform cookie if there is a platform param in the new URL
        if(urlParams.get('platform') && !urlParams.get('category')) {
            window.setPlatformCookie(urlParams);
        }
    };

    var reloadCarousel = function () {
        var carouselContainerElements = document.getElementsByClassName('pk-images-carousel');
        if(carouselContainerElements.length) {
            for (var i = 0; i < carouselContainerElements.length; i++) {
                new app.ImagesCarousel(carouselContainerElements[i]);
            }
        }
    }

    // underline the active link on the first render
    window.updateHeaderActiveItems(urlParams);

    var openMenu = function () {
        if(contentWrapper.is(':hidden')) contentWrapper.show();
    }

    var closeMenu = function () {
        if(contentWrapper.is(':visible')) {
            contentWrapper.hide();
        }
        appCategoriesLink.removeClass('selected');
        platformsLink.removeClass('selected');
    }

    var toggleMenu = function(ownLink, otherLink, sectionToShow, sectionToHide) {
        // move tip
        if(sectionToShow === appCategoriesSection) {
            tip.removeClass('left');
        }
        else if (sectionToShow === platformsSection) {
            tip.addClass('left');
        }

        if(contentWrapper.is(':visible') && sectionToHide.is(':visible')) {
            sectionToHide.hide();
            sectionToShow.show();
            if(!ownLink.is(':selected')) ownLink.toggleClass('selected');
            otherLink.toggleClass('selected');
        }
        else if (contentWrapper.is(':hidden')){
            sectionToShow.show();
            sectionToHide.hide();
            openMenu();
            ownLink.toggleClass('selected');
        }
        else {
            closeMenu();
        }

    }

    appCategoriesLink.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        toggleMenu(appCategoriesLink, platformsLink, appCategoriesSection, platformsSection);
    });
    platformsLink.on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        toggleMenu(platformsLink, appCategoriesLink, platformsSection, appCategoriesSection);
    });

    contentWrapper.on('click', function(event){
        event.stopPropagation();
    });

    $(document).on('click', function(event){
        // if the target is a descendent of content-wrapper do nothing
        if($(event.target).is(".content-wrapper *")) return;
        // otherwise, close any opened menu
        closeMenu();
    });

    $('.pk-mobile-menu-trigger').on('click', function (event) {
        event.preventDefault();
        $(this).hide();
        $('.pk-mobile-menu-cross').show();
    });

    $('.pk-mobile-menu-cross').on('click', function (event) {
        event.preventDefault();
        $(this).hide();
        $('.pk-mobile-menu-trigger').show();
    });

    this.mainHeaderElem = elem;
    this.contentWrapper = document.getElementById('main-header-dropdown-content-wrapper')
    this.activateSearchElem = document.getElementById('main-header-activate-search');
    this.searchCloseButtonElem = document.getElementById('main-header-close-search-button');
    this.searchFormElem = document.getElementById('main-header-search-form');
    this.searchInputElem = document.getElementById('main-header-search-input');
    this.searchSubmitButtonElem = document.getElementById('main-header-search-submit');

    this.searchCanBeActivatedByFocus = (
        !app.uaInfo.isAndroidFirefox &&
        !app.uaInfo.isIos
    );
    this.searchHasBeenTriggered = false;
    this.searchIsActive = false;
    this.searchInputElemHasValue = (this.searchInputElem.value !== '');

    this.activateSearchElem.addEventListener('click', this.focusSearchInput.bind(this), false);
    this.searchCloseButtonElem.addEventListener('mousedown', this.onSearchCloseButtonClick.bind(this), false);
    this.searchFormElem.addEventListener('submit', this.onSearchFormSubmit.bind(this), false);
    this.searchInputElem.addEventListener('keydown', this.updateSearchBlank.bind(this), false);

    document.addEventListener('paskfocuschange', this.onPaskFocusChange.bind(this), true);
    window.addEventListener('paskkeydown', this.focusSearchInputIfForwardSlashKeyPressed.bind(this), true);
    window.addEventListener('paskkeydown', this.clearSearchIfEscKeyPressed.bind(this), true);
    window.addEventListener('click', this.onSearchCloseButtonClick.bind(this), true);
    window.addEventListener( 'resize' , this.onResize.bind(this), false);

    /*
    GH 2018-02-15: The search form is hidden from VoiceOver on iOS because of a
    seemingly-unresolvable collision with Safari’s VoiceOver behaviour and a
    VoiceOver state desync bug. The issues:

    1) Safari only seems to fire focusin and focusout on anchor and button
       elements, which means  searchIsActive is only updated when certain
       elements take focus. This isn’t the end of the world since the invisible
       (technically hidden via z-index and opacity) elements are still
       announced, but:

    2) When the text <input> is activated via VoiceOver, the preceeding <select>
       is activated instead. I can’t figure out the exact cause. My best guess
       is that it’s a desync between VoiceOver’s interface and underlying logic.
       It could even be that VoiceOver triggers clicks by simulating a click via
       Safari, and since the <select> is tecnically still above the <input> due
       to issue 1, it’s triggering the <select> instead?

    Regardless of the cause, the best solution I could find was to disable
    focus-based search activation in iOS WebKit. Instead:

    - The form is only set to `display: block` when activated to prevent focus.
      When focus leaves, it’s set back to `display: none`.
    - The search activation button is focussable and exposed to screen readers.

    It would have been cleaner and more semantic to use `hidden` or
    `aria-hidden` for this, but Safari/VoiceOver doesn’t seem to reliably
    recognize when these values are manipulated in JS.

    The name of the property is generic in case this fix turns out to be useful
    for other platforms.
    */
    if (!this.searchCanBeActivatedByFocus) {
        this.searchFormElem.style.display = 'none';
        this.activateSearchElem.removeAttribute('aria-hidden');
        this.activateSearchElem.removeAttribute('tabindex');
    }

    this.updateDomAttributes();
};

MainHeader.prototype.clearSearchIfEscKeyPressed = function (event) {
    if (event.key !== 'Escape') {
        return;
    }

    if (document.activeElement === this.searchInputElem) {
        this.searchInputElem.value = '';
    }
};

MainHeader.prototype.focusSearchInput = function () {
    /*
    GH 2018-02-14: Without the iOS Chrome-specific fix, if the search button is
    clicked in iOS Chrome when the viewport is scrolled, the Chrome toolbar will
    appear on top of the focussed search input. This is caused by some
    combination of iOS WebKit’s handling of fixed elements (AFAIK, fixed
    elements are absolutely positioned while a child input has focus?) and
    Chrome’s UI implementation. Relatively positioning the toolbar works around
    the issue, albeit with a weird jump. As with the general iOS WebKit fix, the
    viewport is scrolled to the top.

    The general iOS case scrolls the viewport to the top. This papers over an
    iOS WebKit bug that causes the viewport to shift up when an input within a
    fixed element is focussed. IMO it feels less broken to just scroll to the
    top, rather than have the viewport slightly shift for no apparent reason.

    With any luck all of these bugs will be fixed at some point so we can remove
    these workarounds!
    */

    this.searchFormElem.style.display = 'block';

    if (app.uaInfo.isIosChrome) {
        // main-header-is-relative is removed in onPaskFocusChange when focus
        // moves away from search <input>
        document.documentElement.className += ' main-header-is-relative';
    } else if (app.uaInfo.isIos) {
        window.scrollTo(0, 0);
    }
    this.searchInputElem.focus();
    this.searchInputElem.select();
};

MainHeader.prototype.focusSearchInputIfForwardSlashKeyPressed = function (event) {
    if (event.key !== 'ForwardSlash') {
        return;
    }

    this.focusSearchInput();
};

MainHeader.prototype.updateSearchBlank = function () {
    window.setTimeout(function() {
        if (this.searchInputElem.value === '') {
            this.searchInputElemHasValue = false;
        } else {
            this.searchInputElemHasValue = true;
        }

        this.updateDomAttributes();
    }.bind(this));
};

MainHeader.prototype.updateDomAttributes = function () {
    if (this.searchHasBeenTriggered) {
        return;
    }

    // .search-is-active
    if (
        this.searchIsActive &&
        !/ search-is-active/.test(this.mainHeaderElem.className)
    ) {
        this.mainHeaderElem.className = this.mainHeaderElem.className + ' search-is-active';
    } else if (
        !this.searchIsActive &&
        / search-is-active/.test(this.mainHeaderElem.className)
    ) {
        this.mainHeaderElem.className = this.mainHeaderElem.className.replace(' search-is-active', '');
    }

    // .search-has-value
    if (
        this.searchInputElemHasValue &&
        !/ search-has-value/.test(this.mainHeaderElem.className)
    ) {
        this.mainHeaderElem.className = this.mainHeaderElem.className + ' search-has-value';
    } else if (
        !this.searchInputElemHasValue &&
        / search-has-value/.test(this.mainHeaderElem.className)
    ) {
        this.mainHeaderElem.className = this.mainHeaderElem.className.replace(' search-has-value', '');
    }
};

MainHeader.prototype.onSearchCloseButtonClick = function (event) {
    this.updateSearchBlank();
    // Close the search box on mobile when a click event fires up outside of the box or the X button was clicked
    if ((window.innerWidth <= 991 && !this.searchFormElem.contains(event.target) && !this.activateSearchElem.contains(event.target)) ||
        (this.searchCloseButtonElem.contains(event.target))) {
        this.searchFormElem.style.display = 'none';
    }
};

MainHeader.prototype.onSearchFormSubmit = function (event) {
    if (this.searchInputElem.value === '') {
        event.preventDefault();
    }
};

MainHeader.prototype.onPaskFocusChange = function (event) {
    this.searchIsActive = this.searchFormElem.contains(event.focusDestination);
    if (!this.searchCanBeActivatedByFocus && !this.searchIsActive) {
        this.searchFormElem.style.display = 'none';
    }

    // This className is added in focusSearchInput
    if (event.focusDestination !== this.searchInputElem) {
        document.documentElement.className = document.documentElement.className.replace(
            ' main-header-is-relative',
            ''
        );
    }
    this.updateDomAttributes();
};

MainHeader.prototype.onResize = function () {
    // Show the search box on desktop if it was closed on mobile and hide it by default on mobile
    if(window.innerWidth > 991 && this.searchFormElem.style.display === 'none') {
        this.searchFormElem.style.display = 'block';
    }

    // Close the drop-down header menu on mobile as there is another mobile menu for mobile
    if(window.innerWidth <= 991 && this.contentWrapper.style.display === 'block') {
        this.contentWrapper.style.display = 'none';
    }
};

app.MainHeader = MainHeader;

})();

(function () { 'use strict'; if (!app.jsSupported) return;

var ImagesCarousel = function (flickityCarouselElement) {
    var showLoadingIndicatorTimeoutId = window.setTimeout(function () {
        flickityCarouselElement.className += ' loading-indicator-visible';
    }, 250);

    var flickityOptions = {
        // “Accessibility” feature disabled since it just enables arrow key
        // navigation, which isn’t really an accessibility feature anyway
        accessibility: false,
        cellAlign: 'center',
        pageDots: false,
        imagesLoaded: true,
        rightToLeft: true,
        wrapAround: true,
        selectedAttraction: 0.17,
        friction: 1,
        setGallerySize: false,
    };

    var carouselCells = flickityCarouselElement.getElementsByClassName('flickity-carousel-cell');
    if (carouselCells.length < 3) {
        console.info('Less than 3 carousel cells – disabling wrap-around to avoid visible Flickity cell shuffling');
        flickityOptions.wrapAround = false;
    }

    // Trigger reflow to make sure containing box is sized correctly before
    // Flickity layout is calculated.
    flickityCarouselElement.offsetWidth;

    this.flickity = new Flickity(flickityCarouselElement, flickityOptions);

    this.flickity.once('settle', function () {
        console.info('Flickity loaded – showing carousel and hiding loading indicator');
        window.clearTimeout(showLoadingIndicatorTimeoutId);

        flickityCarouselElement.className += ' loaded';
    });

    var carouselCellLinks = flickityCarouselElement.querySelectorAll('.js-image-sizing-container-link');
    for (var i = 0; i < carouselCellLinks.length; i++) {
        carouselCellLinks[i].addEventListener('focus', this.onCarouselCellLinkFocus.bind(this), false);
    }
};

ImagesCarousel.prototype.onCarouselCellLinkFocus = function (event) {
    var cellNumber = Number(event.target.getAttribute('data-cell-number'));

    this.flickity.select(cellNumber);
};

app.ImagesCarousel = ImagesCarousel;

})();

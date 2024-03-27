/*!
 * Unicode Theme configuration for bootstrap-star-rating.
 * This file must be loaded after 'star-rating.js'.
 */
(function ($) {
    "use strict";
    $.fn.ratingThemes['unicode'] = {
        filledStar: '&#x2605;',
        emptyStar: '&#x2605;',
        clearButton: '&#x229d;'
    };

    window.onload = function () {
        this.starsContainerElem = document.querySelector('.badges .average-rating .rating-stars');

        if (this.starsContainerElem) {
            this.starsContainerElem.addEventListener('click', function () {
                var element = document.getElementById('pk-toolversion-main-reviews');
                var headerOffset = document.querySelector('.main-header-header').offsetHeight;
                var elementPosition = element.getBoundingClientRect().top;
                var offsetPosition = elementPosition - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            })
        }
    }

})(window.jQuery);

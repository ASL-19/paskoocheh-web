(function () { 'use strict'; if (!app.jsSupported) return;

var VideoWrapper = function (elem) {
    this.elem = elem;

    this.containerElem = null;
    this.externalVideoId = this.elem.getAttribute('data-external-video-id');
    this.iframeElem = null;
    this.iframeElemIsLoading = false;
    this.isLazyLoading = (this.elem.getAttribute('data-is-lazy-loading') === 'true');
    this.videoType = this.elem.getAttribute('data-video-type');

    var containerElemIdAttr = this.elem.getAttribute('data-container-elem-id');
    if (containerElemIdAttr !== null) {
        this.containerElem = document.getElementById(containerElemIdAttr);
    }

    if (!this.isLazyLoading) {
        this.appendVideoPlayerIframe();
    } else if (this.containerElem !== null && this.isLazyLoading) {
        this.containerElem.addEventListener('pkexpandablelistitemopened', this.appendVideoPlayerIframe.bind(this), true);
        this.containerElem.addEventListener('pkexpandablelistitemclosed', this.removeVideoPlayerIframe.bind(this), true);
    }
};

VideoWrapper.prototype.appendVideoPlayerIframe = function () {
    if (this.iframeElem instanceof HTMLIFrameElement) return;

    this.iframeElem = document.createElement('iframe');
    this.iframeElem.addEventListener('load', this.hideLoadingIndicator.bind(this), false);
    this.iframeElem.setAttribute('class', 'video-iframe');
    this.iframeElem.setAttribute('width', '640');
    this.iframeElem.setAttribute('height', '360');
    this.iframeElem.setAttribute('allowfullscreen', '');

    if (this.videoType === 'youtube') {
        this.iframeElem.setAttribute('src', 'https://www.youtube.com/embed/' + this.externalVideoId + '?autoplay=0&hl=fa-ir&iv_load_policy=3&modestbranding=1&playsinline=1&rel=0&showinfo=0');
    } else if (this.videoType === 'vimeo') {
        this.iframeElem.setAttribute('src', 'https://player.vimeo.com/video/' + this.externalVideoId + '?title=0&byline=0&portrait=0');
    }

    this.iframeElemIsLoading = true;
    this.updateDomAttributes();

    this.elem.appendChild(this.iframeElem);
};

VideoWrapper.prototype.removeVideoPlayerIframe = function () {
    if (this.iframeElem instanceof HTMLIFrameElement === false) return;

    this.elem.removeChild(this.iframeElem);
    this.iframeElem = null;
    this.iframeElemIsLoading = false;
};

VideoWrapper.prototype.hideLoadingIndicator = function () {
    this.iframeElemIsLoading = false;
    this.updateDomAttributes();
};

VideoWrapper.prototype.updateDomAttributes = function () {
    if (this.iframeElem instanceof HTMLIFrameElement) {
        if (
            this.iframeElemIsLoading && !/ is-loading/.test(this.iframeElem.className)
        ) {
            this.iframeElem.className = this.iframeElem.className + ' is-loading';
        } else if (
            !this.iframeElemIsLoading && / is-loading/.test(this.iframeElem.className)
        ) {
            this.iframeElem.className = this.iframeElem.className.replace(' is-loading', '');
        }
    }
};

app.VideoWrapper = VideoWrapper;

})();

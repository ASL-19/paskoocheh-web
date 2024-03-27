(function () { 'use strict'; if (!app.jsSupported) return;

var ExpandableList = function (elem) {
    this.elem = elem;
    this.toggleLinkElems = elem.getElementsByClassName('link toggle');

    for (var i = 0; i < this.toggleLinkElems.length; i++) {
        var controlledElementId = this.toggleLinkElems[i].getAttribute('data-controls-id');

        this.toggleLinkElems[i].setAttribute('aria-controls', controlledElementId);
        this.toggleLinkElems[i].setAttribute('aria-expanded', 'false');
        this.toggleLinkElems[i].addEventListener('click', this.onToggleLinkElemClick.bind(this), false);
    }
};

ExpandableList.prototype.onToggleLinkElemClick = function (event) {
    var linkElem = null;
    if (event.target instanceof HTMLAnchorElement) {
        linkElem = event.target;
    } else if (event.target.parentNode instanceof HTMLAnchorElement) {
        linkElem = event.target.parentNode;
    }

    if (linkElem !== null) {
        var controlledElem = document.getElementById(linkElem.getAttribute('aria-controls'));
        if (/ open/.test(controlledElem.className)) {
            controlledElem.className = controlledElem.className.replace(' open', '');
            linkElem.setAttribute('aria-expanded', 'false');

            var expandableListItemClosedEvent;
            try  {
                expandableListItemClosedEvent = new Event('pkexpandablelistitemclosed');
            } catch (e) {
                expandableListItemClosedEvent = document.createEvent('Event');
                expandableListItemClosedEvent.initEvent('pkexpandablelistitemclosed', false, false);
            }

            controlledElem.dispatchEvent(expandableListItemClosedEvent);
        } else {
            controlledElem.className += ' open';
            linkElem.setAttribute('aria-expanded', 'true');
            controlledElem.pkFocus(true);

            var expandableListItemOpenedEvent;
            try  {
                expandableListItemOpenedEvent = new Event('pkexpandablelistitemopened');
            } catch (e) {
                expandableListItemOpenedEvent = document.createEvent('Event');
                expandableListItemOpenedEvent.initEvent('pkexpandablelistitemopened', false, false);
            }

            controlledElem.dispatchEvent(expandableListItemOpenedEvent);

            var linkElemRecordClickPath = linkElem.getAttribute('data-record-click-path');
            if (linkElemRecordClickPath) {
                this.recordClick(linkElemRecordClickPath);
            }
        }

        event.preventDefault();
    }
};

ExpandableList.prototype.recordClick = function (recordClickPath) {
    var recordClickUrl = location.protocol + '//' + location.host + recordClickPath;
    var csrfToken = document.querySelector('meta[name="pk-csrf-token"]').getAttribute('content');

    var recordClickRequest = new XMLHttpRequest();
    recordClickRequest.addEventListener('load', this.onRecordClickLoad);
    recordClickRequest.open('POST', recordClickUrl);
    recordClickRequest.setRequestHeader('X-CSRFToken', csrfToken);
    recordClickRequest.send();
};

ExpandableList.prototype.onRecordClickLoad = function () {
    if (this.status === 404 || this.status === 500) {
        console.warn('Server error when attempting to record click.');
    }
};

app.ExpandableList = ExpandableList;

})();

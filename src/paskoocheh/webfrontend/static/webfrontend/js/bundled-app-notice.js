(function () {
  "use strict";

  if (!app.jsSupported) return;

  var BundledAppNotice = function (elem) {
    this.elem = elem;
    this.closeButtonElem = this.elem.querySelector(".js-close-button");
    this.isHidden = false;

    this.closeButtonElem.addEventListener("click", this.hide.bind(this), false);

    this.updateDomAttributes();
  };

  BundledAppNotice.prototype.hide = function () {
    this.isHidden = true;
    this.updateDomAttributes();
  };

  BundledAppNotice.prototype.updateDomAttributes = function () {
    if (this.isHidden) {
      this.elem.className = this.elem.className + " hidden";
    }
  };

  app.BundledAppNotice = BundledAppNotice;
})();

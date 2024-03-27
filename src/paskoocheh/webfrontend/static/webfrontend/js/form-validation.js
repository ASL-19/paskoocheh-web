(function () { 'use strict'; if (!app.jsSupported) return;

var FormValidation = function (formElem) {
    this.formIsValid = false;

    this.formElem = formElem;
    this.formElem.addEventListener('submit', this.onSubmit.bind(this), false);
    this.formElem.addEventListener('pkformgrecaptchasuccess', this.onFormGrecaptchaSuccess.bind(this), false);

    this.formFieldElems = this.formElem.querySelectorAll(
        '.pk-form-field[data-pk-form-field-validate="true"]'
    );
    this.fieldValidity = {};
    this.initFields();
};

FormValidation.prototype.initFields = function () {
    for (var i = 0; i < this.formFieldElems.length; i++) {
        if (
            this.formFieldElems[i] instanceof HTMLInputElement ||
            this.formFieldElems[i] instanceof HTMLTextAreaElement
        ) {
            if(this.formFieldElems[i].name === 'rating'){
                $(this.formFieldElems[i]).on('rating:change', this.onFieldChange.bind(this));
            } else {
                this.formFieldElems[i].addEventListener('input', this.onFieldChange.bind(this), false);
            }
        } else if (
            this.formFieldElems[i] instanceof HTMLSelectElement
        ) {
            this.formFieldElems[i].addEventListener('change', this.onFieldChange.bind(this), false);
        }

        this.updateFieldValidity(this.formFieldElems[i]);
    }

    this.updateFormValidity();
    this.updateDomAttributes();
};

FormValidation.prototype.onSubmit = function (event) {
    if (!this.formIsValid) {
        event.preventDefault();
    }
    // else if(app.platform === 'zanga') {
    //     this.formElem.submit();
    // }
    else {
        var formSubmitEvent;
        try  {
            formSubmitEvent = new Event('pkformsubmit');
        } catch (e) {
            formSubmitEvent = document.createEvent('Event');
            formSubmitEvent.initEvent('pkformsubmit', false, false);
        }

        this.formElem.dispatchEvent(formSubmitEvent);

        event.preventDefault();
    }
};

FormValidation.prototype.onFormGrecaptchaSuccess = function () {
    this.formElem.submit();
};

FormValidation.prototype.onFieldChange = function (event) {
    if (event && event.target instanceof HTMLElement) {
        this.updateFieldValidity(event.target);
        this.updateFormValidity();
        this.updateDomAttributes();
    }
};

FormValidation.prototype.updateFieldValidity = function (fieldElem) {
    this.fieldValidity[fieldElem.name] = (
        typeof fieldElem.value !== 'undefined' &&
        fieldElem.value !== null &&
        fieldElem.value.length > 0
    );
};

FormValidation.prototype.updateFormValidity = function () {
    var formIsValid = true;
    var formFieldValidityKeys = Object.keys(this.fieldValidity);

    for (var i = 0; i < formFieldValidityKeys.length; i++) {
        if (this.fieldValidity[formFieldValidityKeys[i]] !== true) {
            formIsValid = false;
            break;
        }
    }

    this.formIsValid = formIsValid;
};

FormValidation.prototype.updateDomAttributes = function () {
    // // Individual field “is-valid” classes aren’t used now, but might be useful in the future
    // for (var i = 0; i < this.formFieldElems.length; i++) {
    //     var fieldIsValid = this.fieldValidity[this.formFieldElems[i].name];

    //     if (
    //         fieldIsValid && !/ is-valid/.test(this.formFieldElems[i].className)
    //     ) {
    //         this.formFieldElems[i].className = this.formFieldElems[i].className + ' is-valid';
    //     } else if (
    //         !fieldIsValid && / is-valid/.test(this.formFieldElems[i].className)
    //     ) {
    //         this.formFieldElems[i].className = this.formFieldElems[i].className.replace(' is-valid', '');
    //     }
    // }

    if (
        this.formIsValid && !/ is-valid/.test(this.formElem.className)
    ) {
        this.formElem.className = this.formElem.className + ' is-valid';
    } else if (
        !this.formIsValid && / is-valid/.test(this.formElem.className)
    ) {
        this.formElem.className = this.formElem.className.replace(' is-valid', '');
    }
};

app.FormValidation = FormValidation;

})();

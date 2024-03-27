# Paskoocheh webfrontend

Django [application](https://docs.djangoproject.com/en/1.11/ref/applications/) (module) that implements the Paskoocheh 3.0 web frontend. Uses the models from `blog`, `preferences`, `tools`, and `stats`.

With the exception of the CSS/JS manifests (referenced in base.html, and used to create bundles when `manage.py collectstatic` is run) and references to the middleware and context processors in `base.py`, all code for the web frontend is contained inside this module. It will operate as long as its included in the `INSTALLED_APPS` array and bound to a URLPattern in `paskoocheh/urls.py`.

## Code standards

### JavaScript

- All JavaScript must conform to [ECMAScript 5](https://kangax.github.io/compat-table/es5/). Don’t use ES6+ features like `let`, `class`, or arrow functions.

- All code should conform to the [JSHint](http://jshint.com/docs/) rules defined in `.jshintrc`.

- All files except `head.js` and `js-unsupported.js` should begin and end with the following:

    ```
(function () { 'use strict'; if (!app.jsSupported) return;
[…]
})();
```

- All global variables (configuration, state, and component functions) should be contained inside the `paskoocheh` (`window.paskoocheh`) object.

- Functionality should be expressed as constructable, reusable, and self-contained (to the greatest degree possible) components with names matching associated Django template tags, template HTML files, and CSS files.

### CSS

- All code should conform to the [Stylelint](https://stylelint.io/) rules defined in `.stylelintrc`.

- With the exception of some baseline rules at the top of `global.css`, all rules must be attached to classes prefixed with `pk-` or `pk-g-`. It’s a bit annoying to type (though not with an IDE with autocomplete, e.g. Visual Studio Code), but this rudimentary componentization system improves clarity; avoids conflicts between local and global styles; and discourages accidental modification of global styles.

    - Styles that are used in a single component should be attached to classes with `pk-` prefixes. e.g. All overlay styles should contain `.pk-overlay`.

    - Styles that are reused across components should be attached to classes with `pk-g-` prefixes. e.g. The global boxed element style is applied to `.pk-g-boxed`, not just `.boxed`.

### Python

Like the rest of paskoocheh_web, webfrontend is written for Python 2.7 and conforms to most [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines. Running `/server/linters.sh` (which runs `flake8` using the configuration in `/server/linters.config`) shouldn’t produce any errors or warnings.

## Development priorities

### Compatibility

The site should work on all current browsers, as well as prevalent older/problematic browsers such as IE9+, Android 4.x WebKit, older releases of Samsung Internet, and Opera Mini. It should also work without JavaScript and/or cookies, both in cases in which they’re explicitly disabled, and in cases where they’re being blocked by an extension.

The site uses JavaScript, but provides fallbacks for users without it. For some browsers (e.g Android 4.1 WebKit, IE<9, Opera Mini), JavaScript is deliberately prevented from loading in favour of providing the less complex no-JS experience.

The idea is to keep the site usable for as many users as possible without wasting resources trying to maintain a consistent experience. Maintaining multiple tiers of experience requires some extra time and diligence, but also lets us leverage new browser features without needing to cut off swaths of users on older browsers, which in this site’s case is a non-trivial percentage of our potential users

### Speed and efficiency

View (controller) code should make as few database queries as possible to reduce page generation time. Bandwidth usage should be kept to a minimum by keeping the number of JS/CSS dependencies to a minimum as well as ensuring production assets are minified and compressed in transit. JavaScript should be lean and efficient. Although the site is moving from a single-page app model to a server-generated document model, it should be as fast or faster to navigate, and use less device resources.

View responses are cached using `webfrontend.caches.responses_cache`. This allows most requests to bypass (in order of importance, to my understanding) template rendering, database queries, and much of the Python execution. If this works according to plan, it should result in very low server resource usage and consistently fast responses.

### Accessibility

The site should be navigable via keyboard and screen reader and meet [Web Content Accessibility Guidelines (WCAG)](https://en.wikipedia.org/wiki/Web_Content_Accessibility_Guidelines) to the greatest degree possible.

Some guidelines:

- Include descriptive text for images
- Make sure text has [appropriate contrast](http://webaim.org/resources/contrastchecker/)
- Use appropriate/semantic HTML tags
- Make sure the document outline is logical and consistent, and include hidden headings in cases where the organization/context of an element requires visual context
- Hide decorative/redundant elements from screen readers
- Manage focus in cases where a change in the page requires visual context and/or mouse/touch to perceive and interact with. For example, focus should move to the heading of an overlay when it’s triggered, and back to the overlay trigger when it’s closed. Without focus management, a non-visual user wouldn’t know that an overlay had opened, and wouldn’t know how to navigate to the overlay.

### Componentization

To a reasonable degree, parts of pages that are recognizably discrete and/or reused should be developed as self-contained components. These should be defined as [Django tags](https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#writing-custom-template-tags) that accept all required data as arguments and render HTML with unique `pk-` classes on containing elements. CSS for this and all contained elements should be prefixed with `.pk-` selectors. JavaScript for the component should be encapsulated inside an object that’s used as a constructor for instances of the component, and initialized at page load by using `document.getElementsByClassName` to find instances of it.

For example, the images carousel component is implemented with:

- `templatetags/images_carousel.py`
    - Takes all required data as arguments, and returns a rendering context.
- `templates/webfrontend/images_carousel.html`
    - Has a single top-level element with `pk-images-carousel` classname.
- `static/webfrontend/css/images-carousel.css`
    - All styles scoped to `.pk-images-carousel`.
- `static/webfrontend/js/images-carousel.js`
    - Contains a constructor that takes `.pk-images-carousel` element references (called from `app.js`).

`images_carousel.py` renders `images_carousel.html`, which is styled by `images-carousel.css` and manipulated by `images-carousel.js`. None of the files should have any side-effects.

This pattern is akin to the modern JavaScript frameworks’ component patterns. It requires a bit more boilerplate and developer discipline, but doesn’t require a transpiler or JavaScript on the client.

The objective of this is to avoid creating (or setting the stage for) a [big ball of mud](https://en.wikipedia.org/wiki/Big_ball_of_mud). By ensuring components have strictly-defined boundaries and parameters, the code can (hopefully) remain decoupled as it grows. Python tags, JavaScript components, CSS files, and HTML templates should be modifiable without fear that doing so will lead to unintended side-effects.

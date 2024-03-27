# Paskoocheh webfrontend changelog

*Note: These version numbers are arbitrary and unrelated to the main paskoocheh_web version. They’re exclusively used for CHANGELOG entries and verifying what code is running in staging/production).*

## 1.0.3 [2018-02-27]

### Fixes

- Fixed issue that caused longer category names to get cut off from the beginning when they didn’t fit inside a tool list item box (this was because the text was wrapping up, behind the tool name).

## 1.0.2 [2018-02-23]

### Fixes

- In tool version view, fixed Jalali associated blog post published date displaying with Western Arabic numerals.
- For Markdown content, fixed layout issue with nested lists (was visible in [announcement blog post](https://paskoocheh.com/blog/posts/2018-02-21-paskoocheh-new-version.html)).
- For external app store (Google Play, Apple App Store, Chrome Web Store, etc.) download links, addressed oversight that caused them to always open in the same tab. They’re now allowed to open in a new tab if the user Ctrl/Cmd/middle-clicks on them.

## 1.0.1 [2018-02-22]

### Fixes

- Fixed bug that caused browser extensions in desktop tool lists (i.e. Chrome and Firefox extensions in Linux/macOS/Windows lists) to incorrectly sort by download count.

## 1.0.0 [2018-02-20]

### Changes

- Pointed about page Sayeh link at Paskoocheh Twitter account (was previously pointed at Twitter tool page).

## 1.0.0-rc.11 [2018-02-20]

### Changes

- Updated featured blog posts list title translation.

## 1.0.0-rc.10 [2018-02-16]

### Additions

- Added custom download button images for Apple App Store, Google Chrome Web Store, Google Play Store, and Microsoft Store.

### Changes

- Improved styling and layout of rendered Markdown (e.g. guides, FAQs, blog posts, pages). Added styling for block quotes, addressed some layout edge cases.

## 1.0.0-rc.9 [2018-02-15]

### Fixes

- The same styling/layout is now applied to the output of all Markdown fields.

    In previous releases tool descriptions and FAQs had simpler styles applied to them, which was causing awkward spacing and issues like English numerals being displayed in ordered lists.

## 1.0.0-rc.8 [2018-02-15]

### Fixes
- Fixed minor rendering issue in sidebar horizontal separator: small white line could be visible on higher-resolution devices, or when zoomed in.
- Added workaround for Android 4.4 Browser glitch that caused tool list titles and Android promo notice text to wrap incorrectly.

## 1.0.0-rc.7 [2018-02-15]

### Fixes

- Added workaround for iOS 11.0-11.2 [bug](https://bugs.webkit.org/show_bug.cgi?id=176896) that could cause text input caret to be incorrectly positioned in review and support overlays.
- Added workaround for iOS Safari and iOS Chrome quirks that caused weird behaviour when the header search input was selected. The solution is to scroll to the top of the page when the search is triggered on iOS, which isn’t great, but seems to be the least bad option.
- Addressed Paskoocheh logo and ASL19 logo rendering issues in older versions of the Android Browser and Internet Explorer.
- Fixed a few untranslated strings.

### Changes

- Increased the clickable area of the overlay close button to make it more difficult to miss on touch devices.

## 1.0.0-rc.6 [2018-02-13]

### Changes

- Moved checksum to bottom of tool version view.
- Reviews containing less than 3 characters of text are no longer displayed.
- Review form text field is no longer required (i.e. blank reviews can now be submitted).
- Standardized (most) colours across site. There were previously some slight variances introduced over the course of development.
- Removed inner shadow active state on buttons.
- Updated ASL19 logo image in about page “Paskoocheh team” section.

### Fixes

- Added Farsi translation for “Version” in tool version page top info section.
- Fixed iOS Safari bug that could cause mobile menu to get stuck open if background was used to close it at any point.
- Added workaround for iOS WebKit 11.0-11.2 Safari bug (which should be fixed in iOS 11.3) that caused viewport to shift when search input focussed. This should also prevent the iOS Chrome toolbar from appearing on top of the navbar search input when focussed.
- Addressed several minor tool list item box rendering issues in Chrome, Safari, Android WebKit, and Internet Explorer.
- Fixed some rendering issues in Opera Mini (“extreme” mode).
- Addressed some missing/incorrect accessibility text.
- Fixed accessibility shortcut links in blog post view and error view.

## 1.0.0-rc.5 [2018-02-08]

### Improvements

- Improved layout/alignment of tool list item box.

### Changes

- Adjusted tool list responsive design to show 3 columns (up from 2 columns) of tools on medium-sized phones including the iPhone 6/7/8, Google Pixel, Nexus 5X/6P, and Galaxy S8+. This is achieved by reducing the font size inside the tool list item box at narrower viewport widths.
- Added links to all “Paskoocheh Team” (mascot) images.
- Updated blog post list title translations.

### Fixes

- Added workaround for Mobile Safari tool list item box download icon rendering issue.
- Added workaround for Safari full-bleed logo alignment issue on retina displays.
- Fixed SVG issue causing tool list item box download icon to misalign on Internet Explorer and Android Browser.
- Disabled spelling correction and auto-capitalization for search field.
- Disabled spelling correction, autocompletion, and auto-capitalization for fallback (no-JavaScript) reCAPTCHA fields.
- Fixed issue causing page (about, terms/privacy) subheadings to appear on the same line as paragraphs.

## 1.0.0-rc.4 [2018-02-06]

### Additions

- Added “Paskoocheh team” (mascots) section to about page.

### Changes

- Updated design of tool list item boxes:

    - Increased font size and reduced font weight of tool names.

    - Increased height of tool name container – tool names can now wrap onto a second line.

    - Added category, which is only visible if the tool name doesn’t extend to a second line.

    - Moved average rating and download count to a single line.

- Tool logo images can now be marked as “[full-bleed][1.0.0-rc.4-full-bleed]” in the admin. If a logo is marked as full-bleed in the admin, it will be displayed without any padding in tool list item boxes.

- Increased space between tool lists on homepage.

### Improvements

- [Perso-Arabic (Persian) numerals][1.0.0-rc.4-perso-arabic] are now converted on the server and encoded as themselves, rather than encoded as [Western Arabic numerals][1.0.0-rc.4-western-arabic] and displayed as Perso-Arabic via a special version of the Iran Sans font with the numerals substituted.

    This allows for more flexibility in content (e.g. having Perso-Arabic and Western Arabic numerals in the same text), and prevents Western Arabic numerals from appearing if the Iran Sans web font doesn’t load.

    This shouldn’t cause any problems, but if you spot an incorrect numeral, please let us know since it may have been overlooked!

- Download counts and rating counts now have comma thousands separators (i.e. “1000000” is now formatted as “1,000,000”).

### Fixes

- Various minor fixes and improvements.

[1.0.0-rc.4-full-bleed]: https://en.wikipedia.org/wiki/Bleed_(printing)#Full_bleed
[1.0.0-rc.4-perso-arabic]: https://en.wikipedia.org/wiki/Eastern_Arabic_numerals#Numerals
[1.0.0-rc.4-western-arabic]: https://en.wikipedia.org/wiki/Arabic_numerals

## 1.0.0-rc.3 [2018-02-02]

### Additions

- “About” page now includes “Paskoocheh team” section (illustrations not final).

### Fixes
- Category names displayed in blog post headings and blog post previews now use locale-appropriate field.

### Changes
- Replaced “Terms of use” and “Privacy policy” pages with single “Terms of use and privacy” page.

    This page’s content is sourced from a new “Terms of Service and Privacy Policy” field in the admin Web Texts section. The old “Terms of Service” and “Privacy Policy” fields remain because they’re used in the Android client (and possibly the bots?), however the intent is to remove them in a future version.
- Updated translations.
- Blog homepage title is now invisible.

## 1.0.0-rc.2 [2018-01-31]

### Fixes
- Adjusted code of menu and search icons to mitigate rendering issues in some browsers.
- Fixed search input layout issue that allowed text to overlap with clear “(–)” button.

## 1.0.0-rc.1 [2018-01-31]

### Additions
- Added Android app promo notice, which replaces the header Android button. The notice will only be shown if the user’s browser identifies as running on Android. If they hide it, it will be shown again in one week (this value is easy to change).

### Changes
- Updated header design:
    - Reduced height
    - Changed menu and search icons
    - Removed Android button
    - Adjusted responsive styles
- Updated download and rating star icons (appear inside tool version preview boxes, and on tool version pages).

## 1.0.0-beta.5 [2018-01-30]

### Changes
- Reviews are now filtered by language.

    The language field is set on the server, so this doesn’t mean reviews written in English won’t be accepted or displayed. It will only have a meaningful effect when we release the Arabic version.

### Improvements
- Images in blog post preview boxes now fill all available space, cutting off the image horizontally if it’s narrower than 2.5:1, or cutting off the image vertically if it’s wider than 2.5:1.
- On stats site, it’s now possible to select the current date as the end date. The end date still defaults to yesterday to avoid displaying partial data for the current date.

## 1.0.0-beta.4 [2018-01-30]

### Additions
- The site can now enforce a canonical domain name. i.e. It can be set up to redirect `www.paskoocheh.com` and `beta-sec.paskoocheh.com` requests to `paskoocheh.com` once the site is live. This improves SEO and avoids duplicate stats.
- Added a new blog category “description” field. This field isn’t displayed on the site, but is used as social media description and search engine snippet suggestion for blog category pages.

### Fixes
- If a download count can’t be found, the site now displays “–” rather than “0”.
- Fixed incorrect Jalali date conversion. Accidentally used the minute value rather than the month!
- Addressed issue that could cause stats to disappear and lists sorted by download count to be incorrect for several hours after a new version of the site was deployed.

### Improvements
- Merged new translations.
- Implemented a server-enforced (and text-direction-aware) character limit for tool names displayed in tool list item boxes.

    This will help avoid cases where a tool name extended past the edge of its container. This was especially problematic for English tool names since the beginning of the right-aligned name could end up cut off.

    The current maximum number of characters is a bit conservative – it can be raised if it makes sense to do so.
- Improved styling of blog post content:
    - Images are now centred.
    - Tables are now styled.
    - Links now have underlines.
- Several design improvements:
    - Reduced the font size of subheadings across the site.
    - Adjusted sizing of headings on blog index and search pages to reflect data hierarchy.
    - Removed the “Category” heading from the sidebar.
    - Reduced margin between image carousel items.
    - Reduced the brightness of inactive image carousel items.
    - Removed the translucent backgrounds behind the image carousel control arrows.
    - Removed promo carousel from category pages (it now only appears on the homepage).
- Added underlines to links inside page headings (e.g. link to associated version page in the headings on FAQ, Guide, Tutorial, and Review pages).
- Improved keyboard navigation and accessibility of image carousels.
- Many behind-the-scenes code quality and organization improvements.

## 1.0.0-beta.3 [2018-01-22]

### Fixes
- Address issue that caused page caches to fail to clear when associated data changed in admin. In previous versions, an incompatibility was causing page caches to be erroneously retained in production.

## 1.0.0-beta.2 [2018-01-19]

### Improvements
- If a blog post list is empty, an explanatory message is now displayed in its place.
- Made many behind-the-scenes improvements to the code. None of these should have a visible effect, but the scope of change means it’s possible that errors were introduced.

### Fixes
- Fixed an issue that was preventing the Paskoocheh logo from appearing in social media preview boxes.

### Admin changes
- Blog post “published date” field is now set automatically, rather than requiring manual updates. It’s set the first time a post is saved with “Draft” status and/or the first time a post is saved with “Published” status.

## 1.0.0-beta.1 [2018-01-12]

This is the first beta release, which means it’s effectively feature complete and ready for more thorough testing. I’m not aware of any significant bugs, so if you see anything, please report it through JIRA!

### Additions

This release adds blog functionality to the site. The [administration guide][1.0.0-beta.1-admin-guide] has been updated with some related instructions and tips.

The blog includes:

* The blog homepage (`/blog/`), which currently contains a list of the latest blog posts sorted by date, and a list of the featured blog posts sorted by the “Feature Order” attribute. It can also contain category-specific (or even tool/version-specific, if desired) lists, however these will need to be hard-coded into a future release once the categories have been set up in the admin.
* Blog listing pages (`/blog/posts/`), which display all posts, and can be filtered based on URL arguments, e.g. `/blog/posts/?featured=true`, `/blog/posts/?version=42-android`, `blog/posts/?category=news`. (These URLs are generated by the server, you don’t have to deal with this.)
* Blog post pages (`/blog/posts/2018-01-12-post-slug.html`), which contain the content of the post and links to associated Versions and Tools.
* The blog [Atom]([1.0.0-beta.1-atom]) (RSS-like) feed (`/blog/posts/index.xml`), which users can add to their RSS readers to receive updates, and can be used to add the Paskoocheh blog to Khoondi.

[1.0.0-beta.1-atom]: https://en.wikipedia.org/wiki/Atom_(standard)
[1.0.0-beta.1-admin-guide]: https://asle19.atlassian.net/wiki/spaces/PAS/pages/101974017/Paskoocheh+3.0+administration+guide

### Changes
* Restored the page links (about, terms of service, privacy policy) to the sidebar/menu, and added a link to the blog.
* Changed the backend blog models to reflect the blog design, as well as to make the editing experience more user-friendly. (We know it’s still not great compared to WordPress – please let us know if you have any suggestions or pain points.)
* Updated translations file. Will send file for completion once this version of the site is deployed.

### Improvements
- Various small tweaks to the layout.

### Fixes
- Various small bug fixes.

## 0.11.0 [2018-01-02]

### Improvements
- Improved styling of images carousel (promo images, version screenshots) next/previous buttons to better reflect the design.
- Reduced the minimum size of tool list boxes. More columns of tools will appear in some screen sizes, though most phones will still display two columns. This was mostly achieved by reducing the font size of the tool names. For technical/usability reasons this is about as small as they can get.
- Image carousels now attempt to limit their height to the height of the viewport (screen) to avoid cases where images were taller than the screen. This was especially problematic on phones in the landscape orientation. The new behaviour can lead to some overly-small carousels – something we can’t really address without getting rid of the fixed navigation bar, which severely limits the screen height.
- Clicking the background behind an overlay now closes the overlay.
- Tutorial videos contained within expandable list items (i.e. on version pages and tutorial listing pages) now unload when their containing expandable list item is closed. Previously they would continue to play and consume resources even when hidden.
- When an external video player (YouTube/Vimeo) is loading in, a loading indicator is now displayed.
- Added [canonical links](https://en.wikipedia.org/wiki/Canonical_link_element) to all pages to improve SEO and shared URLs.

### Changes
- Review and support forms are now hidden in the Android 4.1 browser due to reCAPTCHA compatibility issues.

### Fixes
- Fixed issue causing incorrect ordering by download count.
- When a tool list isn’t platform-specific, aggregate download counts and average ratings are now displayed as expected. (Aggregate counts were broken when the caching system was added in the previous version.)
- Versions are now only displayed if both the version and its parent tool are marked as publishable.
- Tool Infos, FAQs, Guides, Tutorials, and Web Texts are now filtered by (newly-added) publishable fields.
- Fixed overlay “cancel” buttons, which for a time had no effect.
- Fixed bug that caused the viewport to move to the top when an expandable list item was clicked in Internet Explorer 9/10/11.

## 0.10.0 [2017-12-11]

### Improvements
- Added a caching system. If it works correctly it should have no visible effects, but will result in dramatically faster response times and reduced server load.

## 0.9.2 [2017-11-29]

### Additions
- Added Google Analytics reporting (precluded if browser Do Not Track option is enabled).

### Improvements
- Added margins between and beneath reviews.

### Fixes
- Addressed issue that could cause unexpected scrolling when an expandable list item (FAQ or tutorial) was clicked.
- Overlays no longer retain their internal scroll position when closed and reopened.

## 0.9.1 [2017-11-24]

### Fixes
- Potential fix for (or at least mitigation of) bug causing intermittent layout issues (e.g. menu immediately appearing then sliding away, incorrect promo image carousel layout, etc.) on page load, especially on browsers without assets cached.

## 0.9.0 [2017-11-22]

### Improvements
- On version pages, rating count is now displayed inside the average rating badge.

### Changes
- Screenshots and logos are now filtered by language. They will only be displayed if their language attribute matches the request or is unset.

### Improvements
- Updated Farsi translations.
- Implemented some design improvements, including:
    - For expandable FAQ/tutorial lists, improved vertical text alignment and adjusted borders to match mockup.
    - Reduced margins between tool grid items by 50%.
    - Added slight border radius to tool grid items.
    - Changed layout of header (varies based on width of viewport).
- Focus outlines (on macOS, blue outline/glow) are now hidden when the keyboard isn’t being used to navigate. The outlines were previously very noticeable in some places, especially when expanding items in FAQ/tutorials lists.
- Pressing the “/” (forward slash) key now focuses the search input. This is a common keyboard shortcut on other websites.
- Consolidated some styling/layout code to improve consistency across parts of the site.

### Fixes
- Reworked image carousel code to (hopefully) address intermittent bug causing layout to break on page load.
- Fixed a bug that caused the search field “Clear search” (-) button to fail to cancel the search box takeover on mobile at some viewport widths.
- Submitting an empty search query no longer opens a search view displaying all tools.

## 0.8.1 [2017-11-17]

### Changes
- On version pages, moved support section above reviews section.
- On version pages, FAQs, guides, and tutorials sections are now only displayed if not empty.
- On version pages, platform selection bar items are now listed in alphabetical order (using Farsi transliteration – still not sure it’s correct).
- On home, category, search, and version pages, changed the calculation of average ratings and total download counts. Displayed values are now version-specific by default. Pan-version average ratings and download counts are only displayed in two cases: in index and search pages when the global platform is “all”; and in search page “for other operating systems” list.
- FAQ listings and version view guide links are now filtered by language.

### Improvements
- Many behind-the-scenes code improvements. Should have no visible effect unless I made a mistake.

## 0.8.0 [2017-11-14]

### Additions
- Implemented site footer with dynamic 1-3 column responsive layout.
- Implemented admin-controlled ordering of Tool/Version images. Affects ordering of Version screenshots and selection of Tool logo (if multiple logos are present for whatever reason).

### Improvements
- Updated Farsi translations.
- Google reCAPTCHAs (used in review and support forms) are now displayed in Farsi when the site is using the production configuration.
- Average ratings are now limited to one decimal point.

### Fixes
- Added workarounds for some Opera Mini (Extreme mode) rendering issues.
- Adjusted layout code to mitigate some RTL browser bugs.
- Added workaround for Internet Explorer 9/10/11 bug causing mobile menu to fail to open.
- Fixed fallback reCAPTCHA, which appears on older browsers, or when JavaScript is blocked/disabled. Google silently stopped accepting [Invisible reCAPTCHA](https://developers.google.com/recaptcha/docs/invisible) API keys for the fallback IFrame.

## 0.7.6 [2017-11-09]

### Additions
- Added a “slug” field to guide steps. If a guide step has a slug, that step can be linked to by adding “#slug” to the guide URL.

### Changes
- Reviews for older version numbers are no longer listed on the tool version or tool version reviews pages. Outdated reviews will always be accessible via direct link, but will otherwise be inaccessible when a tool version’s version number changes.

## 0.7.5 [2017-11-08]

### Fixes
- Addressed oversight causing review and support form reCAPTCHA code to fail to load.

## 0.7.4 [2017-11-08]

### Improvements
- Adjusted implementation of browser/compatibility detection to improve security (and maybe performance, in some cases).
- Improved accessibility of sidebar page links.

## 0.7.3 [2017-11-07]

### Improvements
- Made some changes to the web server configuration and build process to improve performance and compatibility.

### Fixes
- Fixed several minor browser compatibility and HTML validity issues.
- Added `noopener` and `noreferrer` directives to external links to prevent privacy and security issues.

## 0.7.2 [2017-11-07]

### Fixes
- Fixed bug causing quotation marks to appear in tool list titles even when query was empty.

## 0.7.1 [2017-11-06]

### Improvements
- Integrated first draft of Farsi translation.

### Fixes
- Fixed bug causing homepage “URL contains unknown category code” error view to fail to display.

## 0.7.0 [2017-11-01]

### Additions
- On Linux (64-bit) version pages, 32-bit Linux download links are displayed if the tool also has a 32-bit Linux version.
- Added preliminary `<meta>` tags (for search engines, Twitter, Facebook, etc.) to most views. Where appropriate, view-specific content is provided as the page description. On tool version pages, the tool logo is provided as the page image. **Outreach: Please test the social media previews! They’re easy to change if you’d prefer different formatting.**

### Changes
- Average ratings (on the single version page and in tool list boxes) are now based on ratings for all versions of the tool, not just the displayed/linked tool.
- Download counts (on the single version page and in tool list boxes) are now based on all versions of the tool, not just the displayed/linked tool.
- Review listing pages are now paginated. Previously, all reviews would be displayed at once.
- Promo images are displayed in the provided order.
- Tutorial videos are now listed in the provided order.

### Fixes

- Unpublished promo images are no longer displayed on homepage.
- In FAQ lists, localized platform names are now displayed, and “All” platform name is now translatable.

## 0.6.0 [2017-10-19]

### Additions

- Implemented [gettext](https://en.wikipedia.org/wiki/Gettext)-based localization. All text should now be translatable, though some hard-coded text may have slipped through.
- Implemented about, terms of service, and privacy policy pages with content sourced from the database.
- Added appropriate (and translatable) page titles for all views. Before now, many just used the name of the tool.

### Changes

- Webfrontend (the new interface) is now mapped to the root of the site, rather than `/v3/`. Code and configuration related to the Angular (V2) site has been removed.
- Adjusted templates to support fields that were changed from WYSIWYG HTML to [Markdown](https://en.wikipedia.org/wiki/Markdown).

### Improvements
- Translated platform and tool type names (from the database) are now displayed across the site.
- Header platform drop-down menu selections are now sourced from the database rather than hard-coded.
- Review lists now display explanatory message if the version has no reviews.
- Most admin editor fields should now be displayed right-to-left. The styling is very simple and doesn’t account for the language of the content, but for the most part the editing experience should be better than it was before.

### Fixes
- Fixed oversight causing “Please allow cookies” error message to fail to display if the user submitted a review or support form with cookies disabled.

## 0.5.0 [2017-10-11]

### Additions
- Added “Featured”, “Most downloaded”, “Recently added”, and “Recently updated” sections to homepage. These lists display 4-6 tools depending on screen width, and include links to corresponding search URLs.

### Improvements
- Category pages are now displayed using the same layout as the homepage, rather than the search layout.
- Search views now support new arguments for ordering the list based on predefined modes (`?orderby`), and limiting the display to featured tools (`?featured`).
- Search views are now displayed at `/tools/` rather than the homepage. Previously the index view would route some requests to the search view based on the provided query string arguments in order to replicate the V2 URL scheme. Legacy URLs are still handled, but without carrying forward the flawed URL scheme. This also has the benefit of displaying something if `/tools/` is requested – previously it had nothing mapped to it despite being part of the URL structure.
- Alphabetically-ordered tool lists now correctly(?) order tools with Farsi-language names. Previously, tools with Farsi names appeared at the end of lists; now they’re ordered according to a transliteration of their Farsi name. (This will need to be verified by Farsi readers.)

### Fixes
- Fixed issue causing small gaps to appear above or beneath the menu and overlay backgrounds on some mobile browsers.
- Address two issues causing the sidebar/menu to appear/move when navigating back on some browsers.

## 0.4.1 [2017-10-05]

### Fixes
- Fixed leftover reference to a renamed file that was causing pages displaying review lists to fail to load in production.
- Fixed an issue with the production logging configuration.

## 0.4.0 [2017-10-04]

### Additions
- Added click tracking for FAQs. FAQ click_count attributes are now incremented when an FAQ is expanded in a FAQ list. Views for single FAQ pages aren’t tracked using this mechanism since doing so might skew the numbers, and because we can already track this via Google Analytics.
- Added recording of S3 downloads. Tool version download links now point at a `/download` URL that gets an S3 URL, records the download, then redirects to the S3 URL. This may also help mitigate download abuse, though it wouldn’t stop a knowledgeable/dedicated mischief-maker.
- Added recording of referrals to external download sites. Includes detection of App Store, Chrome Web Store, Google Play Store, Microsoft Store (Windows/Windows Phone), and Mozilla Add-ons, as well as generic “External website” type.

### Fixes
- Addressed minor layout issue that could cause the tool version page badges to jitter as the page renders.
- Fixed mistake causing download counts and average ratings to fail to appear on tools with localized names.

## 0.3.0 [2017-10-03]

### Additions
- Tool version download counts and average ratings are now displayed in tool listings and the tool version detail page. Previous values were placeholders.
- Added support for tool and tool version FAQs. The first 5 FAQs associated with a version or its parent tool are displayed on the tool version page using a new expandable/collapsible component. There are also several new views:
    - All tool version FAQs (e.g. `/tools/1/android/faqs/`): Lists all FAQs associated with a tool version or its parent tool.
    - Single tool version FAQ (e.g. `/tools/1/android/faqs/1.html`): Displays a single FAQ associated with a tool version.
    - All tool FAQs (e.g. `/tools/1/faqs/`): Lists all FAQs associated with a tool, including those associated with all of the tool’s versions.
    - Single tool FAQ (e.g. `/tools/1/faqs/1.html`): Displays a single FAQ associated with a tool.
- Added support for tool version video tutorials. The first 5 video tutorials (Tutorial) associated with a version are displayed on the tool version page. At the moment only YouTube and Vimeo video links are supported (not uploaded video files or other services). Embedded video players are listed using the expandable/collapsible component, and lazy-loaded where appropriate to reduce bandwidth usage. There are also two new views:
    - All tool version tutorials (e.g. `/tools/1/android/tutorials/`): Lists all tutorials associated with a tool version.
    - Single tool version FAQ (e.g. `/tools/1/android/tutorials/1.html`): Displays a single tutorial associated with a tool version.
- Added support for tool version guides. If a tool version has at least one step (“Guide”), the tool version page will include a link to a new view:
    - Tool version guide (e.g. `/tools/1/android/guide.html`): Displays all guide steps associated with a tool version.
- Added favicon images.


### Fixes
- Various minor fixes.

## 0.2.0 [2017-09-27]

### Additions
- The latest 5 reviews are now displayed on the tool version page.
- Added dedicated tool version reviews listing page.
- Added dedicated tool version review page.

### Changes
- Adjusted review and support forms to use new API mechanism.

### Improvements
- Reduced width of sidebar/menu.
- Added landscape/portrait-specific images carousel layout adjustments. These will help avoid scenarios in which the images carousel fills too much of the viewport, as well as scenarios in which individual images are too small.
- Improved performance of image carousels by using cached versions of image dimensions.
- Modified the way components are denoted in HTML in order to improve performance of CSS and JavaScript.
- Encapsulated almost all JavaScript variables into shared window.paskoocheh to avoid global name collisions and improve code clarity.
- Assorted performance, accessibility, and code quality improvements.

### Fixes
- Fixed bug causing Chrome/Firefox tool list item badges to block clicking on the item.
- Support form email field now uses [Western Arabic numerals](https://en.wikipedia.org/wiki/Arabic_numerals).
- Addressed oversight causing form submissions to fail if multiple reCAPTCHAs have been loaded in the same page.
- Various minor fixes.

## 0.1.1 [2017-09-18]

### Fixes
- Modified some code to account for changes to other Paskoocheh components.

## 0.1.0 [2017-09-18]

First tagged release. Changes since last PR:

### Changes
- Added Google reCAPTCHA to review and support/feedback forms. Uses [Invisible reCAPTCHA](https://developers.google.com/recaptcha/docs/invisible) (which requires no user input if Google trusts them) when JavaScript is available; falls back to a simpler inline challenge otherwise.

### Improvements
- Added a translucent background between content and menu when mobile menu is active.
- Improved responsive layout of tool version page platform selection bar.
- Improved IE8 compatibility to some degree.
- Improved Opera Mini compatibility.
- Improved pattern for encapsulating parts of site into reusable components, setting the stage for easier future development.

### Fixes
- Adjusted sidebar layout to allow for vertical scrolling when necessary.
- Fixed issue causing sidebar to sometimes momentarily appear on load in Safari/WebKit.
- Fixed some miscellaneous rendering and logic issues.

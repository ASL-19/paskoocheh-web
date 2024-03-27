# Paskoocheh stats changelog

## 1.0.0-rc.1 [2017-11-28]

Initial conversion/port of site to Django app consuming the new stats API.

### Improvements
- Cleaned up and modernized JavaScript code (didn’t rewrite everything, but improved the general structure, moved global variables into single container, refactored, moved reused code into helper functions, etc.).
- Improved/simplified approach to avoiding displaying today’s (incomplete, and therefore lower) stats. Instead of dropping the final X and Y data, the default end date is set to yesterday.
- A loading indicator is now displayed when a chart is loading.
- When a chart is selected or the date range changes, the previous chart is immediately removed from the page rather than remaining until it’s replaced.
- Left sidebar is now fixed-width to allow more room for chart container.

### Changes
- All data is now read from the new stats api (`/api/v1/stats/*`). This dramatically reduces bandwidth usage and loading times, especially for the “per tool” chart.
- Changed format of start and end date fields.
- Shortened and improved consistency of chart titles.

### Fixes
- Selected start date and end dates are now automatically applied to newly-loaded charts. Previously the dates would only apply to an chart if a date field was changed after the chart was loaded – charts would always load in with the default/initial date range.

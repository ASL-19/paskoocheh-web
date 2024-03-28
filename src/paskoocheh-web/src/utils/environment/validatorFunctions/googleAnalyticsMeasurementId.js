const { makeValidator } = require("envalid");

const googleAnalyticsMeasurementId = makeValidator((s) => {
  if (/^G-\w+$/.test(s) || s === "") {
    return s;
  }

  throw new Error(
    'Must be a Google Analytics MeasurementId ID (e.g. "G-XXXXXXXXXX")',
  );
});

module.exports = googleAnalyticsMeasurementId;

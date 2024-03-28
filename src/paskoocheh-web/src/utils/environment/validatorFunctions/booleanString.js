const { makeValidator } = require("envalid");

/**
 * Validate that environment variable is "true" or "".
 *
 * Envalid custom validator (https://github.com/af/envalid#custom-validators)
 */
const booleanString = makeValidator((s) => {
  if (s === "true" || s === "") {
    return s;
  }

  throw new Error('Must be "true" or ""');
});

module.exports = booleanString;

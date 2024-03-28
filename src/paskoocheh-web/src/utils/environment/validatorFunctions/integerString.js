const { makeValidator } = require("envalid");

/**
 * Validate that environment variable is a string containing an integer.
 *
 * Envalid custom validator (https://github.com/af/envalid#custom-validators)
 */
const integerString = makeValidator((s) => {
  if (s === "" || /^\d+$/.test(s)) {
    return s;
  }

  throw new Error("Must be an integer");
});

module.exports = integerString;

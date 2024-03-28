const { makeValidator } = require("envalid");

/**
 * Validate that environment variable is a URL.
 *
 * Valid examples:
 *
 * - "http://localhost:8000/graphql/"
 * - "https://example.com")
 *
 * Envalid custom validator (https://github.com/af/envalid#custom-validators)
 */
const url = makeValidator((s) => {
  if (/^https?:\/\/.*$/.test(s)) {
    return s;
  }

  throw new Error("Must be a URL");
});

module.exports = url;

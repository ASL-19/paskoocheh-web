const { makeValidator } = require("envalid");

/**
 * Validate that environment variable is a protocol and host.
 *
 * Valid examples:
 *
 * - "https://beepassvpn.com"
 * - "http://localhost:3000")
 *
 * Envalid custom validator (https://github.com/af/envalid#custom-validators)
 */
const protocolAndHost = makeValidator((s) => {
  if (/^https?:\/\/[^/]*$/.test(s)) {
    return s;
  }

  throw new Error(
    'Must be a protocol and host with no trailing slash (e.g. "https://beepassvpn.com" or "http://localhost:3000")',
  );
});

module.exports = protocolAndHost;

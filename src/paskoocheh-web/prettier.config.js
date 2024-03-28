/** @type {import("prettier").Config} */
const prettierConfig = {
  trailingComma: "all",
  // eslint-disable-next-line sort-keys-fix/sort-keys-fix
  overrides: [
    {
      files: ["*.json"],
      options: {
        // Prevent consolidating multiple values on one line
        printWidth: 1,
      },
    },
  ],
};

module.exports = prettierConfig;

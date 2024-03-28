require("@rushstack/eslint-patch/modern-module-resolution");

const eslintConfig = {
  extends: [
    "@asl-19/eslint-config",
    "@asl-19/eslint-config/next",
    "@asl-19/eslint-config/react",
    "@asl-19/eslint-config/typescript",
  ],
  plugins: ["sort-keys-fix"],
  rules: {
    "@emotion/syntax-preference": ["warn", "object"],
    "no-restricted-imports": [
      "warn",
      {
        paths: [
          // https://mui.com/material-ui/guides/minimizing-bundle-size/#option-one-use-path-imports
          {
            message:
              "Import from @ariakit/react/* instead (to reduce build time)",
            name: "@ariakit/react",
          },
        ],
        patterns: [
          // Default from @asl-19/eslint-config
          {
            group: ["./", "../"],
          },

          // https://mui.com/material-ui/guides/minimizing-bundle-size/#option-one-use-path-imports
          {
            group: ["@ariakit/react/*/*"],
            message:
              "Import from @ariakit/react/* instead (to reduce build time)",
          },
        ],
      },
    ],
    "sort-keys-fix/sort-keys-fix": [
      "warn",
      "asc",
      {
        caseSensitive: false,
        natural: true,
      },
    ],
  },
};

module.exports = eslintConfig;

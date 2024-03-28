# paskoocheh-website-web

Paskoocheh front-end. Powered by [Next.js](https://nextjs.org).

- [Instructions](#instructions)
    - [Prerequisites](#prerequisites)
    - [Build and start development server](#build-and-start-development-server)
    - [Build and start production server](#build-and-start-production-server)
    - [Build and run tests](#build-and-run-tests)
- [Environment variables](#environment-variables)
- [Guidelines](#guidelines)
    - [VS Code](#vs-code)
    - [GraphQL](#graphql)
        - [Schema](#schema)
    - [TypeScript](#typescript)
    - [Styling](#styling)
    - [ESLint](#eslint)
    - [Prettier](#prettier)

## Instructions

### Prerequisites

- You need Node.js 20.x and NPM 10.x (bundled with Node 20.x) installed and in the shell’s PATH.
- All required [environment variables](#environment-variables) must be set.

### Build and start development server

```sh
npm install
npm run dev
```

### Build and start production server

```bash
npm install
npm run dev-build-start
```

### Build and run tests

```bash
npm install
npm run dev-lint-test
```

## Environment variables

Environment variables are documented in [paskoocheh-env.d.ts][env-vars-paskoocheh-env].

For local development we recommend copying [`.env.local.template`][env-vars-env-local-template] to `.env.local` and modifying the contents as needed. The content of `.env.local` will be automatically loaded when the site builds.

If you need a value for `NEXT_PUBLIC_BACKEND_URL` check the internal wiki ask a team member.

**Note**: Any variable beginning with [`NEXT_PUBLIC_`][env-vars-next-public] is exposed in front-end JS files, so must not include any private passwords, URLs, or keys!

[env-vars-env-local-template]: ./.env.local.template
[env-vars-paskoocheh-env]: ./paskoocheh-env.d.ts
[env-vars-next-public]: https://nextjs.org/docs/basic-features/environment-variables#exposing-environment-variables-to-the-browser

## Guidelines

### VS Code

VS Code is strongly recommended for developing this project. If you open the `src/paskoocheh-web` directory in VS Code it will load [`.vscode/settings.json`](.vscode/settings.json) (which includes most the configuration described in the project guidelines) and [`.vscode/extensions.json`](.vscode/extensions.json) (a list of recommended extensions VS Code will prompt you to install when opening the project).

### GraphQL

See the GraphQL section of the internal Next.js guidelines.

#### Schema

When the backend GraphQL schema models change, GraphQL schema file (`src/server/schema.graphql`). This file is used to generate the front-end GraphQL client and types.

In the src_server container shell:

```sh
./manage.py graphql_schema --schema main.schema.schema --out schema.graphql
```

### TypeScript

The project is designed to work with the TypeScript compiler version specified in package.json.

If you’re using VS Code, use the “Select TypeScript Version…” command and select “Use Workspace Version” to avoid subtle issues caused by VS Code using its internal TypeScript version (which might be newer than the version we use to build).

### Styling

All styling is done using [Emotion][emotion].

[emotion]: https://emotion.sh/

### ESLint

The project includes an ESLint configuration. You can run ESLint using `npm run eslint-check`, and auto-fix issues using `npm run eslint-fix` (be careful with this — stash any important changes!).

ESLint rules are enforced in the CI/CD system — changes can’t be merged if there are any warnings or errors.

### Prettier

All code is formatted using [Prettier](https://prettier.io).

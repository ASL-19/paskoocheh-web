import type { NextRequest } from "next/server";
import { match, P } from "ts-pattern";

import redirectLegacyAppUrlsMiddleware from "src/middleware/redirectLegacyAppUrlsMiddleware";

export const config = {
  // By statically defining the middleware matcher we prevent it from running on
  // other URLs
  matcher: ["/tools/(\\d+)/([a-z]+)\\.html"],
};

const legacyToolUrlRegExp =
  /\/tools\/(?<toolPk>\d+)\/(?<platformSlug>[a-z]+)\.html/;

export type LegacyToolUrlParts = { platformSlug: string; toolPk: number };

// This function can be marked `async` if using `await` inside
export const middleware = async (request: NextRequest) => {
  const { pathname } = request.nextUrl;

  const legacyToolUrlMatch = legacyToolUrlRegExp.exec(pathname);

  const legacyToolUrlParts = match(legacyToolUrlMatch?.groups)
    .returnType<LegacyToolUrlParts | null>()
    .with(
      { platformSlug: P.string, toolPk: P.string },
      ({ platformSlug, toolPk }) => ({
        platformSlug,
        // toolPk is guaranteed to be a string of digits if RegExp matched
        toolPk: parseInt(toolPk),
      }),
    )
    .otherwise(() => null);

  if (legacyToolUrlParts) {
    return await redirectLegacyAppUrlsMiddleware({ legacyToolUrlParts });
  }

  console.warn(
    "[middleware] URL didn’t match any middlewares. This shouldn’t ever happen — is config.matcher out of sync with the middleware regular expressions?",
  );
};

import { IncomingMessage } from "http";
import { match, P } from "ts-pattern";

import getUrlPlatform from "src/utils/routing/getUrlPlatform";
import { LocaleCode } from "src/values/localeValues";
import { defaultPlatformSlug } from "src/values/miscValues";

const getReqInfo = (req: IncomingMessage) => {
  const localeCode = match<string, LocaleCode>(req.url ?? "")
    .with(
      P.string.regex(/^\/en/),
      P.string.regex(/^\/_next\/data\/development\/en/),
      P.string.regex(/^\/_next\/data\/[^/]*\/en/),
      () => "en",
    )
    .with(
      P.string.regex(/^\/fa/),
      P.string.regex(/^\/_next\/data\/development\/fa/),
      P.string.regex(/^\/_next\/data\/[^/]*\/fa/),
      () => "fa",
    )
    .otherwise(() => "en");

  // There shouldn’t be any scenario where req.url isn’t set, but just in case we
  // fall back to defaultPlatformSlug
  const platformSlug = req.url ? getUrlPlatform(req.url) : defaultPlatformSlug;

  return { localeCode, platformSlug };
};

export default getReqInfo;

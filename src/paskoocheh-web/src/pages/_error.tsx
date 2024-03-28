import { NextPage } from "next";

import ErrorPageContent, {
  ErrorPageContentProps,
} from "src/components/ErrorPageContent";
import getGraphQlSdk from "src/utils/config/getGraphQlSdk";
import getLocaleMetadata from "src/utils/getLocaleMetadata";
import getPlatforms from "src/utils/page/getPlatforms";

const ErrorPage: NextPage<ErrorPageContentProps> = (props) => {
  return <ErrorPageContent {...props} />;
};

type NextError = Error & {
  statusCode?: number;
};

ErrorPage.getInitialProps = async ({ asPath, err, res }) => {
  const typedErr: NextError | null | undefined = err;

  const { localeCode } = getLocaleMetadata((asPath || "").slice(1, 3));

  const statusCode = typedErr?.statusCode ?? res?.statusCode ?? 500;

  if (!process.browser && res && typeof statusCode === "number") {
    // eslint-disable-next-line no-param-reassign
    res.statusCode = statusCode;
  }

  const platforms = await (async () => {
    try {
      const graphQlSdk = await getGraphQlSdk();

      return await getPlatforms({ graphQlSdk });
    } catch {
      return null;
    }
  })();

  const { default: strings } = await import(
    `src/strings/${localeCode === "en" ? "stringsEn" : "stringsFa"}`
  );

  return {
    localeCode,
    platforms,
    statusCode,
    strings,
  };
};

export default ErrorPage;

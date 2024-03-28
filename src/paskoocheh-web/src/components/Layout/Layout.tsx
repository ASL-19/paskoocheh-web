import { css, Global } from "@emotion/react";
import Head from "next/head";
import { FC, memo, ReactNode } from "react";

import Footer from "src/components/Footer/Footer";
import Header from "src/components/Header/Header";
import { GqlPlatform } from "src/generated/graphQl";
import appleTouchIcon180Png from "src/static/favicons/apple-touch-icon-180x180.png";
import favicon1616Png from "src/static/favicons/favicon-16x16.png";
import favicon3232Png from "src/static/favicons/favicon-32x32.png";
import globalStyles from "src/styles/globalStyles";

const pageContentWrapper = css({
  flex: "1 0 auto",
  width: "100%",
});

const wrapper = css({
  display: "flex",
  flexDirection: "column",
  minHeight: "100vh",
});

const Layout: FC<{
  children: ReactNode;
  platforms: Array<GqlPlatform> | null;
}> = memo(({ children, platforms }) => (
  <div css={wrapper}>
    <Global styles={globalStyles} />

    <Head>
      {/* -----------
        --- Icons ---
        --------- */}

      {/* NOTE: We don’t provide an SVG icon with dark mode styling
          because of edge cases around the way browsers display icons. It’s
          possible for the favicon to be displayed against a light background
          when the OS is in dark mode; and it’s possible for the favicon to be
          displayed against a dark background when the OS is in light mode.
          Because of this providing a favicon that isn’t universally legible
          is an accessibility issue.

          See also: https://css-tricks.com/svg-favicons-in-action/#comment-1775964

          We also don’t provide a <link> tag referencing favicon.ico since
          every modern browser supports PNG favicons, but some will prefer the
          much larger uncompressed .ico file due to browser bugs and/or weird
          interpretations of web standards. */}

      <link
        rel="apple-touch-icon"
        sizes="180x180"
        href={appleTouchIcon180Png.src}
      />

      <link
        rel="icon"
        type="image/png"
        sizes="16x16"
        href={favicon1616Png.src}
      />

      <link
        rel="icon"
        type="image/png"
        sizes="32x32"
        href={favicon3232Png.src}
      />
    </Head>

    <Header platforms={platforms} />

    <div css={pageContentWrapper}>{children}</div>

    <Footer />
  </div>
));

Layout.displayName = "Layout";

export default Layout;

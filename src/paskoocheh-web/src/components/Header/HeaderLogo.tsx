import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import Link from "next/link";
import { memo } from "react";

import LogoSvg from "src/components/icons/logos/LogoSvg";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";

// Note: We need to calculate the logo aspect ratio and manually style the
// width and height to work around an intrinsic SVG sizing bug in WebKit (and
// maybe older versions of Gecko and Blink).

const logoHeight = "2.5rem";

const logoAnchor = css({
  alignSelf: "center",
  display: "flex",
  flex: "0 0 auto",
  position: "relative",
});

const logoSvg = css({
  height: logoHeight,
  width: "auto",
});

const HeaderLogo: StylableFC = memo((props) => {
  const { localeCode } = useAppLocaleInfo();
  const { shared: sharedStrings } = useAppStrings();
  const queryOrDefaultPlatformSlug = useQueryOrDefaultPlatformSlug();

  return (
    <Link
      href={routeUrls.home({
        localeCode,
        platform: queryOrDefaultPlatformSlug,
      })}
      css={logoAnchor}
      {...props}
    >
      <LogoSvg
        aria-label={sharedStrings.siteTitle}
        css={logoSvg}
        logoType="header"
      />
    </Link>
  );
});

HeaderLogo.displayName = "HeaderLogo";

export default HeaderLogo;

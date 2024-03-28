import { css, SerializedStyles } from "@emotion/react";
import { FC, memo, useMemo } from "react";

import FooterLinkList from "src/components/Footer/FooterLinkList";
import { FooterNavLinkInfo } from "src/components/Footer/FooterLinkListItem";
import useQueryOrDefaultPlatformSlug from "src/hooks/useQueryPlatform";
import routeUrls from "src/routeUrls";
import { useAppLocaleInfo, useAppStrings } from "src/stores/appStore";

export type FooterNavStrings = {
  /**
   * Accessibility label for two footer link lists.
   */
  a11yLabel: string;
  contactUs: {
    email: string;
    heading: string;
    telegram: string;
  };
  moreInfo: {
    aboutUs: string;
    heading: string;
    privacyPolicy: string;
    termsAndConditions: string;
  };
};

const container = css({
  display: "contents",
});

/**
 * Displayed with `display: contents;`, so container has no effect on layout
 * (and isn’t stylable via `css` prop).
 */
const FooterNav: FC<{ itemCss?: SerializedStyles }> = memo(({ itemCss }) => {
  const { localeCode } = useAppLocaleInfo();
  const strings = useAppStrings();
  const queryPlatform = useQueryOrDefaultPlatformSlug();

  const contactUsNavLinkInfos = useMemo<Array<FooterNavLinkInfo>>(
    () => [
      {
        text: strings.FooterNav.contactUs.telegram,
        // replace with telegram link
        url: routeUrls.home({ localeCode, platform: queryPlatform }),
      },
      {
        text: strings.FooterNav.contactUs.email,
        url: `mailto:${process.env.NEXT_PUBLIC_CONTACT_EMAIL_ADDRESS}`,
      },
    ],
    [localeCode, queryPlatform, strings],
  );

  const moreInfoNavLinkInfos = useMemo<Array<FooterNavLinkInfo>>(
    () => [
      {
        text: strings.FooterNav.moreInfo.aboutUs,
        url: routeUrls.about({ localeCode, platform: queryPlatform }),
      },
      {
        text: strings.FooterNav.moreInfo.termsAndConditions,
        url: routeUrls.termsOfService({ localeCode, platform: queryPlatform }),
      },
      {
        text: strings.FooterNav.moreInfo.privacyPolicy,
        url: routeUrls.privacyPolicy({ localeCode, platform: queryPlatform }),
      },
    ],
    [localeCode, queryPlatform, strings],
  );

  return (
    <nav aria-label={strings.FooterNav.a11yLabel} css={container}>
      <FooterLinkList
        heading={strings.FooterNav.contactUs.heading}
        navLinkInfos={contactUsNavLinkInfos}
        css={itemCss}
      />
      <FooterLinkList
        heading={strings.FooterNav.moreInfo.heading}
        navLinkInfos={moreInfoNavLinkInfos}
        css={itemCss}
      />
    </nav>
  );
});

FooterNav.displayName = "FooterNav";

export default FooterNav;

import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import FooterNav from "src/components/Footer/FooterNav";
import FooterNewsletterSignUp from "src/components/Footer/FooterNewsletterSignUp";
import FooterSocialMedia from "src/components/Footer/FooterSocialMedia";
import LogoSvg from "src/components/icons/logos/LogoSvg";
import PageSegment from "src/components/Page/PageSegment";
import { useAppStrings } from "src/stores/appStore";
import { fullWidthWrapper } from "src/styles/generalStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

export type FooterStrings = {
  findUs: string;
};

const footerContainer = css(fullWidthWrapper, {
  backgroundColor: colors.greyDark,
  color: colors.shadesWhite,
  padding: "3.75rem 0",
});

const pageSegmentCenteredContainer = css(
  {
    columnGap: "2.5rem",
    display: "flex",
    rowGap: "2rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        flexDirection: "column",
      },
    },
  }),
);

const pageFlexItem = breakpointStyles({
  desktopNarrow: {
    gte: { flex: "1 1 100%", minWidth: 0, width: 0 },
    lt: { flex: "1 1 auto" },
  },
});

const logoSvg = css({
  height: "2.75rem",
  width: "auto",
});

const Footer: StylableFC = memo(({ className }) => {
  const strings = useAppStrings();

  return (
    <footer className={className} css={footerContainer}>
      <PageSegment
        as="section"
        centeredContainerCss={pageSegmentCenteredContainer}
      >
        <div css={pageFlexItem}>
          <LogoSvg
            aria-label={strings.shared.siteTitle}
            css={logoSvg}
            logoType="footer"
          />
          <FooterNewsletterSignUp />
        </div>

        {/* Displayed with `display: contents` so its two FooterLinkList
        children are flex items of pageSegmentCenteredContainer */}
        <FooterNav itemCss={pageFlexItem} />

        <FooterSocialMedia css={pageFlexItem} />
      </PageSegment>
    </footer>
  );
});

Footer.displayName = "Footer";

export default Footer;

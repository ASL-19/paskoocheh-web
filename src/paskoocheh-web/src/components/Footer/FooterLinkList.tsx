import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import FooterLinkListItem, {
  FooterNavLinkInfo,
} from "src/components/Footer/FooterLinkListItem";
import { paragraphP3SemiBold } from "src/styles/typeStyles";

const list = css({
  display: "flex",
  flexDirection: "column",
  gap: "0.25rem",
});

const headingParagraph = css(paragraphP3SemiBold, {
  marginBottom: "1rem",
  minWidth: "8rem",
});

const FooterLinkList: StylableFC<{
  heading: string;
  navLinkInfos: Array<FooterNavLinkInfo>;
}> = memo(({ className, heading, navLinkInfos }) => (
  <div className={className}>
    {heading && <h2 css={headingParagraph}>{heading}</h2>}
    <ul css={list}>
      {navLinkInfos.map((footerLinkInfo, index) => (
        <FooterLinkListItem footerLinkInfo={footerLinkInfo} key={index} />
      ))}
    </ul>
  </div>
));

FooterLinkList.displayName = "FooterLinkList";

export default FooterLinkList;

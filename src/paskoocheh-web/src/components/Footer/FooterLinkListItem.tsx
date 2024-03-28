import { css } from "@emotion/react";
import Link from "next/link";
import { FC, memo } from "react";

import colors from "src/values/colors";

export type FooterNavLinkInfo = {
  children?: Array<FooterNavLinkInfo>;
  text: string;
  url: string;
};

const listItem = css({
  alignItems: "center",
  display: "flex",
});

const link = css({
  color: colors.shadesWhite,
  overflow: "hidden",
  whiteSpace: "nowrap",
});

const FooterLinkListItem: FC<{
  footerLinkInfo: FooterNavLinkInfo;
}> = memo(({ footerLinkInfo }) => (
  <li css={listItem}>
    <Link href={footerLinkInfo.url ?? ""} css={link}>
      {footerLinkInfo.text}
    </Link>
  </li>
));

FooterLinkListItem.displayName = "FooterLinkListItem";

export default FooterLinkListItem;

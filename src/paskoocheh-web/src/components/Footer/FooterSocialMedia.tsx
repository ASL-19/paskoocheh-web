import { StylableFC } from "@asl-19/react-dom-utils";
import { css } from "@emotion/react";
import { memo } from "react";

import SocialMediaLinkList from "src/components/SocialMediaLinkList";
import { useAppStrings } from "src/stores/appStore";
import { paragraphP3SemiBold } from "src/styles/typeStyles";
import { breakpointStyles } from "src/utils/media/media";
import colors from "src/values/colors";

const container = css(
  {
    alignItems: "flex-end",
    display: "flex",
    flexDirection: "column",
    rowGap: "1rem",
  },
  breakpointStyles({
    desktopNarrow: {
      lt: {
        alignItems: "flex-start",
      },
    },
  }),
);

const FooterSocialMedia: StylableFC<{}> = memo(({ className }) => {
  const strings = useAppStrings();

  return (
    <div className={className} css={container}>
      <h1 css={paragraphP3SemiBold}>{strings.Footer.findUs}</h1>
      <SocialMediaLinkList
        facebookUsername={strings.shared.socialMediaUsernames.facebook}
        telegramUsername={strings.shared.socialMediaUsernames.telegram}
        twitterUsername={strings.shared.socialMediaUsernames.twitter}
        instagramUsername={strings.shared.socialMediaUsernames.instagram}
        itemIconColor={colors.shadesWhite}
        itemSize="2rem"
      />
    </div>
  );
});

FooterSocialMedia.displayName = "FooterSocialMedia";

export default FooterSocialMedia;
